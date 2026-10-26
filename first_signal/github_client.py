"""Bounded, unauthenticated public GitHub reads using urllib only."""
import base64
import json
import re
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from pathlib import Path
FIXTURES = Path(__file__).resolve().parent.parent / 'tests' / 'fixtures'

class GitHubClient:
    def get(self, path):
        req = Request('https://api.github.com' + path,
                      headers={'User-Agent': 'FirstSignal/1.0', 'Accept': 'application/vnd.github+json'})
        with urlopen(req, timeout=15) as response:
            return json.load(response)

    def optional(self, path, empty):
        try:
            return self.get(path)
        except HTTPError as exc:
            if exc.code == 404:
                return empty
            raise

    def repositories(self, username, limit=3):
        if not re.fullmatch(r'[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?', username):
            raise ValueError('Enter a GitHub username, not a URL.')
        if not 1 <= limit <= 3:
            raise ValueError('Repository limit must be 1–3.')
        repos = self.get('/users/' + username + '/repos?sort=pushed&per_page=' + str(limit))
        result = []
        for repo in repos:
            prefix = '/repos/' + repo['full_name']
            contents = self.optional(prefix + '/contents', [])
            names = {entry['name'].lower() for entry in contents}
            readme = self.optional(prefix + '/readme', {})
            body = base64.b64decode(readme.get('content', '')).decode('utf-8', errors='replace')
            workflows = self.optional(prefix + '/contents/.github/workflows', [])
            result.append(dict(full_name=repo['full_name'], html_url=repo['html_url'],
                description=repo.get('description'), topics=repo.get('topics', []),
                license=repo.get('license'), pushed_at=repo.get('pushed_at'),
                homepage=repo.get('homepage'), readme=bool(body.strip()),
                tests=any(n in names for n in ('tests', 'test', 'pytest.ini', 'tox.ini')),
                ci=any(e['name'].endswith(('.yml', '.yaml')) for e in workflows),
                showcase=any(token in body.lower() for token in ('## example', '![', '## demo'))))
        return result

def fixture(name):
    if name not in ('strong', 'weak', 'empty'):
        raise ValueError('Fixture must be strong, weak or empty.')
    return json.loads((FIXTURES / (name + '.json')).read_text())
