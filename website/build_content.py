"""Build public site data from repository sources and archived public evidence.

Run with a stock Python 3.11+ interpreter. The dated PDF and public research ZIP
in dist/downloads are immutable publication inputs; generated current-source and
documentation archives are deterministic outputs. No local audit/tmp folder,
user configuration or network access is needed, including in GitHub Actions.
"""
from pathlib import Path
import hashlib, json, re, zipfile, xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'website/dist'
DATA=DIST/'data'; DOCS=DIST/'docs'; DOWNLOADS=DIST/'downloads'
for p in [DATA,DOCS,DOWNLOADS]:p.mkdir(parents=True,exist_ok=True)
AUDIT_DATE='2026-10-29'
REPOSITORY_URL='https://github.com/enderPeer/simworld'
SITE_URL='https://enderpeer.github.io/simworld/'
PAPER=json.loads((ROOT/'research/whitepaper/publication.json').read_text(encoding='utf-8'))
# Keep the no-JavaScript fallback and browser cache keys aligned with the PDF.
index_path=DIST/'index.html'
index_text=index_path.read_text(encoding='utf-8')
index_text=re.sub(r'(<strong id="paper-page-count">)\d+',lambda m:m[1]+str(PAPER['pages']),index_text)
index_text=re.sub(r'(<meta name="simworld-paper-version" content=")[^"]+',lambda m:m[1]+PAPER['version'],index_text)
index_path.write_text(index_text,encoding='utf-8')


def write_archive(path, entries):
    """Stable ordering and timestamps make checksums repeat across clean builds."""
    with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for name, content in sorted(entries.items()):
            member=zipfile.ZipInfo(name, date_time=(2026,10,29,0,0,0))
            member.compress_type=zipfile.ZIP_DEFLATED
            member.external_attr=0o100644 << 16
            archive.writestr(member, content)

def clean_text(text):
    # Local machine identity contributes nothing to public scientific evidence.
    for src,dst in [(str(ROOT),'<SOURCE_ROOT>'),(ROOT.as_posix(),'<SOURCE_ROOT>'),
                    (str(Path.home()),'<USER_HOME>'),(Path.home().as_posix(),'<USER_HOME>')]:
        text=text.replace(src,dst)
    text=re.sub(r'DESKTOP-[A-Z0-9]+','REDACTED_HOST',text)
    text=re.sub(r'\(this box,\s*[^)]+\)', '(recorded development host)', text)
    return text

def clean_obj(obj):
    if isinstance(obj,dict):
        return {k:('python' if k=='executable' else clean_obj(v)) for k,v in obj.items() if k!='hostname'}
    if isinstance(obj,list):return [clean_obj(v) for v in obj]
    if isinstance(obj,str):return clean_text(obj)
    return obj

def public_bytes(name,raw):
    ext=Path(name).suffix.lower()
    if ext=='.json':
        return (json.dumps(clean_obj(json.loads(raw.decode('utf-8'))),ensure_ascii=False,indent=2)+'\n').encode()
    if ext=='.xml':
        tree=ET.fromstring(raw)
        for el in tree.iter():
            el.attrib.pop('hostname',None)
            for k,v in list(el.attrib.items()):el.attrib[k]=clean_text(v)
        return ET.tostring(tree,encoding='utf-8',xml_declaration=True)
    if ext in {'.md','.txt','.py','.toml','.csv','.sha256'}:
        return clean_text(raw.decode('utf-8')).encode()
    return raw

def sha(data):return hashlib.sha256(data).hexdigest()
def write_json(path,obj):path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Proposed products are an authored catalog, separate from measured model results.
products=json.loads((ROOT/'website/content/products.json').read_text(encoding='utf-8'))
write_json(DATA/'products.json',products)
write_json(DOWNLOADS/'SimWorld_Product_Portfolio.json',products)

phase_rows=[
 (0,'World rules','Foundations','Define the primitive records, effective fields, initial state, time and observation contracts.',
  ['Sampled quant records and field metadata','Deterministic events and state hashes','Restricted quiet-cell jumps'],
  ['A reproducible cooling-seed demonstration','Explicit state and event invariants','Measured cost and declared approximation limits']),
 (1,'Quantum layer','Foundations','Develop field dynamics, quantum observables and observation interfaces beyond the reduced seed.',
  ['Array-based state and field kernels','Interference and entanglement representations','Tiered scheduling and observation maps'],
  ['Interference and non-signalling controls','Spectral and stochastic benchmarks','Reproducibility across supported environments']),
 (2,'Nuclear layer','Matter','Compute nuclear structure, reactions, decay and energy deposition from effective physical models.',
  ['Residual-force and Coulomb kernels','Fusion, fission and decay channels','Recomputable nuclide registry'],
  ['Held-out binding and yield comparisons','Conservation across reaction events','Closed decay pathways and validated rates']),
 (3,'Atomic layer','Matter','Derive electronic properties and spectra rather than enumerate element behavior.',
  ['Radial self-consistent-field solver','Ionization, affinity and spectra','Cached atomic calculations with provenance'],
  ['Numerical refinement convergence','Independent atomic benchmarks','Atomic approximations suitable for chemistry']),
 (4,'Chemistry','Matter','Build molecular structure and reaction discovery from atomic models.',
  ['Bond-energy and geometry calculations','Reaction-channel and barrier search','Surface, polymer and catalytic chemistry'],
  ['Molecular energetics and geometry','Reversible kinetics and equilibrium checks','Conserved material in controlled reactors']),
 (5,'Materials and substances','Matter','Connect composition and processing history to bulk properties.',
  ['Microstructure and bounded history records','Mechanical and transport properties','Phase-change and constitutive models'],
  ['Material-property and hysteresis benchmarks','Process-dependent behavior','Measured reconstruction and closure error']),
 (6,'Continuum physics','World','Couple mechanics, heat, fluids, radiation and electromagnetism.',
  ['Conservative transport and gravity','Stress, fracture and heat transfer','Radiation and electromagnetic operators'],
  ['Convergence and conservation tests','Orbit, convection and wave benchmarks','Energy and entropy accounting in devices']),
 (7,'Planet and space','World','Model planetary environments, stellar inputs and geological change.',
  ['Accretion and differentiation','Climate, water and reservoir cycles','Stellar summaries and spatial refinement'],
  ['Closed planetary resource budgets','Long-time numerical stability','Detailed-versus-compressed comparisons']),
 (8,'Life and ecosystems','Life','Explore whether chemistry supports persistent, heritable and evolving systems.',
  ['Templating and catalytic networks','Compartments and metabolism','Genotype populations and ecological feedback'],
  ['Persistence with resource controls','Heritable variation and competition','Energy closure and population agreement']),
 (9,'Agency and civilization','Life','Connect learned behavior and physical bodies to tools and cumulative culture.',
  ['Sensory and learned action policies','Articulated bodies and tool use','Culture and demographic summaries'],
  ['Novel-resource and tool tasks','Energetic viability','Controlled tests of cumulative learning']),
 (10,'Technology and knowledge','Society','Let agents experiment, communicate and assemble physical technologies.',
  ['Claims, experiments and replication','Machines, grids and communication','Computation and nested simulation contracts'],
  ['Physical energy and signal tests','Recorded endogenous discovery','Reproducible computation and nested histories']),
 (11,'People and society','Society','Study communication, institutions, education and collective behavior.',
  ['Sanction and coalition networks','Language, learning and knowledge transmission','Social and cultural summaries'],
  ['Matched interventions across communities','Distributional outcomes across seeds','Measured social-compression error']),
 (12,'Money and politics','Society','Represent ownership, obligations, exchange and governance over physical resources.',
  ['Ownership and transfer events','Credit, repayment and enforcement','Information diffusion and political coordination'],
  ['Holdings survive compression','Real and nominal accounting remain distinct','Conditional institutional tests without fixed outcomes']),
 (13,'Infrastructure and externalities','Society','Connect owned infrastructure, industrial flows, exposure and responsibility.',
  ['Terrain-aware networks and maintenance histories','Producer-attributed emissions and local tracers','Supply, recycling, hazards and liability records'],
  ['Material-flow and attribution closure','Maintenance-dependent failure comparisons','Recovery retains physical transport delays']),
 (14,'Perception and detail','Integration','Make observation, memory and simulation resolution explicit, reproducible contracts.',
  ['Agent-derived gaze and observation maps','Memory and testimony with provenance','Deterministic frame budgets and resolution governor'],
  ['Probe-fixture equivalence where maps agree','Consistent physical and knowledge records','Measured cost reduction at declared epistemic parity']),
 (15,'Runtime and scalability','Integration','Measure and optimize the full hierarchy across hardware and time scales.',
  ['Data-oriented storage','Heterogeneous tick rates and CPU/GPU work','Measured memory, logging and reconstruction cost'],
  ['Workload scaling at declared fidelity','Reproducible scheduling policy','Fidelity-versus-cost curves']),
 (16,'The integrated emergent loop','Integration','Test a persistent history with endogenous innovation across the hierarchy.',
  ['Continuous causal provenance','Audited transfers between scales','Playable exploration and observation'],
  ['Disclose every seed and approximation','Document both successful and failed emergence','Verify each interface before end-to-end claims'])
]
phases=[]
for i,title,group,summary,mechanisms,criteria in phase_rows:
    available=(ROOT/f'PHASE{i}.md').exists()
    phases.append({'id':i,'title':title,'group':group,
      'status':'implemented-baseline' if i==0 else ('detailed-proposal' if available else 'roadmap-only'),
      'statusLabel':'Reduced baseline built' if i==0 else ('Detailed research plan' if available else 'Roadmap vision'),
      'summary':summary,'mechanisms':mechanisms,'criteria':criteria,
      'document':f'/docs/PHASE{i}.md' if available else '/docs/ROADMAP.md',
      'documentAvailable':available,
      'implementationNote':'A reduced Phase 0 micro-seed exists; this does not establish all world-rule ambitions.' if i==0 else
       ('The baseline contains a simplified precursor; this full phase is not implemented.' if i in [1,2,3] else 'Proposed research; not implemented in the current sim package.')})

detailed_phases=[phase['id'] for phase in phases if phase['documentAvailable']]
outline_phases=[phase['id'] for phase in phases if not phase['documentAvailable']]
detailed_label=', '.join(str(i) for i in detailed_phases)
if detailed_phases == list(range(len(detailed_phases))):
    detailed_label=f'0–{detailed_phases[-1]}'
coverage_note=f'Detailed phase plans cover {detailed_label}.'
if outline_phases:
    coverage_note+=' '+('Phase ' if len(outline_phases)==1 else 'Phases ')+', '.join(map(str,outline_phases))+' '+('is a roadmap outline.' if len(outline_phases)==1 else 'are roadmap outlines.')
else:
    coverage_note+=' All seventeen phases have detailed plans; implementation status is separate.'

docs=[]
doc_paths=[ROOT/'ROADMAP.md',ROOT/'BUILD0.md']+[ROOT/f'PHASE{i}.md' for i in range(17) if (ROOT/f'PHASE{i}.md').exists()]+sorted((ROOT/'spec').glob('*.md'))
for p in doc_paths:
    rel=p.relative_to(ROOT)
    dest=DOCS/rel;dest.parent.mkdir(parents=True,exist_ok=True)
    payload=public_bytes(rel.name,p.read_bytes());dest.write_bytes(payload)
    title=payload.decode().splitlines()[0].lstrip('# ').strip()
    category='Roadmap' if p.name=='ROADMAP.md' else 'Build specification' if p.name=='BUILD0.md' else 'Phase plan' if p.name.startswith('PHASE') else 'Specifications'
    docs.append({'id':rel.as_posix(),'title':title,'category':category,'url':'/docs/'+rel.as_posix(),
                 'bytes':len(payload),'sha256':sha(payload)})

pdf=DOWNLOADS/'SimWorld_Research_White_Paper.pdf'
research_archive=DOWNLOADS/'SimWorld_Research_Materials_Public.zip'
for publication_input in [pdf,research_archive]:
    if not publication_input.is_file():
        raise FileNotFoundError(f'Missing committed publication input: {publication_input.relative_to(ROOT)}')
assert sha(pdf.read_bytes())==PAPER['pdfSha256'], 'PDF and publication metadata disagree'
assert pdf.stat().st_size==PAPER['pdfBytes'], 'PDF size and publication metadata disagree'
# Read the public snapshot without rewriting it: the paper's historical evidence
# must not silently become a new measurement when the current source changes.
with zipfile.ZipFile(research_archive) as archive:
    evidence={name:archive.read(name) for name in archive.namelist() if name.startswith('research/')}

patterns=['README.md','CONTRIBUTING.md','docs/*.md','ROADMAP.md','BUILD0.md','PHASE*.md','requirements.txt','sim/*.py','spec/*.md',
          'tests/*.py','tests/*.toml','tests/oracle/*.json','tests/oracle/*.py',
          'spikes/*/*.py','spikes/*/*.json','spikes/*/*.csv']
current_files=sorted({p for pat in patterns for p in ROOT.glob(pat) if p.is_file()})
current={p.relative_to(ROOT).as_posix():public_bytes(p.name,p.read_bytes()) for p in current_files}
current_manifest={'snapshot_date':'2026-10-29','physics_build':'0.1',
   'scope':'Current allowlisted engine source and research plans; public identifiers redacted',
   'repository':REPOSITORY_URL,'detailed_phases':detailed_phases,
   'files':[{'path':name,'bytes':len(raw),'sha256':sha(raw)} for name,raw in current.items()]}
source_package={'simworld/'+name:raw for name,raw in current.items()}
source_package['simworld/public_source_manifest.json']=(json.dumps(current_manifest,indent=2)+'\n').encode()
source_package['simworld/PUBLIC_README.txt']=('SimWorld engine source and documentation snapshot.\n'
      +coverage_note+' '
      'The implemented engine remains the reduced physics_build 0.1 baseline.\n'
      'Use Python 3.11.9; install requirements.txt, run python -m pytest -q, then '
      'python -m sim.demo --seed 42 --ticks 3400 --cells 8 --probe-cells 2,3 --out run_demo.\n'
      'The complete repository, including website tooling, is '+REPOSITORY_URL+'.\n'
      'No software license has been selected; public availability does not itself grant a license.\n').encode()
write_archive(DOWNLOADS/'SimWorld_Current_Source.zip',source_package)
write_archive(DOWNLOADS/'SimWorld_Documentation.zip',
              {p.relative_to(ROOT).as_posix():public_bytes(p.name,p.read_bytes()) for p in doc_paths})

for source,target in [('research/fresh_m4/summary.json','SimWorld_Verified_Run.json'),
                      ('research/audit_tests.xml','SimWorld_Test_Report.xml'),
                      ('research/audit_diagnostics.json','SimWorld_Audit_Diagnostics.json')]:
    (DOWNLOADS/target).write_bytes(public_bytes(source,evidence[source]))

download_meta=[
 ('whitepaper','Research white paper',f"Version {PAPER['version']} · {PAPER['pages']} pages. Detailed profiles of all 17 phases, latest project status, implementation evidence and research limits.",pdf.name,'PDF'),
 ('research','Research materials',f"Version {PAPER['version']} manuscript, all 17 phase profiles, current source snapshot and CI evidence, plus the separately preserved original audit.",'SimWorld_Research_Materials_Public.zip','ZIP'),
 ('portfolio','Possible product portfolio','Twelve proposed products, with intended users, first scopes, dependencies and validation gates. These are concepts, not shipping products.','SimWorld_Product_Portfolio.json','JSON'),
 ('source','Current engine source','Python engine, tests, prototypes, contributor documentation and all currently available phase plans.','SimWorld_Current_Source.zip','ZIP'),
 ('documentation','Complete documentation','Roadmap, first-build contract, all available phase plans and specification records.','SimWorld_Documentation.zip','ZIP'),
 ('run','Verified run data','Full-precision summary of the reproduced seed-42, eight-cell, 3,400-tick realization.','SimWorld_Verified_Run.json','JSON'),
 ('tests','Full test report','JUnit results for the 65-test audit suite. Host identifiers removed.','SimWorld_Test_Report.xml','XML'),
 ('diagnostics','Audit diagnostics','Reproduction results and targeted checks of reverse pathways, neutral-state behavior and RNG stream reuse.','SimWorld_Audit_Diagnostics.json','JSON')]
downloads=[]
for ident,title,description,name,fmt in download_meta:
    raw=(DOWNLOADS/name).read_bytes()
    suffix='?v='+PAPER['version'] if ident in ('whitepaper','research') else ''
    downloads.append({'id':ident,'title':title,'description':description,'filename':name,
                      'url':'/downloads/'+name+suffix,'format':fmt,'bytes':len(raw),'sha256':sha(raw)})
write_json(DATA/'downloads.json',downloads)

literature=json.loads(evidence['research/literature.json'])['references']
references=[{'id':r['id'],'title':r['title'],'authors':r['authors'],'year':r['year'],
             'venue':r['venue'],'url':'https://doi.org/'+r['doi'],'topic':r['use']} for r in literature]
seams=(ROOT/'spec/seams.md').read_text(encoding='utf-8')
seam_rows=[l for l in seams.splitlines() if re.match(r'\| S\d+ \|',l)]
open_seams=sum(l.rstrip().endswith('OPEN |') for l in seam_rows)
summary=json.loads(evidence['research/fresh_m4/summary.json'])
project={
 'name':'SimWorld','tagline':'A world built from consequences.',
 'description':'A research project exploring how physical processes, life, learning and institutions might connect through one reproducible simulated history.',
 'snapshotDate':AUDIT_DATE,'physicsBuild':'0.1','status':'Research prototype',
 'repositoryURL':REPOSITORY_URL,'websiteURL':SITE_URL,
 'portfolio':{'url':'portfolio.html','conceptCount':len(products['products']),'version':products['version']},
 'statusDescription':'The current build is a reduced stochastic physics model. The wider world remains a research program.',
 'paper':{**PAPER,'url':'/downloads/'+pdf.name+'?v='+PAPER['version']},
 'metrics':{'testsPassed':65,'testSeconds':123.64,'replayHashes':34,'seed':42,'cells':8,'ticks':3400,
            'phaseCount':17,'detailedPhasePlans':len(detailed_phases),'documents':len(docs),'references':len(references),
            'openSeams':open_seams,'totalSeams':len(seam_rows),'Yp':summary['Y_p'],
            'Xe':summary['X_e'],'nucleons':summary['nucleons'],'reactions':summary['reactions'],
            'finalHash':summary['final_hash']},
 'principles':[
   {'title':'Computed consequences','text':'Properties should follow from explicit models and interactions, with fitted assumptions and missing mechanisms disclosed.'},
   {'title':'A traceable history','text':'Seeded events, recorded causes and state hashes make each experiment inspectable and repeatable.'},
   {'title':'Evidence before scale','text':'The roadmap expands through tested interfaces, independent benchmarks and measured approximation errors.'}],
 'implemented':[
   {'title':'Cooling micro-seed','text':'Eight-cell thermal populations with prescribed expansion, effective nucleon formation, nuclear reactions and electron capture.'},
   {'title':'Deterministic replay','text':'A fresh seed-42 run reproduced the archived result and all 34 hashes in the audited environment.'},
   {'title':'Inspectable experiments','text':'The Python implementation, 65-test suite, prototype reports and full-precision audit evidence are downloadable.'}],
 'findings':[
   {'title':'Repeatable does not mean physically validated','text':'The green suite verifies existing regression criteria. Broad fitted bands do not establish precision cosmology.'},
   {'title':'Reverse kinetics need further work','text':'Diagnostics found missing nuclear reverse-path reachability and an absorbing fully neutral atomic state.'},
   {'title':'Random-stream identity needs refinement','text':'Repeated calls at the same stream coordinates reuse prefixes, even when their payloads differ.'},
   {'title':'Prototype speed is not engine speed','text':'The array microbenchmark and the dictionary-backed main engine use different storage. Their throughput cannot be equated.'}],
 'researchQuestions':[
   'Can reversible kernels reach the same equilibrium from both directions?',
   'What information must survive compression for later predictions to remain reliable?',
   'Can independent physical mechanisms be coupled without losing conservation or provenance?',
   'Which higher-level patterns survive changes in seeds, parameters and environments?'],
 'provenance':{'note':'All reported implementation results refer to the 29 October 2026 audit of physics_build 0.1. Future-phase gates and scale targets are proposals, not achieved capabilities.',
   'currentDocumentation':coverage_note,
   'snapshotDifference':PAPER['snapshotNote'],
   'publicDistribution':'Public download archives remove workstation identifiers and include manifests for the distributed bytes.'},
 'phases':phases,'documents':docs,'downloads':downloads,'references':references,
 'reproduce':{'commands':['python -m pip install -r requirements.txt','python -m pytest -q','python -m sim.demo --seed 42 --ticks 3400 --cells 8 --probe-cells 2,3 --out run_demo','python -m sim.replay run_demo'],
              'environment':'Python 3.11.9 · NumPy 2.4.6 · pytest 9.1.1',
              'scope':'Exact reproduction is established for the audited machine and source environment; cross-platform equivalence requires separate testing.'}
}
write_json(DATA/'project.json',project)
(DIST/'.nojekyll').write_text('',encoding='utf-8')

# Version page assets by their bytes and datasets by the combined public content.
# A product or website edit can now invalidate caches without changing the paper.
content_version=sha((DATA/'project.json').read_bytes()+(DATA/'products.json').read_bytes())[:12]
def version_asset(match):
    name=match['name']
    asset=DIST/name
    if not asset.is_file():raise FileNotFoundError(f'Missing page asset: {name}')
    return match['prefix']+name+'?v='+sha(asset.read_bytes())[:12]+'"'
for page in DIST.glob('*.html'):
    page_text=page.read_text(encoding='utf-8')
    metadata=f'<meta name="simworld-content-version" content="{content_version}">'
    if 'name="simworld-content-version"' in page_text:
        page_text=re.sub(r'<meta name="simworld-content-version" content="[^"]*">',metadata,page_text)
    else:page_text=page_text.replace('</head>','  '+metadata+'\n</head>')
    page_text=re.sub(r'(?P<prefix>(?:src|href)=")(?P<name>[^":?#]+\.(?:js|css))(?:\?[^"]*)?"',version_asset,page_text)
    page.write_text(page_text,encoding='utf-8')

# Verify public archives contain no private host paths and every published source
# manifest hashes the actual public bytes. Use strict checks on decoded text.
for p in [*DOCS.rglob('*.md'),*DATA.glob('*.json'),*DOWNLOADS.glob('*.json'),*DOWNLOADS.glob('*.xml')]:
    text=p.read_text(encoding='utf-8')
    assert not re.search(r'C:(?:\\\\|\\|/)Users(?:\\\\|\\|/)',text),p
    assert not re.search(r'DESKTOP-[A-Z0-9]+',text),p
for p in DOWNLOADS.glob('*.zip'):
    with zipfile.ZipFile(p) as z:
        assert z.testzip() is None,p
        for name in z.namelist():
            if Path(name).suffix in {'.json','.xml','.txt','.md','.py','.toml','.csv'}:
                text=z.read(name).decode('utf-8')
                assert not re.search(r'C:(?:\\\\|\\|/)Users(?:\\\\|\\|/)',text),(p,name)
                assert not re.search(r'DESKTOP-[A-Z0-9]+',text),(p,name)
print(json.dumps({'phases':len(phases),'detailedPhasePlans':len(detailed_phases),'documents':len(docs),
  'downloads':len(downloads),'seams':len(seam_rows),'openSeams':open_seams,
  'status':'content built and public identifier checks passed'},indent=2))
