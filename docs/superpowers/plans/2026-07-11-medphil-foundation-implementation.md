# MedPhil Revision Toolkit Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a locally installable Codex plugin foundation with four isolated journal packs, machine-checkable source provenance, two reusable skills, and four offline routing evaluations.

**Architecture:** The plugin manifest points to two skills: a workflow controller and a journal router. Journal knowledge stays outside the skills in uniform YAML/Markdown packs; Python validators enforce the pack contract and an offline lexical baseline provides deterministic routing regression tests without claiming acceptance prediction.

**Tech Stack:** Codex plugin manifest, Agent Skills Markdown, Python 3.12, standard-library `unittest`, PyYAML, Apache-2.0, PowerShell.

---

## Execution context

- Project root: `<repo-root>`
- Python: `python`
- Git: `git`
- Full test command:

```powershell
$PY='python'
& $PY -m unittest discover -s evals/tests -v
```

## File responsibility map

| Path | Responsibility |
|---|---|
| `.codex-plugin/plugin.json` | Plugin identity and bundled-skill entry point |
| `skills/medphil-revision/SKILL.md` | Full revision workflow, safety gates, and outputs |
| `skills/journal-router/SKILL.md` | Four-journal comparison and routing explanation |
| `journal-packs/*/profile.yaml` | Machine-readable scope and routing signals |
| `journal-packs/*/source_registry.md` | YAML-front-matter evidence registry plus human notes |
| `journal-packs/*/official_requirements.md` | Current official requirements only |
| `journal-packs/*/editorial_profile.md` | Clearly labeled observed tendencies and inferences |
| `journal-packs/*/routing_examples.md` | Human-readable positive and negative routing cases |
| `journal-packs/*/eval_cases.yaml` | Pack-local evaluation cases |
| `scripts/validate_journal_pack.py` | Contract, evidence-type, URL, and staleness validation |
| `scripts/route_journal.py` | Deterministic offline routing baseline |
| `evals/fixtures/routing_cases.yaml` | Four cross-journal regression cases |
| `evals/tests/*` | Automated structure, provenance, and routing tests |

### Task 1: Establish a testable plugin skeleton

**Files:**
- Create: `.codex-plugin/plugin.json`
- Create: `requirements.txt`
- Create: `skills/medphil-revision/SKILL.md`
- Create: `skills/medphil-revision/agents/openai.yaml`
- Create: `skills/journal-router/SKILL.md`
- Create: `skills/journal-router/agents/openai.yaml`
- Create: `evals/tests/test_plugin_structure.py`

- [ ] **Step 1: Write the failing plugin-structure test**

Create `evals/tests/test_plugin_structure.py`:

```python
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class PluginStructureTests(unittest.TestCase):
    def test_manifest_points_to_existing_skills_directory(self):
        manifest_path = ROOT / ".codex-plugin" / "plugin.json"
        self.assertTrue(manifest_path.exists())
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"], "medphil-revision-toolkit")
        self.assertEqual(manifest["skills"], "./skills/")
        self.assertTrue((ROOT / manifest["skills"]).is_dir())

    def test_required_skills_have_frontmatter(self):
        for name in ("medphil-revision", "journal-router"):
            text = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertTrue(text.startswith("---\n"))
            self.assertIn(f"name: {name}", text)
            self.assertIn("description:", text)
            metadata = (ROOT / "skills" / name / "agents" / "openai.yaml")
            self.assertTrue(metadata.exists())
            self.assertIn(f"${name}", metadata.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test and verify RED**

Run:

```powershell
$PY='python'
& $PY -m unittest evals.tests.test_plugin_structure -v
```

Expected: FAIL because `.codex-plugin/plugin.json` and both skill files do not exist.

- [ ] **Step 3: Create the minimal plugin files**

Create `.codex-plugin/plugin.json`:

```json
{
  "name": "medphil-revision-toolkit",
  "version": "0.1.0-alpha.1",
  "description": "Journal routing and safe revision workflows for philosophy of medicine and bioethics manuscripts.",
  "author": {
    "name": "MedPhil Revision Toolkit Contributors"
  },
  "license": "Apache-2.0",
  "keywords": ["bioethics", "medical-ethics", "philosophy-of-medicine", "academic-editing"],
  "skills": "./skills/",
  "interface": {
    "displayName": "MedPhil Revision Toolkit",
    "shortDescription": "Route and revise medical philosophy manuscripts",
    "longDescription": "Compare journal fit and safely revise philosophy of medicine and bioethics manuscripts with source-aware journal adapters.",
    "developerName": "MedPhil Revision Toolkit Contributors",
    "category": "Productivity",
    "capabilities": ["Read", "Write"],
    "defaultPrompt": [
      "Compare this manuscript across MHCP, JME, Bioethics, and JMP."
    ]
  }
}
```

Create `requirements.txt`:

```text
PyYAML>=6.0,<7.0
python-docx>=1.2,<2.0
```

Initialize both skill folders before replacing the generated placeholders:

```powershell
$PY='python'
$INIT='<codex-home>\skills\.system\skill-creator\scripts\init_skill.py'
& $PY $INIT medphil-revision --path skills --interface 'display_name=MedPhil Revision' --interface 'short_description=Revise medical philosophy manuscripts safely' --interface 'default_prompt=Use $medphil-revision to revise this manuscript for its confirmed target journal.'
& $PY $INIT journal-router --path skills --interface 'display_name=Journal Router' --interface 'short_description=Compare fit across four ethics journals' --interface 'default_prompt=Use $journal-router to compare this manuscript across MHCP, JME, Bioethics, and JMP.'
```

Replace the generated `skills/medphil-revision/SKILL.md` with:

```markdown
---
name: medphil-revision
description: Use when an English philosophy-of-medicine, bioethics, medical-ethics, or medical-humanities manuscript needs journal selection or revision for MHCP, JME, Bioethics, or JMP.
---

# MedPhil Revision

Load the journal-router skill first when the target journal is not confirmed. Preserve the author's thesis, citations, reference list, factual claims, and original input file. Produce a clean revised manuscript, revision log, journal-fit report, routing report, and author-confirmation list. Stop on identifiable patient information or unsafe document structure.
```

Replace the generated `skills/journal-router/SKILL.md` with:

```markdown
---
name: journal-router
description: Use when the target journal is undecided among MHCP, JME, Bioethics, and JMP, or when manuscript fit needs comparison before revision.
---

# Journal Router

Compare all four journal packs. Separate official requirements, observed tendencies, and editorial inference. Recommend a ranked target with reasons and mismatch risks. Never provide an acceptance probability. Require author confirmation before loading a revision adapter.
```

- [ ] **Step 4: Run the structure test and verify GREEN**

Run the command from Step 2.

Expected: 2 tests pass.

- [ ] **Step 5: Commit only Task 1 files**

```powershell
$GIT='git'
& $GIT add -- '.codex-plugin/plugin.json' 'requirements.txt' 'skills/medphil-revision' 'skills/journal-router' 'evals/tests/test_plugin_structure.py'
& $GIT commit -m 'feat: scaffold medphil revision plugin'
```

### Task 2: Define and enforce the journal-pack contract

**Files:**
- Create: `scripts/validate_journal_pack.py`
- Create: `references/journal_pack_schema.md`
- Create: `evals/tests/test_journal_pack_validator.py`

- [ ] **Step 1: Write validator tests first**

Create `evals/tests/test_journal_pack_validator.py`:

```python
import tempfile
import unittest
from pathlib import Path

from scripts.validate_journal_pack import validate_pack


VALID_PROFILE = """id: mhcp
name: Medicine, Health Care and Philosophy
publisher: Springer Nature
scope_summary: Philosophy of medicine, health care, and bioethics.
article_types: [conceptual, normative]
fit_signals: [clinical judgment, philosophy of medicine]
mismatch_signals: [purely technical validation]
official_urls: [https://link.springer.com/journal/11019]
checked_at: 2026-07-11
"""

VALID_REGISTRY = """---
sources:
  - claim_id: scope-001
    claim: The journal covers philosophy of medicine and health care.
    evidence_type: official_requirement
    url: https://link.springer.com/journal/11019
    checked_at: 2026-07-11
    applies_to: all articles
    status: current
---
# Source notes
"""


class JournalPackValidatorTests(unittest.TestCase):
    def make_pack(self, profile=VALID_PROFILE, registry=VALID_REGISTRY):
        temp = tempfile.TemporaryDirectory()
        path = Path(temp.name)
        (path / "profile.yaml").write_text(profile, encoding="utf-8")
        (path / "source_registry.md").write_text(registry, encoding="utf-8")
        for name in ("official_requirements.md", "editorial_profile.md", "routing_examples.md"):
            (path / name).write_text(f"# {name}\n", encoding="utf-8")
        (path / "eval_cases.yaml").write_text("cases: []\n", encoding="utf-8")
        return temp, path

    def test_valid_pack_has_no_errors(self):
        temp, path = self.make_pack()
        self.addCleanup(temp.cleanup)
        self.assertEqual(validate_pack(path, as_of="2026-07-11"), [])

    def test_missing_profile_field_is_reported(self):
        temp, path = self.make_pack(profile=VALID_PROFILE.replace("publisher: Springer Nature\n", ""))
        self.addCleanup(temp.cleanup)
        self.assertIn("profile missing field: publisher", validate_pack(path, as_of="2026-07-11"))

    def test_unknown_evidence_type_is_reported(self):
        temp, path = self.make_pack(registry=VALID_REGISTRY.replace("official_requirement", "reputation"))
        self.addCleanup(temp.cleanup)
        self.assertIn("source scope-001 has invalid evidence_type: reputation", validate_pack(path, as_of="2026-07-11"))

    def test_source_older_than_90_days_is_reported(self):
        temp, path = self.make_pack(registry=VALID_REGISTRY.replace("2026-07-11", "2026-01-01"))
        self.addCleanup(temp.cleanup)
        self.assertIn("source scope-001 is stale", validate_pack(path, as_of="2026-07-11"))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Install the declared dependencies and verify RED**

```powershell
$PY='python'
& $PY -m pip install -r requirements.txt
& $PY -m unittest evals.tests.test_journal_pack_validator -v
```

Expected: dependency installation succeeds; test import fails because `scripts.validate_journal_pack` does not exist.

- [ ] **Step 3: Implement the minimal validator**

Create `scripts/validate_journal_pack.py`:

```python
import argparse
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

import yaml

REQUIRED_FILES = {
    "profile.yaml",
    "source_registry.md",
    "official_requirements.md",
    "editorial_profile.md",
    "routing_examples.md",
    "eval_cases.yaml",
}
PROFILE_FIELDS = {
    "id", "name", "publisher", "scope_summary", "article_types",
    "fit_signals", "mismatch_signals", "official_urls", "checked_at",
}
EVIDENCE_TYPES = {
    "official_requirement", "observed_tendency",
    "editorial_inference", "abstract_limited",
}
MAX_AGE_DAYS = 90


def _frontmatter(text):
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    return yaml.safe_load(text[4:end]) if end != -1 else {}


def _valid_url(value):
    parsed = urlparse(str(value))
    return parsed.scheme == "https" and bool(parsed.netloc)


def _to_date(value):
    return value if isinstance(value, date) else date.fromisoformat(str(value))


def validate_pack(pack_path, as_of=None):
    path = Path(pack_path)
    errors = []
    missing = sorted(REQUIRED_FILES - {item.name for item in path.iterdir()})
    errors.extend(f"missing file: {name}" for name in missing)
    if missing:
        return errors

    profile = yaml.safe_load((path / "profile.yaml").read_text(encoding="utf-8")) or {}
    for field in sorted(PROFILE_FIELDS - set(profile)):
        errors.append(f"profile missing field: {field}")
    for url in profile.get("official_urls", []):
        if not _valid_url(url):
            errors.append(f"profile has invalid official URL: {url}")

    registry = _frontmatter((path / "source_registry.md").read_text(encoding="utf-8"))
    today = _to_date(as_of or date.today())
    for source in registry.get("sources", []):
        claim_id = source.get("claim_id", "unknown")
        evidence_type = source.get("evidence_type")
        if evidence_type not in EVIDENCE_TYPES:
            errors.append(f"source {claim_id} has invalid evidence_type: {evidence_type}")
        if not _valid_url(source.get("url")):
            errors.append(f"source {claim_id} has invalid URL")
        checked_at = source.get("checked_at")
        if checked_at and (today - _to_date(checked_at)).days > MAX_AGE_DAYS:
            errors.append(f"source {claim_id} is stale")
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pack")
    parser.add_argument("--as-of")
    args = parser.parse_args()
    errors = validate_pack(args.pack, as_of=args.as_of)
    for error in errors:
        print(error)
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
```

Create `references/journal_pack_schema.md` documenting the exact fields and four allowed evidence types shown above, plus the rule that official requirements are rechecked every 90 days.

- [ ] **Step 4: Run validator tests and verify GREEN**

Run the test command from Step 2.

Expected: 4 tests pass.

- [ ] **Step 5: Commit Task 2 files**

```powershell
$GIT='git'
& $GIT add -- 'scripts/validate_journal_pack.py' 'references/journal_pack_schema.md' 'evals/tests/test_journal_pack_validator.py' 'requirements.txt'
& $GIT commit -m 'feat: validate journal pack provenance'
```

### Task 3: Add four isolated journal packs

**Files:**
- Create: `journal-packs/{mhcp,jme,bioethics,jmp}/profile.yaml`
- Create: `journal-packs/{mhcp,jme,bioethics,jmp}/source_registry.md`
- Create: `journal-packs/{mhcp,jme,bioethics,jmp}/official_requirements.md`
- Create: `journal-packs/{mhcp,jme,bioethics,jmp}/editorial_profile.md`
- Create: `journal-packs/{mhcp,jme,bioethics,jmp}/routing_examples.md`
- Create: `journal-packs/{mhcp,jme,bioethics,jmp}/eval_cases.yaml`
- Create: `evals/tests/test_repository_journal_packs.py`

- [ ] **Step 1: Write the repository-pack test**

```python
import unittest
from pathlib import Path

from scripts.validate_journal_pack import validate_pack

ROOT = Path(__file__).resolve().parents[2]


class RepositoryJournalPackTests(unittest.TestCase):
    def test_all_four_packs_validate(self):
        for journal_id in ("mhcp", "jme", "bioethics", "jmp"):
            with self.subTest(journal=journal_id):
                self.assertEqual(
                    validate_pack(ROOT / "journal-packs" / journal_id, as_of="2026-07-11"),
                    [],
                )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run and verify RED**

Expected: FAIL because `journal-packs/mhcp` does not exist.

- [ ] **Step 3: Create the packs from verified official sources**

Use these pack IDs, publishers, and primary official URLs:

```yaml
mhcp:
  name: Medicine, Health Care and Philosophy
  publisher: Springer Nature
  url: https://link.springer.com/journal/11019
jme:
  name: Journal of Medical Ethics
  publisher: BMJ
  url: https://jme.bmj.com/pages/about
bioethics:
  name: Bioethics
  publisher: Wiley
  url: https://onlinelibrary.wiley.com/page/journal/14678519/homepage/productinformation.html
jmp:
  name: The Journal of Medicine and Philosophy
  publisher: Oxford University Press
  url: https://academic.oup.com/jmp
```

For each `profile.yaml`, use the shared schema and at least three `fit_signals` plus two `mismatch_signals`. For each `source_registry.md`, register the official scope claim with `official_requirement`, `checked_at: 2026-07-11`, and `status: current`. Keep `observed_tendency` and `editorial_inference` out of `official_requirements.md`; place them in `editorial_profile.md` with explicit labels. Create at least one positive and one negative case in both `routing_examples.md` and `eval_cases.yaml`.

- [ ] **Step 4: Run the full suite and verify GREEN**

Expected: 7 tests pass: 2 structure, 4 validator, 1 repository-pack test.

- [ ] **Step 5: Commit the journal packs**

```powershell
$GIT='git'
& $GIT add -- 'journal-packs' 'evals/tests/test_repository_journal_packs.py'
& $GIT commit -m 'feat: add four journal adapter packs'
```

### Task 4: Build the deterministic routing baseline

**Files:**
- Create: `scripts/route_journal.py`
- Create: `evals/fixtures/routing_cases.yaml`
- Create: `evals/tests/test_routing_baseline.py`

- [ ] **Step 1: Write four failing routing cases**

Create `evals/fixtures/routing_cases.yaml` with exactly four cases whose expected primary journals are `mhcp`, `jme`, `bioethics`, and `jmp`. Each case contains `id`, `title`, `abstract`, `expected_primary`, and `reason_markers`. Use synthetic abstracts: care/phenomenology for MHCP; bedside allocation/clinical committee for JME; AI/data justice/policy for Bioethics; health-disease/metaphysics/conceptual analysis for JMP.

Create `evals/tests/test_routing_baseline.py`:

```python
import unittest
from pathlib import Path

import yaml

from scripts.route_journal import route_text

ROOT = Path(__file__).resolve().parents[2]


class RoutingBaselineTests(unittest.TestCase):
    def test_four_synthetic_cases_route_to_expected_primary(self):
        data = yaml.safe_load((ROOT / "evals/fixtures/routing_cases.yaml").read_text(encoding="utf-8"))
        self.assertEqual(len(data["cases"]), 4)
        for case in data["cases"]:
            with self.subTest(case=case["id"]):
                ranking = route_text(case["title"] + " " + case["abstract"], ROOT / "journal-packs")
                self.assertEqual(ranking[0]["journal"], case["expected_primary"])
                self.assertNotIn("acceptance_probability", ranking[0])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run and verify RED**

Expected: import failure because `scripts.route_journal` does not exist.

- [ ] **Step 3: Implement a transparent offline baseline**

Create `scripts/route_journal.py`:

```python
from pathlib import Path

import yaml


def route_text(text, packs_root):
    haystack = text.casefold()
    ranking = []
    for profile_path in sorted(Path(packs_root).glob("*/profile.yaml")):
        profile = yaml.safe_load(profile_path.read_text(encoding="utf-8"))
        positive = [term for term in profile["fit_signals"] if str(term).casefold() in haystack]
        negative = [term for term in profile["mismatch_signals"] if str(term).casefold() in haystack]
        ranking.append({
            "journal": profile["id"],
            "score": (2 * len(positive)) - len(negative),
            "matched_fit_signals": positive,
            "matched_mismatch_signals": negative,
        })
    return sorted(ranking, key=lambda item: (-item["score"], item["journal"]))
```

Document in the module docstring that this baseline is a regression aid, not the final semantic router and not an acceptance predictor.

- [ ] **Step 4: Tune only pack signals until GREEN**

Run the full suite. Change only `fit_signals` and `mismatch_signals` when a synthetic case is misrouted; do not add case-specific code.

Expected: 8 tests pass.

- [ ] **Step 5: Commit routing baseline and cases**

```powershell
$GIT='git'
& $GIT add -- 'scripts/route_journal.py' 'evals/fixtures/routing_cases.yaml' 'evals/tests/test_routing_baseline.py' 'journal-packs'
& $GIT commit -m 'test: add four-journal routing baseline'
```

### Task 5: Expand both skills into complete safe workflows

**Files:**
- Modify: `skills/medphil-revision/SKILL.md`
- Modify: `skills/journal-router/SKILL.md`
- Create: `references/source_policy.md`
- Create: `references/editorial_safety.md`
- Create: `evals/tests/test_skill_contracts.py`

- [ ] **Step 1: Write contract tests**

The test must assert that the revision skill names all five outputs, contains the phrases `preserve the author's thesis`, `do not invent citations`, and `identifiable patient information`, and requires target-journal confirmation. The router test must assert all four journal IDs, evidence-layer separation, mismatch reasons, and the prohibition on acceptance probability.

- [ ] **Step 2: Run and verify RED**

Expected: FAIL because the minimal skills do not yet contain the complete contracts.

- [ ] **Step 3: Expand the skills using approved design language**

Keep each `SKILL.md` under 250 lines. `medphil-revision` must implement intake, document safety gate, manuscript profile, routing handoff, journal-fit diagnosis, staged revision, citation freeze, safety review, and five outputs. `journal-router` must load all four profiles, rank fit, explain positive and negative signals, separate `official_requirement`, `observed_tendency`, `editorial_inference`, and `abstract_limited`, and stop before revision until the author confirms a target.

Create `references/source_policy.md` and `references/editorial_safety.md` from Sections 6 and 7 of the approved design without copying journal article prose.

- [ ] **Step 4: Run full suite and verify GREEN**

Expected: all structure, validator, pack, routing, and skill-contract tests pass.

- [ ] **Step 5: Commit workflow skills and policies**

```powershell
$GIT='git'
& $GIT add -- 'skills' 'references/source_policy.md' 'references/editorial_safety.md' 'evals/tests/test_skill_contracts.py'
& $GIT commit -m 'feat: define safe journal revision workflows'
```

### Task 6: Finish foundation documentation and verification

**Files:**
- Create: `LICENSE`
- Create: `CONTRIBUTING.md`
- Create: `CHANGELOG.md`
- Modify: `README.md`
- Modify: `project_log.md`
- Modify: `<workspace-root>\全局控制台.md`

- [ ] **Step 1: Add Apache-2.0 and contribution rules**

Use the unmodified Apache License 2.0 text in `LICENSE`. `CONTRIBUTING.md` must require legal sources, no paywall bypass, no unpublished manuscripts, no identifiable patient data, source dates, pack validation, and at least one positive plus one negative routing case.

- [ ] **Step 2: Add release metadata**

Create `CHANGELOG.md` with an `0.1.0-alpha.1` entry listing plugin skeleton, four journal packs, source validation, routing baseline, and safety workflow. Update README with installation, validation, directory map, current limitations, and the exact full test command.

- [ ] **Step 3: Run fresh verification**

```powershell
$PY='python'
& $PY -m unittest discover -s evals/tests -v
& $PY scripts/validate_journal_pack.py journal-packs/mhcp
& $PY scripts/validate_journal_pack.py journal-packs/jme
& $PY scripts/validate_journal_pack.py journal-packs/bioethics
& $PY scripts/validate_journal_pack.py journal-packs/jmp
$PLUGIN_VALIDATOR='<codex-home>\skills\.system\plugin-creator\scripts\validate_plugin.py'
$SKILL_VALIDATOR='<codex-home>\skills\.system\skill-creator\scripts\quick_validate.py'
& $PY $PLUGIN_VALIDATOR .
& $PY $SKILL_VALIDATOR skills/medphil-revision
& $PY $SKILL_VALIDATOR skills/journal-router
```

Expected: all tests pass; each journal-pack command exits 0; the plugin and both skill validators report success.

- [ ] **Step 4: Inspect plugin contents**

```powershell
Get-ChildItem -Recurse -Force | Select-Object FullName,Length
rg -n 'T[B]D|T[O]DO|acceptance probability|AI percentage|bypass paywall' README.md skills journal-packs references CONTRIBUTING.md
```

Expected: no placeholders; prohibited claims appear only in explicit prohibition language.

- [ ] **Step 5: Update project records and commit**

Set Project_038 status to `阶段 1 已完成` only after the verification output is fresh. Record exact test count and remaining Phase 2 DOCX work in `project_log.md` and `全局控制台.md`.

```powershell
$GIT='git'
& $GIT add -- 'Project_038_medphil_revision_toolkit' '全局控制台.md'
& $GIT commit -m 'docs: complete medphil toolkit foundation'
```

## Plan self-review result

- Spec coverage for Phase 1: plugin packaging, four journal packs, provenance, routing, skill safety, documentation, and offline evaluation are covered.
- Deferred by deliberate phase boundary: DOCX inspection/protection, clean revised DOCX generation, revision-log generation from document diffs, and end-to-end manuscript processing belong to Phase 2.
- Type consistency: journal IDs are `mhcp`, `jme`, `bioethics`, and `jmp`; validator entry point is `validate_pack`; router entry point is `route_text`.
- No production implementation begins before its failing test.
