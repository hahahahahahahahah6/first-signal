import copy
import json
import unittest
from unittest.mock import patch
from urllib.error import URLError
from first_signal.agents import Scout, Auditor, Coach, Tracker, audit
from first_signal.github_client import GitHubClient, fixture
from first_signal.scoring import WEIGHTS, RULES, score
from first_signal.server import handle_request

class PipelineTests(unittest.TestCase):
    def test_weights(self):
        self.assertEqual(sum(WEIGHTS.values()), 100)
        for category, weight in WEIGHTS.items():
            self.assertEqual(sum(r[2] for r in RULES if r[1] == category), weight)

    def test_fixture_determinism(self):
        for name, expected in [('strong', 100), ('weak', 10), ('empty', 0)]:
            first = audit(fixture_name=name)
            self.assertEqual(first, audit(fixture_name=name))
            self.assertEqual(first['auditor']['repos'][0]['score'], expected)

    def test_coach_order_and_accounting(self):
        result = audit(fixture_name='weak')
        points = [t['points'] for t in result['coach']['tasks']]
        self.assertEqual(points, sorted(points, reverse=True))
        self.assertEqual(sum(points), 90)
        self.assertTrue(all(t['where'] and t['example'] for t in result['coach']['tasks']))

    def test_tracker_names(self):
        scout = fixture('strong')
        scout['repos'] += fixture('weak')['repos']
        result = Auditor().run(dict(scout, evidence={'source': 'fixture'}))
        tracked = Tracker().run(result, Coach().run(result))
        for repo in scout['repos']:
            self.assertIn(repo['full_name'], tracked['markdown'])

    def test_before_after(self):
        data = copy.deepcopy(fixture('weak'))
        data['repos'][0]['readme'] = True
        self.assertEqual(score(data['repos'][0], data['as_of'])['score'], 35)

    def test_activity_boundaries(self):
        repo = {'full_name': 'x/y', 'pushed_at': '2026-04-29'}
        self.assertEqual(score(repo, '2026-10-26')['breakdown']['recent activity'], 15)
        for value in ['2026-04-28', '2027-01-01', 'bad', None]:
            repo['pushed_at'] = value
            self.assertEqual(score(repo, '2026-10-26')['breakdown']['recent activity'], 0)

    def test_api(self):
        status, mime, body, headers = handle_request('/api/audit?source=fixture:weak')
        self.assertEqual(status, 200)
        self.assertEqual(mime, 'application/json')
        self.assertEqual(json.loads(body)['auditor']['repos'][0]['score'], 10)

    def test_html_export_errors(self):
        self.assertIn('Coach tasks', handle_request('/results?source=fixture:weak')[2])
        result = handle_request('/export?source=fixture:strong')
        self.assertIn('fixture/strong', result[2])
        self.assertIn('PORTFOLIO.md', result[3]['Content-Disposition'])
        for path in ['/api/audit', '/api/audit?source=fixture:no', '/api/audit?source=https://bad']:
            self.assertEqual(handle_request(path)[0], 400)
        self.assertEqual(handle_request('/missing')[0], 404)

    def test_explicit_fallback(self):
        with patch.object(GitHubClient, 'repositories', side_effect=URLError('offline')):
            result = Scout().run(username='octocat', fallback='weak')
            self.assertEqual(result['evidence']['source'], 'fixture')
            self.assertIn('fallback_reason', result['evidence'])
            with self.assertRaises(ValueError):
                Scout().run(username='octocat')

    def test_public_normalization(self):
        responses = [
            [{'full_name': 'a/b', 'html_url': 'https://github.com/a/b'}],
            [{'name': 'tests'}], {'content': 'IyMgRXhhbXBsZQ=='}, [{'name': 'test.yml'}]]
        with patch.object(GitHubClient, 'get', side_effect=responses) as get:
            repo = GitHubClient().repositories('octocat')[0]
            self.assertTrue(repo['readme'] and repo['tests'] and repo['ci'] and repo['showcase'])
            self.assertEqual(get.call_count, 4)

if __name__ == '__main__':
    unittest.main()
