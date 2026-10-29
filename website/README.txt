SIMWORLD PUBLIC WEBSITE

PRIMARY HOSTING
  https://enderpeer.github.io/simworld/

GitHub Pages serves the public site independently of this computer. Pushes to
main rebuild, validate, and publish website/dist through .github/workflows/pages.yml.
Read README.md in this folder for the complete website editing guide.

REBUILD AND VALIDATE (from the repository root)
  python website/build_content.py
  python website/check_site.py

The builder reads committed public research assets and current source documents.
It does not require private authoring folders or a local Cloudflare process.

OPTIONAL LOCAL CLOUDFLARE SHARING

The public files are in dist/. The server serves only dist/, never the parent
project folder, local scripts, logs, credentials, or the runtime directory.

START (PowerShell, from the project folder)
  powershell -NoProfile -ExecutionPolicy Bypass -File .\website\start.ps1

The script starts Node and cloudflared in hidden windows and prints a free
https://...trycloudflare.com URL. This URL is temporary, may change when the
tunnel restarts, and works only while both processes and this computer stay on.
The script reuses the recorded running site instead of starting duplicates.
It normally uses http://127.0.0.1:8787, or the next free port.

STOP
  powershell -NoProfile -ExecutionPolicy Bypass -File .\website\stop.ps1

Only processes with the recorded executable path AND creation time are stopped.
No Windows service, login settings, scheduled task, or DNS record is created.

LOGS AND STATE
  website/.runtime/runtime.json
  website/.runtime/server.out.log and server.err.log
  website/.runtime/tunnel.out.log and tunnel.err.log

These files are local-only. A URL being printed means Cloudflare issued an
address; check that address in a browser before considering publication verified.
This optional tunnel is separate from the persistent GitHub Pages address above.

Requirements: Node.js and cloudflared available on PATH. You may pass explicit
-NodePath and -CloudflaredPath to start.ps1. All website code is buildless.

SERVER CHECKS
  node --check .\website\server.mjs
  http://127.0.0.1:<port>/healthz

The server accepts GET/HEAD, supports PDF byte ranges, blocks hidden paths and
parent traversal, rejects files outside dist/ including symlink escapes, and
does not produce directory listings.
