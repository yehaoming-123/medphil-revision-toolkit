---
name: medphil-revision
description: Use when an English philosophy-of-medicine, bioethics, medical-ethics, or medical-humanities manuscript needs journal selection or revision for MHCP, JME, Bioethics, or JMP.
---

# MedPhil Revision

Revise the manuscript without changing its intellectual ownership. Preserve the author's thesis, citations, factual claims, and original input file.

## Required references

Read `../../references/editorial_safety.md` before editing. Read `../../references/source_policy.md` before using journal evidence. Read `references/revision_workflow.md` before changing a DOCX. Load only the confirmed target's directory under `../../journal-packs/`.

Respond to the user in Chinese. Keep manuscript prose in English unless the user explicitly requests another language. Reports use Chinese narrative and retain the exact evidence labels.

## Workflow

1. Run `../../scripts/inspect_docx.py <input> --strict`. Stop on any strict-intake failure; never copy sensitive findings into chat or reports.
2. Stop on identifiable patient information, encrypted or damaged files, image-only text, or citation structures that cannot be protected.
3. Run `../../scripts/build_revision_inventory.py <input>` and build a manuscript profile: article type, central question, thesis, key concepts, descriptive claims, interpretive claims, normative claims, and positions requiring author control.
4. If the target is uncertain, invoke `$journal-router`. Confirm the target journal before loading a journal pack or revising prose.
5. Diagnose fit before rewriting. Separate official requirements, observed tendencies, abstract-limited evidence, and editorial inference.
6. Draft a JSON revision specification conforming to `../../references/revision_spec_schema.json`. Revise in order: title/abstract/keywords; introduction/core argument/objections/conclusion; remaining high-risk passages.
7. Run `../../scripts/validate_revision_spec.py <spec> --source <input>`. Present high-risk or thesis-sensitive items for author confirmation instead of silently applying them.
8. Run `../../scripts/apply_revision_spec.py <input> <new-output> <spec>`. Freeze the reference list and unsafe citation-bearing passages. Do not invent citations, evidence, data, clinical cases, or author experiences.
9. Inspect both files and run `compare_protected_fields` from `../../scripts/protect_document.py`. Fail closed on any citation, reference, table, section, comments, or footnotes violation.
10. Run `../../scripts/build_delivery_bundle.py` through its Python API using the application, routing, and fit records. Confirm the output directory contains exactly the five required files.

## Editing rules

- Preserve the author's thesis unless the author explicitly requests restructuring.
- Keep descriptive, interpretive, empirical, and normative claims distinct.
- Treat examples as illustrations, not empirical proof.
- Do not strengthen clinical, causal, or policy claims beyond the supplied evidence.
- Put any change that may alter the author's position in the confirmation file.
- Fail closed when a paragraph contains citations, fields, hyperlinks, drawings, mixed formatting, or other unsupported content. Diagnose the issue instead of forcing an edit.
- Never overwrite the original manuscript.

## Required outputs

- `revised_manuscript.docx`: clean revised copy.
- `revision_log.md`: material changes and reasons.
- `journal_routing_report.md`: four-journal comparison, or a note that an existing confirmed route was reused.
- `journal_fit_report.md`: target-journal fit, evidence layers, remaining risks, and pre-submission checks.
- `author_confirmation_needed.md`: unresolved conceptual, normative, evidential, or formatting decisions.

Do not claim acceptance likelihood, authorship detection, or an AI-writing percentage.
