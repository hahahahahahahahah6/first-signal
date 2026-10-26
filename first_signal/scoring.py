"""Published additive rubric; missing/unknown evidence earns no points."""
from datetime import date
WEIGHTS = {"README": 25, "description+topics": 15, "licence": 10,
           "tests/CI signal": 20, "recent activity": 15, "portfolio polish": 15}
# name, category, points, field, actionable instruction, example
RULES = [
 ("readme", "README", 25, "readme", "Add README.md with purpose, setup and a usage example", "# Project\nSolves ...\n## Run\npython3 app.py"),
 ("description", "description+topics", 10, "description", "Set the repository About description", "A command-line tool that helps beginners track study sessions."),
 ("topics", "description+topics", 5, "topics", "Add relevant repository topics in About", "python, education, command-line"),
 ("licence", "licence", 10, "license", "Choose a suitable licence and add LICENSE", "MIT (only if appropriate for your work and dependencies)"),
 ("tests", "tests/CI signal", 10, "tests", "Add tests/ with an executable test case", "python3 -m unittest discover -s tests -v"),
 ("ci", "tests/CI signal", 10, "ci", "Add .github/workflows/tests.yml to run tests", "Run python3 -m unittest discover -s tests -v on push."),
 ("activity", "recent activity", 15, "pushed_at", "Ship a meaningful improvement and push it", "Implement and test one documented bug fix; avoid empty activity commits."),
 ("homepage", "portfolio polish", 5, "homepage", "Set About website to useful documentation or a demo", "https://example.org/project-demo"),
 ("showcase", "portfolio polish", 10, "showcase", "Add a README screenshot, demo or worked example", "## Example\nInput: ...\nOutput: ...")]

def score(repo, as_of):
    breakdown = {k: 0 for k in WEIGHTS}
    evidence = []
    for name, category, points, field, instruction, example in RULES:
        value = repo.get(field)
        present = bool(value)
        if field == "pushed_at":
            try:
                age = (date.fromisoformat(as_of) - date.fromisoformat(value[:10])).days
                present = 0 <= age <= 180
            except (TypeError, ValueError):
                present = False
        earned = points if present else 0
        breakdown[category] += earned
        evidence.append(dict(rule=name, category=category, maximum=points, earned=earned,
                             observed=value, instruction=instruction, example=example))
    return dict(name=repo['full_name'], score=sum(breakdown.values()), breakdown=breakdown,
                evidence=evidence, url=repo.get('html_url', ''))
