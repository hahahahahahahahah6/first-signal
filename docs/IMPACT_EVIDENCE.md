# Impact evidence

## Scope and date

Measured 2026-10-26. Fixture as-of date: 2026-10-26. Scores measure observable portfolio evidence. A higher score is NOT a hiring prediction or job offer. No users, adoption or employment outcomes have been measured.

## Fixture baseline

Three synthetic repositories: strong 100/100 (0 gaps), weak 10/100 (8 gaps), empty 0/100 (9 gaps). Total 3 repos and 17 fixable rule gaps. These are fixtures, not real users or deployed impact.

## Fixture intervention

Weak fixture: 10 → 35/100; gaps 8 → 7. Applied only the Coach README task by changing the normalized readme evidence to true in memory. Synthetic intervention, not a real repository edit.

Reproduce from the project root:

```sh
python3 -m unittest discover -s tests -v
python3 -m first_signal.cli --fixture strong --fixture weak
python3 -m first_signal.cli --fixture empty
```

`test_before_after` reproduces the 10 → 35 intervention without altering the baseline fixture.

## Actual test transcript

```text
test_activity_boundaries (test_first_signal.PipelineTests.test_activity_boundaries) ... ok
test_api (test_first_signal.PipelineTests.test_api) ... ok
test_before_after (test_first_signal.PipelineTests.test_before_after) ... ok
test_coach_order_and_accounting (test_first_signal.PipelineTests.test_coach_order_and_accounting) ... ok
test_explicit_fallback (test_first_signal.PipelineTests.test_explicit_fallback) ... ok
test_fixture_determinism (test_first_signal.PipelineTests.test_fixture_determinism) ... ok
test_html_export_errors (test_first_signal.PipelineTests.test_html_export_errors) ... ok
test_public_normalization (test_first_signal.PipelineTests.test_public_normalization) ... ok
test_tracker_names (test_first_signal.PipelineTests.test_tracker_names) ... ok
test_weights (test_first_signal.PipelineTests.test_weights) ... ok

----------------------------------------------------------------------
Ran 10 tests in 0.011s

OK
```

## Actual requested CLI transcript

```text
Source: {"fixture": "strong", "source": "fixture"}
fixture/strong: 100/100
  README: 25
  description+topics: 15
  licence: 10
  tests/CI signal: 20
  recent activity: 15
  portfolio polish: 15
Coach: 0 tasks; 0 points recoverable
Source: {"fixture": "weak", "source": "fixture"}
fixture/weak: 10/100
  README: 0
  description+topics: 10
  licence: 0
  tests/CI signal: 0
  recent activity: 0
  portfolio polish: 0
Coach: 8 tasks; 90 points recoverable
  +25 fixture/weak: Add README.md with purpose, setup and a usage example
  +15 fixture/weak: Ship a meaningful improvement and push it
  +10 fixture/weak: Add .github/workflows/tests.yml to run tests
  +10 fixture/weak: Choose a suitable licence and add LICENSE
  +10 fixture/weak: Add a README screenshot, demo or worked example
  +10 fixture/weak: Add tests/ with an executable test case
  +5 fixture/weak: Set About website to useful documentation or a demo
  +5 fixture/weak: Add relevant repository topics in About
```

## Real-API sample (separate from fixtures)

Command: `python3 -m first_signal.cli --username hahahahahahahahah6 --json`

Public API attempt failed with HTTP 403: rate limit exceeded. No retry or fallback was made. Zero real repositories were audited; no real-user or real-API impact is claimed.

Raw evidence, when successful, is saved in REAL_API_RUN.json beside this document. This bounded convenience sample is not a representative study and does not establish real-world improvement.

## Deployment and participants template

- Deployment URL/date: not deployed.
- Participants and consent: no recruited participants.
- Real before/after repository URLs and commit IDs: not collected.
- Measurement window and sample method: future study should state these explicitly.
- Observed portfolio evidence change: fixture intervention above only.
- Employment outcomes: not measured; never inferred from scores.
- Limitations: heuristic presence checks, small sample, no code execution or hiring validation.

## HTTP verification

An ephemeral local ThreadingHTTPServer served /, /api/audit?source=fixture:weak, /results?source=fixture:weak and /export?source=fixture:weak with HTTP 200. The JSON score was verified as 10. No public deployment was made.
