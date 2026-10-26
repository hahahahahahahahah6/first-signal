"""Local stdlib HTTP UI. Every result carries its evidence source."""
import argparse
import html
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlencode, urlsplit
from .agents import audit

FORM = '''<h1>FirstSignal</h1><p>Public portfolio evidence, not a hiring prediction or job offer.</p>
<form action="/results"><label>GitHub username or fixture:strong, fixture:weak, fixture:empty
<input name="source" value="fixture:weak" required maxlength="80"></label><button>Audit</button></form>'''

def audit_query(query):
    source = query.get('source', [''])[0].strip()
    if source.startswith('fixture:'):
        return audit(fixture_name=source.split(':', 1)[1])
    return audit(username=source)

def render(result, source):
    esc = html.escape
    output = [FORM, '<h2>Results</h2><p>Evidence: ' + esc(json.dumps(result['auditor']['evidence'])) + '</p>']
    for repo in result['auditor']['repos']:
        output.append('<h3>{}: {}/100</h3><table><tr><th>Category</th><th>Points</th></tr>'.format(esc(repo['name']), repo['score']))
        for key, value in repo['breakdown'].items():
            output.append('<tr><td>{}</td><td>{}</td></tr>'.format(esc(key), value))
        output.append('</table><details><summary>Rule evidence</summary><pre>' + esc(json.dumps(repo['evidence'], indent=2)) + '</pre></details>')
    output.append('<h2>Coach tasks</h2><ol>')
    for task in result['coach']['tasks']:
        output.append('<li><label><input type="checkbox">{} (+{}): {}</label><pre>{}</pre></li>'.format(esc(task['repo']), task['points'], esc(task['where']), esc(task['example'])))
    output += ['</ol>', '<a href="/export?' + esc(urlencode({'source': source}), quote=True) + '">Download PORTFOLIO.md</a>']
    return ''.join(output)

def handle_request(target):
    """Pure request routing, also exercised without sockets in unit tests."""
    url = urlsplit(target)
    if url.path == '/':
        return 200, 'text/html; charset=utf-8', FORM, {}
    if url.path not in ('/api/audit', '/results', '/export'):
        return 404, 'text/plain; charset=utf-8', 'Not found', {}
    query = parse_qs(url.query)
    try:
        result = audit_query(query)
    except ValueError as exc:
        return 400, 'application/json', json.dumps({'error': str(exc)}), {}
    if url.path == '/api/audit':
        return 200, 'application/json', json.dumps(result), {}
    if url.path == '/export':
        return 200, 'text/markdown; charset=utf-8', result['tracker']['markdown'], {'Content-Disposition': 'attachment; filename="PORTFOLIO.md"'}
    return 200, 'text/html; charset=utf-8', render(result, query['source'][0]), {}

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        status, mime, body, headers = handle_request(self.path)
        if mime.startswith('text/html'):
            body = '<!doctype html><html lang="en"><meta charset="utf-8"><title>FirstSignal</title><main>' + body + '</main></html>'
        data = body.encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', mime)
        self.send_header('Content-Length', str(len(data)))
        self.send_header('X-Content-Type-Options', 'nosniff')
        for key, value in headers.items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(data)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    with ThreadingHTTPServer((args.host, args.port), Handler) as server:
        print('FirstSignal: http://{}:{}'.format(args.host, args.port), flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass

if __name__ == '__main__':
    main()
