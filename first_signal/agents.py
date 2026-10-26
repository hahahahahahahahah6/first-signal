"""Four deterministic agents, each with explicit evidence."""
from datetime import date
from urllib.error import URLError
from .github_client import GitHubClient, fixture
from .scoring import score

class Scout:
    def run(self, username=None, fixture_name=None, fallback=None):
        if bool(username) == bool(fixture_name):
            raise ValueError('Provide exactly one username or fixture.')
        if fixture_name:
            data = fixture(fixture_name)
            return dict(repos=data['repos'], as_of=data['as_of'],
                        evidence={'source': 'fixture', 'fixture': fixture_name})
        try:
            repos = GitHubClient().repositories(username)
            return dict(repos=repos, as_of=date.today().isoformat(),
                        evidence={'source': 'real-API', 'username': username, 'limit': 3})
        except (URLError, TimeoutError, OSError) as exc:
            if not fallback:
                raise ValueError('GitHub unavailable; use --fixture or --fallback-fixture. ' + str(exc)) from exc
            data = self.run(fixture_name=fallback)
            data['evidence']['fallback_reason'] = str(exc)
            data['evidence']['requested_username'] = username
            return data

class Auditor:
    def run(self, scout):
        repos = [score(repo, scout['as_of']) for repo in scout['repos']]
        return dict(repos=repos, evidence={'rubric': 'v1', 'as_of': scout['as_of'],
                    'source': scout['evidence'], 'repo_count': len(repos)})

class Coach:
    def run(self, audit):
        tasks = [dict(repo=repo['name'], rule=e['rule'], points=e['maximum']-e['earned'],
                      where=e['instruction'], example=e['example'])
                 for repo in audit['repos'] for e in repo['evidence'] if e['earned'] < e['maximum']]
        tasks.sort(key=lambda t: (-t['points'], t['repo'], t['rule']))
        return dict(tasks=tasks, evidence={'ordering': 'points descending, repository, rule',
                                         'recoverable_points': sum(t['points'] for t in tasks)})

class Tracker:
    def run(self, audit, coach):
        lines = ['# Portfolio', '', 'Public repository evidence; not a hiring prediction or job offer.', '']
        for repo in audit['repos']:
            lines += ['## ' + repo['name'], '', 'Score: {}/100'.format(repo['score']), repo['url'], '']
        lines += ['## Improvement checklist', '']
        lines += ['- [ ] {} (+{}): {}. Example: {}'.format(t['repo'], t['points'], t['where'], t['example'].replace('\n', ' ')) for t in coach['tasks']]
        return dict(markdown='\n'.join(lines) + '\n', evidence={'repo_names': [r['name'] for r in audit['repos']], 'tasks': len(coach['tasks'])})

def audit(username=None, fixture_name=None, fallback=None):
    scout = Scout().run(username, fixture_name, fallback)
    auditor = Auditor().run(scout)
    coach = Coach().run(auditor)
    tracker = Tracker().run(auditor, coach)
    return dict(scout=scout, auditor=auditor, coach=coach, tracker=tracker)
