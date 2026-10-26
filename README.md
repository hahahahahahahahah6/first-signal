# FirstSignal

A transparent portfolio auditor for first-time coders. Four deterministic agents turn public repository metadata into evidence, prioritized improvements and a downloadable PORTFOLIO.md. Python 3.9+; standard library only. No installation, account, API key or paid service is required.

## Problem size

The target problem is first-time coders whose public projects lack readable evidence of their work. A missing README, description or test signal makes a project harder to understand. The number of affected people has not been measured by this project; no population or employment statistics are claimed.

## Severity

A reviewer cannot easily reproduce or assess an undocumented project. This creates avoidable friction when presenting a portfolio. This project has not measured recruiter behavior or employment outcomes.

## Solution

Scout reads fixtures or public GitHub REST data. Auditor applies the published rubric below and retains each observation. Coach maps every lost point to a concrete task, location and example, sorted by points recoverable. Tracker creates a checklist and PORTFOLIO.md. Each agent returns its own evidence. An optional environment-configured LLM adapter stub is in `first_signal/llm_adapter.py`; it makes no network calls and is never required.

| Category | Maximum | Exact v1 heuristic |
| --- | ---: | --- |
| README | 25 | Nonempty README |
| Description + topics | 15 | Nonempty description 10; at least one topic 5 |
| Licence | 10 | GitHub licence metadata present |
| Tests/CI signal | 20 | Root tests/, test/, pytest.ini or tox.ini 10; workflow .yml/.yaml 10 |
| Recent activity | 15 | pushed_at between 0 and 180 days before audit date, inclusive |
| Portfolio polish | 15 | Nonempty homepage 5; README contains `## Example`, `## Demo` or image markup 10 (case insensitive) |
| Total | 100 | Additive; missing evidence earns zero |

Showcase evidence is a proxy for a presentation worth pinning; actual pinned repositories are not queried. Scores do not verify README accuracy, licence validity, test execution, CI success, demo availability or code quality. Unknown evidence earns zero, so a score can understate a project. Tasks improve these observable signals; adding a file alone does not prove quality. **The score is NOT a hiring prediction or job offer.**

## Run

From this project directory:

```sh
python3 -m unittest discover -s tests -v
python3 -m first_signal.cli --fixture strong --fixture weak
python3 -m first_signal.cli --fixture empty
python3 -m first_signal.cli --fixture weak --export PORTFOLIO.md
python3 -m first_signal.cli --username octocat
python3 -m first_signal.cli --username octocat --fallback-fixture weak --json
python3 -m first_signal.server
```

Visit http://127.0.0.1:8000. Enter a username or `fixture:strong`, `fixture:weak`, `fixture:empty`. Results include breakdown, rule evidence, Coach tasks and an export link. JSON is available at `/api/audit?source=fixture:weak`; download at `/export?source=fixture:weak`. Exports recompute the audit; live data may change between requests.

Public API mode reads at most three repositories sorted by push time, using at most ten requests per audit (one list and up to three reads per repository). No authentication, retries, background polling or pagination. HTTP 404 on optional files means missing evidence; other failures stop the audit. CLI fallback is opt-in and prominently labeled as fixture evidence. Fixture dates are frozen for reproducibility; live audits use the current UTC machine date. Requests time out after 15 seconds each. GitHub may rate-limit anonymous clients. Prefer fixtures for repeated demos.

For a host you control, `python3 -m first_signal.server --host 0.0.0.0 --port 8000` binds externally. Use a reverse proxy with TLS and request limits for public deployment: this minimal server has no authentication, caching or abuse controls. No cloud deployment or account creation is included.

## Proven impact

See [measured evidence](docs/IMPACT_EVIDENCE.md) for exact commands, test output, fixture results, a fixture before/after intervention and a separately labeled public API sample. These measure repository evidence only. No real users, adoption, hiring gains or job offers are claimed. See [demo script](docs/DEMO_SCRIPT.md) for a 2–3 minute recording plan; no video has been recorded.

## Licence

MIT, copyright 2026 hao li. See [LICENSE](LICENSE).
