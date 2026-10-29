# White paper sources

This directory contains the reviewed manuscript and detailed phase profiles for the SimWorld white paper. The document version is separate from `physics_build`: publication 1.1 still describes the reduced physics build 0.1.

- `manuscript.json` is the editable text, tables, and page structure.
- `phase_profiles.json` records the detailed synthesis of phases 0–16.
- `publication_status.json` identifies the source commit, CI evidence, dependency ledger, and scope of the claims.
- `publication.json` identifies the published PDF and research archive.
- `build.py` renders the PDF with ReportLab.
- `package.py` creates the research archive while retaining the original audit evidence.

From the repository root, install the separate authoring dependencies and render:

```sh
python -m pip install -r research/whitepaper/requirements.txt
python research/whitepaper/build.py
```

The default output is `output/whitepaper/SimWorld_Research_White_Paper.pdf`. The published layout uses Windows Times New Roman and Arial. `--font-dir` selects a directory containing those fonts; on Linux the renderer also supports the system Liberation Serif/Sans directory. Different fonts can change pagination, so render and inspect every page before publication.

The website build intentionally does not render or revise the paper. After reviewing a new PDF, update its publication metadata and the research archive, copy the verified PDF to `website/dist/downloads/SimWorld_Research_White_Paper.pdf`, then run:

```sh
python website/build_content.py
python website/check_site.py
```

Keep historical measurements attributed to their original experiment. A passing CI run on two platforms is not a direct comparison of their complete state hashes. A new detailed phase plan is not an implemented capability. Never replace the original audit evidence with newly generated data without recording a new experiment and its provenance.
