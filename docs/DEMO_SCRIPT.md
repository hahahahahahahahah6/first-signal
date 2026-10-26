# Demo script — 2 minutes 40 seconds

Preparation: open a terminal in the project root and a browser at http://127.0.0.1:8000. Fixtures work offline. Record the screen yourself; no video is included.

| Time | Action and narration |
| --- | --- |
| 0:00–0:20 | “First-time coders can have useful code but little readable evidence. FirstSignal identifies fixable portfolio gaps.” |
| 0:20–0:45 | Run the strong/weak fixture CLI command below. Explain 100 versus 10, and that these are synthetic examples. |
| 0:45–1:10 | Point at the published six-category rubric in README. Show the +25 README task first and explain every lost point has evidence. |
| 1:10–1:45 | Open the web UI, enter fixture:weak. Expand rule evidence, review example text and tick a checklist task. Download PORTFOLIO.md and show the repository name. |
| 1:45–2:10 | Run the before/after test below. Explain changing the fixture README signal raises 10 to 35; this is a simulated evidence improvement, not a measured employment outcome. |
| 2:10–2:30 | Show IMPACT_EVIDENCE.md with fixture and real-API runs clearly separated. The test transcript and sample counts are reproducible. |
| 2:30–2:40 | “Standard library only, no paid API or model key. This score is not a hiring prediction or job offer.” |

```sh
python3 -m first_signal.cli --fixture strong --fixture weak
python3 -m first_signal.server
# In a second terminal:
python3 -m unittest discover -s tests -p test_first_signal.py -k before_after -v
python3 -m first_signal.cli --fixture weak --export PORTFOLIO.md
```

The exact CLI transcript is in IMPACT_EVIDENCE.md. Optional live demonstration (network dependent, do once):

```sh
python3 -m first_signal.cli --username hahahahahahahahah6 --json
```

Account creation, AgentFoundry import, recording, hosting and final competition submission remain human steps. Nothing has been submitted or deployed.
