"""Check the static artifact before CI uploads it to GitHub Pages.

The project is served under /simworld/ on Pages. Root-absolute asset URLs
would bypass that prefix, so index resources must be relative. Data URLs
are resolved by the browser's site-relative URL helper.
"""
from pathlib import Path, PurePosixPath
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import hashlib
import json
import zipfile
import re

ROOT = Path(__file__).resolve().parent / 'dist'
checks = 0


def require(condition, message):
    global checks
    checks += 1
    if not condition:
        raise AssertionError(message)


def artifact(url):
    relative = unquote(urlsplit(url).path).lstrip('/')
    require('..' not in PurePosixPath(relative).parts, f'Unsafe artifact path: {url}')
    result = ROOT / relative
    require(result.is_file(), f'Missing artifact: {url}')
    require(result.resolve().is_relative_to(ROOT.resolve()), f'Artifact escapes dist: {url}')
    return result


class ResourceParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        url = attrs.get('src') if tag == 'script' else attrs.get('href') if tag in ('link', 'a') else None
        if not url or url.startswith('#') or urlsplit(url).scheme:
            return
        require(not url.startswith('/'), f'Root-absolute URL breaks GitHub project Pages: {url}')
        artifact(url)


for page in ROOT.glob('*.html'):
    ResourceParser().feed(page.read_text(encoding='utf-8'))
data = json.loads((ROOT / 'data/project.json').read_text(encoding='utf-8'))
require(len(data['phases']) == 17, 'The roadmap must retain all 17 phases')
publication=json.loads((ROOT.parent.parent/'research/whitepaper/publication.json').read_text(encoding='utf-8'))
require(data['paper']['version']==publication['version'], 'Stale paper version on the website')
require(data['paper']['pages']==publication['pages'], 'Stale paper page count on the website')
require(data['paper']['phaseCoverage']==list(range(17)), 'Paper metadata must cover all detailed phases')
with zipfile.ZipFile(ROOT/'downloads'/publication['archiveFilename']) as research:
    archived_publication=json.loads(research.read('research/publication.json'))
    require(archived_publication==publication, 'Research archive and PDF publication metadata disagree')
    require(all(f'source/PHASE{i}.md' in research.namelist() for i in range(17)),
            'Research archive is missing a detailed phase plan')
for item in data['downloads'] + data['documents']:
    path = artifact(item['url'])
    raw = path.read_bytes()
    require(len(raw) == item['bytes'], f'Wrong file size: {item["url"]}')
    require(hashlib.sha256(raw).hexdigest() == item['sha256'], f'Checksum mismatch: {item["url"]}')
    if path.suffix == '.zip':
        with zipfile.ZipFile(path) as archive:
            require(archive.testzip() is None, f'Damaged archive: {path.name}')
            require(all(not name.startswith('/') and '..' not in PurePosixPath(name).parts
                        for name in archive.namelist()), f'Unsafe archive members: {path.name}')
for phase in data['phases']:
    artifact(phase['document'])

# The current development plan is a separate, changing record from the paper's
# dated evidence. Keep all public copies and the self-contained source bundle in
# agreement, without silently rewriting that scientific publication.
repo = ROOT.parent.parent
backlog = json.loads((repo/'spec/development_backlog.json').read_text(encoding='utf-8'))
status = json.loads((repo/'spec/status.json').read_text(encoding='utf-8'))
development = data['development']
require(development['version'] == backlog['planning_version'], 'Stale development planning version')
require(development['date'] == backlog['date'], 'Stale development planning date')
require(development['readyTickets'] == status['ready_now'], 'Website ready queue differs from current status')
require(development['starterTicketCount'] == len(backlog['starter_tickets']), 'Stale starter ticket count')
require(development['workPackageCount'] == sum(len(p['work_packages']) for p in backlog['phases']),
        'Stale phase work package count')
require(development['seamCount'] == len(backlog['seams']), 'Stale development seam count')
require(any(doc['id'] == 'DEVELOPMENT_SPEC.md' for doc in data['documents']),
        'Development specification is missing from the project library')
require(any(doc['id'] == 'ROADMAP_DIFF.md' for doc in data['documents']),
        'Roadmap audit is missing from the project library')
require((ROOT/'downloads/SimWorld_Development_Specification.md').read_bytes() ==
        artifact(development['document']).read_bytes(), 'Specification download differs from the library')
require(json.loads((ROOT/'downloads/SimWorld_Development_Backlog.json').read_text(encoding='utf-8')) == backlog,
        'Downloadable development backlog differs from the current plan')
with zipfile.ZipFile(ROOT/'downloads/SimWorld_Current_Source.zip') as source:
    required = ['DEVELOPMENT_SPEC.md', 'ROADMAP_DIFF.md', 'scripts/check_development_spec.py',
                'spec/development_backlog.json', 'spec/development_sources.json', 'spec/status.json']
    required += [name for ticket in backlog['starter_tickets'] for name in ticket['files_existing']]
    required += [item['path'] for item in json.loads((repo/'spec/development_sources.json').read_text(encoding='utf-8'))['inputs']]
    require(all('simworld/'+name in source.namelist() for name in required),
            'Source download is missing part of the development specification or its source inputs')
    require(json.loads(source.read('simworld/spec/development_backlog.json')) == backlog,
            'Source download contains a stale development backlog')
    require(json.loads(source.read('simworld/spec/status.json')) == status,
            'Source download contains a stale development status')
catalog=json.loads((ROOT/'data/products.json').read_text(encoding='utf-8'))
require(len(catalog['products'])==12, 'The portfolio should contain twelve complete concepts')
require(data['portfolio']['conceptCount']==len(catalog['products']), 'Portfolio count is stale')
ids=set()
fields=('id','name','category','tagline','audience','problem','experience','output','firstRelease','foundation','validation','format','boundary')
for product in catalog['products']:
    require(all(isinstance(product.get(key),str) and product[key].strip() for key in fields), 'Incomplete product concept')
    require(bool(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',product['id'])), 'Invalid product identifier')
    require(product['id'] not in ids, 'Duplicate product identifier')
    ids.add(product['id'])
    require(product['category'] in ('foundation','physical','worlds'), 'Unknown concept category')
    require(isinstance(product['requirements'],list) and all(isinstance(x,str) and x.strip() for x in product['requirements']), 'Missing capability requirements')
    require(bool(product['phases']) and all(type(n) is int and 0<=n<=16 for n in product['phases']), 'Invalid phase dependency')
require(json.loads((ROOT/'downloads/SimWorld_Product_Portfolio.json').read_text(encoding='utf-8'))==catalog,
        'Downloadable catalog differs from the website')
for path in ROOT.rglob('*'):
    require(not any(part in ('.git', '.runtime', '__pycache__') or part.startswith('.env')
                    for part in path.relative_to(ROOT).parts), f'Private runtime file in artifact: {path}')
print(f'{checks} static website checks passed; {len(data["documents"])} documents, '
      f'{len(data["downloads"])} downloads, 17 phases, {len(catalog["products"])} product concepts.')
