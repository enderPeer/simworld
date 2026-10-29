"""Package current paper sources with separately preserved historical evidence.

Run from a Git checkout. --previous-archive identifies the already-public
research distribution; none of its recorded simulation results are rerun.
"""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import subprocess
import zipfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--previous-archive',type=Path,required=True)
parser.add_argument('--output',type=Path,default=ROOT/'website/dist/downloads/SimWorld_Research_Materials_Public.zip')
args=parser.parse_args()
publication=json.loads((HERE/'publication.json').read_text(encoding='utf-8'))
revision=publication['sourceRevision']

def digest(data):return hashlib.sha256(data).hexdigest()
def encoded(value):return (json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def git(*parts):return subprocess.check_output(['git',*parts],cwd=ROOT)
def source_allowed(name):
    path=PurePosixPath(name)
    if path.parts[0] in ('sim','tests','spec','spikes','docs'):
        return path.suffix in ('.py','.md','.json','.toml','.csv')
    return name in ('README.md','CONTRIBUTING.md','CHANGELOG.md','requirements.txt','ROADMAP.md','BUILD0.md') or (len(path.parts)==1 and name.startswith('PHASE') and path.suffix=='.md')

with zipfile.ZipFile(args.previous_archive) as previous:
    prior={name:previous.read(name) for name in previous.namelist() if not name.endswith('/')}

entries={}
baseline_prefix='baseline_source/' if any(n.startswith('baseline_source/') for n in prior) else 'source/'
for name,raw in prior.items():
    if name.startswith(baseline_prefix):
        entries['baseline_source/'+name[len(baseline_prefix):]]=raw
    elif (name.startswith('research/fresh_m4/') or name.startswith('research/audit_') or
          name in ('research/implementation_audit.txt','research/literature.json')):
        entries[name]=raw
    elif name=='research/roadmap_audit.txt':
        entries['research/historical_roadmap_audit_v1_0.txt']=raw
    elif name=='research/historical_roadmap_audit_v1_0.txt':
        entries[name]=raw
old_manifest=prior.get('research/baseline_source_manifest.json',prior.get('research/source_manifest.json'))
if old_manifest is None:raise ValueError('The previous distribution is missing its source manifest')
entries['research/baseline_source_manifest.json']=old_manifest

source_paths=sorted(p for p in git('ls-tree','-r','--name-only',revision).decode().splitlines() if source_allowed(p))
for name in source_paths:entries['source/'+name]=git('show',f'{revision}:{name}')
manifest={'snapshot_date':publication['date'],'source_revision':revision,'physics_build':'0.1',
          'scope':'Current engine, plans and reader guides at the paper source baseline; historical audit source is separate.',
          'files':[{'path':name,'bytes':len(entries['source/'+name]),'sha256':digest(entries['source/'+name])} for name in source_paths]}
entries['research/source_manifest.json']=encoded(manifest)
entries['research/source_manifest.sha256']=(digest(entries['research/source_manifest.json'])+'\n').encode()

for name in ('manuscript.json','phase_profiles.json','publication_status.json','publication.json','build.py','package.py','requirements.txt','README.md'):
    entries['research/'+name]=(HERE/name).read_bytes()
entries['README.txt']=(
    'SimWorld research white paper v1.1 — 29 October 2026\n\n'
    'source/: current engine and detailed phase plans at '+revision+'.\n'
    'baseline_source/: original public audit source, including archived M3/M4 references.\n'
    'research/: current manuscript, all 17 profiles, renderer, publication status, '
    'current/baseline manifests and preserved original audit evidence.\n\n'
    'Engine: cd source; use Python 3.11.9; pip install -r requirements.txt; python -m pytest -q.\n'
    'Historical diagnostics (from this archive root): python research/audit_diagnostics.py '
    '--source-root baseline_source --output-dir reproduced_audit\n'
    'Paper: install research/requirements.txt, then python research/build.py --output reconstructed.pdf. '
    'See research/README.md for font and visual verification requirements.\n\n'
    'The original simulation measurements were not repeated for this publication revision. '
    'Later Windows/Linux CI results and their URLs are recorded separately. '
    'Preserved historical audit notes describe their original snapshot; current source comments '
    'now explain the same unresolved mechanisms more accurately.\n'
    'The complete repository and published paper are available at https://github.com/enderPeer/simworld '
    'and https://enderpeer.github.io/simworld/.\n').encode('utf-8')
entries['PUBLICATION.txt']=entries['README.txt']

# Validate both source identities before creating the distribution.
for prefix,m in [('source/',manifest),('baseline_source/',json.loads(old_manifest))]:
    for item in m['files']:
        raw=entries[prefix+item['path']]
        assert digest(raw)==item['sha256'], prefix+item['path']
        assert len(raw)==item['bytes'], prefix+item['path']
assert all(f'source/PHASE{i}.md' in entries for i in range(17))
assert 'baseline_source/_m4run/summary.json' in entries
args.output.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(args.output,'w',zipfile.ZIP_DEFLATED) as archive:
    for name,raw in sorted(entries.items()):
        member=zipfile.ZipInfo(name,date_time=(2026,10,29,0,0,0))
        member.compress_type=zipfile.ZIP_DEFLATED
        member.external_attr=0o100644 << 16
        archive.writestr(member,raw)
print(f'Packaged {len(source_paths)} current source files, 17 detailed plans and preserved baseline evidence: {args.output}')
