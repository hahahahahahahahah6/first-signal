import argparse
import json
from pathlib import Path
from .agents import audit

def main():
    parser = argparse.ArgumentParser(description='Audit public portfolio evidence, not hiring potential.')
    parser.add_argument('--username')
    parser.add_argument('--fixture', action='append', choices=['strong', 'weak', 'empty'])
    parser.add_argument('--fallback-fixture', choices=['strong', 'weak', 'empty'])
    parser.add_argument('--export', type=Path, help='Write PORTFOLIO.md; one audit only')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    if bool(args.username) == bool(args.fixture):
        parser.error('Choose --username or one or more --fixture options.')
    if args.export and len(args.fixture or [None]) != 1:
        parser.error('--export requires one audit.')
    try:
        results = [audit(args.username, name, args.fallback_fixture) for name in (args.fixture or [None])]
    except ValueError as exc:
        parser.exit(1, str(exc) + '\n')
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for result in results:
            print('Source: ' + json.dumps(result['scout']['evidence'], sort_keys=True))
            for repo in result['auditor']['repos']:
                print('{}: {}/100'.format(repo['name'], repo['score']))
                for category, points in repo['breakdown'].items():
                    print('  {}: {}'.format(category, points))
            print('Coach: {} tasks; {} points recoverable'.format(len(result['coach']['tasks']), result['coach']['evidence']['recoverable_points']))
            for task in result['coach']['tasks']:
                print('  +{} {}: {}'.format(task['points'], task['repo'], task['where']))
    if args.export:
        args.export.write_text(results[0]['tracker']['markdown'], encoding='utf-8')

if __name__ == '__main__':
    main()
