# DOCX Safety Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Add a deterministic DOCX intake and protection pipeline that inspects structure, blocks obvious sensitive identifiers, preserves the original, freezes citations and references, produces a safe working copy, and emits an auditable revision log.

**Architecture:** `inspect_docx.py` creates a JSON-safe manifest from python-docx plus OOXML package checks. `protect_document.py` owns copy and invariant comparison; `generate_revision_log.py` renders the comparison into Markdown. A synthetic two-page manuscript supplies deterministic integration and render fixtures.

**Tech Stack:** Python 3.12, python-docx 1.2, zipfile/XML inspection, unittest, canonical Documents skill renderer.

---

## Task 1: Synthetic manuscript and structural manifest

**Files:**
- Create: `scripts/make_synthetic_manuscript.py`
- Create: `scripts/inspect_docx.py`
- Create: `evals/tests/test_docx_inspection.py`

- [x] Write a failing test that generates a two-page DOCX with headings, one table, two citations, a DOI, and a References section; assert paragraph/table/section counts, heading names, citation fingerprints, reference fingerprint, and SHA-256.
- [x] Run `python -m unittest evals.tests.test_docx_inspection -v`; expect import failure for `scripts.inspect_docx`.
- [x] Implement `make_synthetic_manuscript(path)` with python-docx and `inspect_docx(path)` with deterministic text extraction, citation regexes, SHA-256, reference-section fingerprint, and OOXML part presence checks.
- [x] Re-run the test; expect GREEN.

## Task 2: Sensitive-identifier gate

**Files:**
- Modify: `scripts/inspect_docx.py`
- Create: `evals/tests/test_sensitive_gate.py`

- [x] Write failing tests for synthetic email, international phone number, Chinese national-ID-shaped string, and `MRN:` marker; also assert ordinary years and DOI digits do not trigger.
- [x] Implement `detect_sensitive_markers(text)` returning label and redacted match, plus strict CLI failure when markers exist.
- [x] Run the new tests and the full suite; expect GREEN.

## Task 3: Safe working-copy creation

**Files:**
- Create: `scripts/protect_document.py`
- Create: `evals/tests/test_document_protection.py`

- [x] Write failing tests that reject source=destination, reject an existing destination, and verify a new copy has the same hash while leaving the source unchanged.
- [x] Implement `create_working_copy(source, destination)` using resolved-path checks and `shutil.copy2`.
- [x] Run tests; expect GREEN.

## Task 4: Citation, reference, and structure invariants

**Files:**
- Modify: `scripts/protect_document.py`
- Modify: `evals/tests/test_document_protection.py`

- [x] Add a failing test that changes a DOI/reference paragraph and expects `compare_protected_fields` to report citation and reference-fingerprint violations.
- [x] Implement comparison for citations, reference fingerprint, table count, section count, comments-part presence, and footnotes-part presence.
- [x] Confirm an unchanged working copy returns no violations and the changed copy fails for the expected reasons.

## Task 5: Revision-log generation

**Files:**
- Create: `scripts/generate_revision_log.py`
- Create: `evals/tests/test_revision_log.py`

- [x] Write a failing test requiring source/output hashes, structural status, representative changes, and protected-field violations in Markdown.
- [x] Implement `generate_revision_log(before, after, changes, violations)` without reading or rewriting manuscript prose.
- [x] Run tests; expect GREEN.

## Task 6: End-to-end and render verification

**Files:**
- Create: `evals/tests/test_docx_pipeline_integration.py`
- Create: `evals/fixtures/synthetic_manuscript.docx`
- Create: `evals/fixtures/synthetic_working_copy.docx`
- Create: `evals/expected/synthetic_revision_log.md`
- Modify: `README.md`
- Modify: `CHANGELOG.md`
- Modify: `project_log.md`

- [x] Write an integration test that generates the fixture, inspects it, creates a working copy, compares invariants, and generates a clean log.
- [x] Run the full suite; expect at least 19 tests and zero failures.
- [x] Render both DOCX fixtures with the Documents skill `render_docx.py`; require matching page counts and PNGs for every page.
- [x] Inspect every rendered page visually; reject clipping, overlap, broken tables, missing glyphs, or pagination drift.
- [x] Update documentation with commands, supported invariants, privacy limitations, and the fact that semantic PII detection remains outside this deterministic gate.
- [x] Run plugin/skill validators, placeholder scan, and a clean Git status check; commit only after all checks pass.

## Self-review

- Phase boundary: this plan creates a safe working copy but does not perform model-driven prose revision.
- The original file is immutable by contract.
- PII patterns are conservative indicators, not proof that a manuscript is de-identified.
- Rendered PNG/PDF files remain internal QA artifacts.
