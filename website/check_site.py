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


ResourceParser().feed((ROOT / 'index.html').read_text(encoding='utf-8'))
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
for path in ROOT.rglob('*'):
    require(not any(part in ('.git', '.runtime', '__pycache__') or part.startswith('.env')
                    for part in path.relative_to(ROOT).parts), f'Private runtime file in artifact: {path}')
print(f'{checks} static website checks passed; {len(data["documents"])} documents, '
      f'{len(data["downloads"])} downloads, 17 phases.')
