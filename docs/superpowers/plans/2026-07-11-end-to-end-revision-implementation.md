# End-to-End Revision Orchestration Implementation Plan

> **Execution mode:** Follow this plan sequentially in the current agent session. Write a failing test before each production behavior and commit only after the complete phase passes verification.

**Goal:** Turn the validated journal knowledge base and DOCX safety layer into a usable v0.1 workflow that applies an explicitly reviewed revision specification to a safe DOCX copy and produces all five required deliverables.

**Architecture:** The skill performs contextual diagnosis and writes a structured revision specification. Deterministic scripts validate that specification, reject unsafe paragraph targets, apply only exact-match prose replacements to a new DOCX, compare protected fields, and assemble reports from structured records. The original manuscript, citations, references, tables, notes, comments, and complex formatted paragraphs remain protected by default.

**Phase boundary:** This phase supports controlled paragraph-level revision. It does not promise lossless editing of fields, equations, text boxes, nested content controls, citation-manager objects, or mixed-format paragraphs.

---

## Task 1: Revision specification contract

**Files:**
- Create: `references/revision_spec_schema.json`
- Create: `scripts/validate_revision_spec.py`
- Create: `evals/tests/test_revision_spec.py`

- [x] Write failing tests for the required target journal, source hash, paragraph index, exact original text, revised text, reason, risk level, and author-confirmation flag.
- [x] Require the target journal to be one of `mhcp`, `jme`, `bioethics`, or `jmp`.
- [x] Reject empty revisions, unknown fields, invalid risk levels, and source-hash mismatch.
- [x] Implement a JSON-only contract so semantic judgment remains inspectable before DOCX mutation.

## Task 2: Safe paragraph inventory

**Files:**
- Create: `scripts/build_revision_inventory.py`
- Create: `evals/tests/test_revision_inventory.py`

- [x] Build a paragraph inventory with stable indices, section headings, style names, text hashes, citation presence, reference-section status, run count, hyperlinks, fields, drawings, and edit eligibility.
- [x] Mark citation-bearing, reference, empty, table, field-containing, drawing-containing, and mixed-format paragraphs as protected by default.
- [x] Add tests showing that ordinary abstract/introduction prose is eligible while citations and complex content are not.

## Task 3: Exact-match DOCX revision engine

**Files:**
- Create: `scripts/apply_revision_spec.py`
- Create: `evals/tests/test_apply_revision_spec.py`

- [x] Write failing tests that revise eligible prose in a new output file while leaving the input hash unchanged.
- [x] Reject an existing output, incorrect paragraph index, original-text mismatch, protected paragraph, citation change, and reference change.
- [x] Preserve paragraph style and use the existing safe working-copy and protected-field comparison functions.
- [x] Return a machine-readable application record containing applied, rejected, and author-confirmation items.

## Task 4: Five-deliverable assembly

**Files:**
- Create: `scripts/build_delivery_bundle.py`
- Create: `references/report_contract.md`
- Create: `evals/tests/test_delivery_bundle.py`

- [x] Generate `revision_log.md` from the application record and before/after manifests.
- [x] Generate `journal_routing_report.md` with all four journals, fit reasons, mismatch reasons, evidence limits, recommendation, and alternative.
- [x] Generate `journal_fit_report.md` with the confirmed target, evidence-layer labels, remaining risks, and pre-submission checks.
- [x] Generate `author_confirmation_needed.md` with unresolved conceptual, normative, evidential, and formatting choices, or an explicit none-required statement.
- [x] Validate that the bundle contains exactly the required five named deliverables including `revised_manuscript.docx`.

## Task 5: Skill orchestration update

**Files:**
- Modify: `skills/medphil-revision/SKILL.md`
- Modify: `skills/medphil-revision/agents/openai.yaml`
- Create: `skills/medphil-revision/references/revision_workflow.md`
- Modify: `evals/tests/test_skill_contracts.py`

- [x] Require strict intake, inventory generation, routing or confirmed-target reuse, diagnosis, revision-spec review, exact-match application, protected-field comparison, and delivery-bundle validation.
- [x] Require the skill to stop rather than force edits when a high-impact paragraph is ineligible.
- [x] Keep Chinese interaction and English manuscript outputs explicit.
- [x] Preserve the rule that thesis-altering edits enter author confirmation rather than being silently applied.

## Task 6: Synthetic MHCP end-to-end evaluation

**Files:**
- Create: `evals/fixtures/synthetic_revision_spec.json`
- Create: `evals/expected/synthetic_routing_report.md`
- Create: `evals/expected/synthetic_fit_report.md`
- Create: `evals/expected/synthetic_confirmation.md`
- Create: `evals/tests/test_end_to_end_revision.py`

- [x] Use the existing synthetic manuscript and a confirmed MHCP route.
- [x] Revise eligible abstract, ethical-analysis, and conclusion prose; assert that the citation-bearing introduction remains frozen.
- [x] Assert that all five deliverables exist, the original hash is unchanged, protected fields pass, and expected prose changes appear only in the revised copy.
- [x] Render the revised DOCX and inspect every page for clipping, overlap, missing glyphs, table damage, and pagination drift.

## Task 7: Release-candidate verification and documentation

**Files:**
- Modify: `README.md`
- Modify: `CHANGELOG.md`
- Modify: `CONTRIBUTING.md`
- Modify: `project_log.md`
- Modify: `全局控制台.md` at the workspace level
- Append: `工程复利日志.md` at the workspace level

- [x] Run the full unit suite, four journal-pack validators, plugin validator, and both skill validators.
- [x] Scan for placeholders, local absolute paths, unpublished text, and ignored render artifacts.
- [x] Document supported and rejected DOCX edit classes with a minimal local example.
- [x] Confirm the Git worktree is clean and keep `feature/foundation` as previously selected.
- [x] Commit the complete phase as one intentional change.

## Completion criteria

- All five required deliverables are generated from a synthetic English DOCX.
- The input DOCX hash remains unchanged.
- Citations, references, tables, sections, comments, and footnotes pass protected-field comparison.
- Unsafe or ambiguous paragraph edits fail closed.
- The revised DOCX passes page-by-page visual inspection.
- No real patient, author, or unpublished manuscript content enters fixtures or repository history.
