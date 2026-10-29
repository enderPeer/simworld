import http from 'node:http';
import fs from 'node:fs';
import { promises as fsp } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = await fsp.realpath(path.join(here, 'dist'));
const args = process.argv.slice(2);
const option = (name, fallback) => {
  const i = args.indexOf(name);
  return i === -1 ? fallback : args[i + 1];
};
const port = Number(option('--port', '8787'));
const instance = option('--instance', 'manual');
if (!Number.isInteger(port) || port < 1024 || port > 65535) throw new Error('Invalid port');
if (!/^[A-Za-z0-9-]{1,64}$/.test(instance)) throw new Error('Invalid instance identifier');

const mime = new Map([
  ['.html', 'text/html; charset=utf-8'], ['.css', 'text/css; charset=utf-8'],
  ['.js', 'text/javascript; charset=utf-8'], ['.json', 'application/json; charset=utf-8'],
  ['.md', 'text/plain; charset=utf-8'], ['.txt', 'text/plain; charset=utf-8'],
  ['.xml', 'application/xml; charset=utf-8'], ['.csv', 'text/csv; charset=utf-8'],
  ['.toml', 'text/plain; charset=utf-8'], ['.svg', 'image/svg+xml'],
  ['.png', 'image/png'], ['.jpg', 'image/jpeg'], ['.jpeg', 'image/jpeg'],
  ['.webp', 'image/webp'], ['.ico', 'image/x-icon'], ['.woff2', 'font/woff2'],
  ['.pdf', 'application/pdf'], ['.zip', 'application/zip'],
]);
const securityHeaders = {
  'X-Content-Type-Options': 'nosniff',
  'Referrer-Policy': 'strict-origin-when-cross-origin',
  'X-Frame-Options': 'SAMEORIGIN',
  'Permissions-Policy': 'camera=(), microphone=(), geolocation=()',
  'Content-Security-Policy': "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'; frame-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'self'; form-action 'none'",
};
function reply(res, status, text, method = 'GET', headers = {}) {
  const body = Buffer.from(text);
  res.writeHead(status, { ...securityHeaders, 'Content-Type': 'text/plain; charset=utf-8',
    'Cache-Control': 'no-store', 'Content-Length': body.length, ...headers });
  res.end(method === 'HEAD' ? undefined : body);
}
function isInside(candidate) {
  const relative = path.relative(root, candidate);
  return relative !== '' && !relative.startsWith('..' + path.sep) && relative !== '..' && !path.isAbsolute(relative);
}

const server = http.createServer(async (req, res) => {
  const method = req.method || 'GET';
  try {
    if (!['GET', 'HEAD'].includes(method)) return reply(res, 405, 'Method not allowed\n', method, { Allow: 'GET, HEAD' });
    if (!req.url || req.url.length > 4096) return reply(res, 400, 'Bad request\n', method);
    let pathname;
    try { pathname = decodeURIComponent(req.url.split('?')[0]); }
    catch { return reply(res, 400, 'Bad request\n', method); }
    if (pathname === '/healthz') {
      return reply(res, 200, JSON.stringify({ service: 'simworld-static', status: 'ok', instance }), method,
        { 'Content-Type': 'application/json; charset=utf-8' });
    }
    if (!pathname.startsWith('/') || /[\\\x00-\x1f:]/.test(pathname) || pathname.split('/').some(part => part.startsWith('.'))) {
      return reply(res, 404, 'Not found\n', method);
    }
    if (pathname === '/') pathname = '/index.html';
    if (pathname.endsWith('/')) return reply(res, 404, 'Not found\n', method);
    const candidate = path.resolve(root, '.' + pathname);
    if (!isInside(candidate) || !mime.has(path.extname(candidate).toLowerCase())) return reply(res, 404, 'Not found\n', method);
    let real, stat;
    try {
      real = await fsp.realpath(candidate);
      if (!isInside(real)) return reply(res, 404, 'Not found\n', method);
      stat = await fsp.stat(real);
    } catch { return reply(res, 404, 'Not found\n', method); }
    if (!stat.isFile()) return reply(res, 404, 'Not found\n', method);
    const ext = path.extname(real).toLowerCase();
    const etag = `"${stat.size.toString(16)}-${Math.trunc(stat.mtimeMs).toString(16)}"`;
    const headers = {
      ...securityHeaders, 'Content-Type': mime.get(ext), 'ETag': etag,
      'Last-Modified': stat.mtime.toUTCString(), 'Accept-Ranges': 'bytes',
      'Cache-Control': ['.html', '.json', '.md'].includes(ext) ? 'no-cache' : 'public, max-age=300',
    };
    if (ext === '.zip') headers['Content-Disposition'] = `attachment; filename="${path.basename(real).replace(/[^A-Za-z0-9._-]/g, '_')}"`;
    if (req.headers['if-none-match'] === etag && !req.headers.range) {
      res.writeHead(304, headers); return res.end();
    }
    let start = 0, end = stat.size - 1, status = 200;
    if (req.headers.range && stat.size > 0) {
      const range = /^bytes=(\d*)-(\d*)$/.exec(req.headers.range);
      if (!range || (!range[1] && !range[2])) return reply(res, 416, 'Invalid range\n', method, { 'Content-Range': `bytes */${stat.size}` });
      if (range[1]) { start = Number(range[1]); end = range[2] ? Number(range[2]) : end; }
      else { start = Math.max(0, stat.size - Number(range[2])); }
      if (!Number.isSafeInteger(start) || !Number.isSafeInteger(end) || start > end || start >= stat.size || end < 0) {
        return reply(res, 416, 'Invalid range\n', method, { 'Content-Range': `bytes */${stat.size}` });
      }
      end = Math.min(end, stat.size - 1); status = 206;
      headers['Content-Range'] = `bytes ${start}-${end}/${stat.size}`;
    }
    headers['Content-Length'] = stat.size === 0 ? 0 : end - start + 1;
    res.writeHead(status, headers);
    if (method === 'HEAD' || stat.size === 0) return res.end();
    const stream = fs.createReadStream(real, { start, end });
    stream.on('error', () => res.destroy());
    res.on('close', () => stream.destroy());
    stream.pipe(res);
  } catch (error) {
    console.error(JSON.stringify({ time: new Date().toISOString(), event: 'request_error', code: error.code || 'internal' }));
    if (!res.headersSent) reply(res, 500, 'Server error\n', method);
    else res.destroy();
  }
});
server.requestTimeout = 30000;
server.headersTimeout = 15000;
server.keepAliveTimeout = 5000;
server.on('error', error => { console.error(JSON.stringify({ event: 'server_error', code: error.code })); process.exitCode = 1; });
server.listen(port, '127.0.0.1', () => console.log(JSON.stringify({ event: 'listening', origin: `http://127.0.0.1:${port}`, instance })));
for (const signal of ['SIGINT', 'SIGTERM']) process.on(signal, () => {
  console.log(JSON.stringify({ event: 'stopping', signal }));
  server.close(() => process.exit(0));
  setTimeout(() => process.exit(0), 3000).unref();
});
