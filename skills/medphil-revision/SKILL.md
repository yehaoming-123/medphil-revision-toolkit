---
name: medphil-revision
description: Use when an English philosophy-of-medicine, bioethics, medical-ethics, or medical-humanities manuscript needs journal selection or revision for MHCP, JME, Bioethics, or JMP.
---

# MedPhil Revision

Revise the manuscript without changing its intellectual ownership. Preserve the author's thesis, citations, factual claims, and original input file.

## Required references

Read `../../references/editorial_safety.md` before editing. Read `../../references/source_policy.md` before using journal evidence. Load only the confirmed target's directory under `../../journal-packs/`.

## Workflow

1. Inspect the input and identify title, abstract, keywords, headings, citations, reference list, tables, notes, and comments.
2. Stop on identifiable patient information, encrypted or damaged files, image-only text, or citation structures that cannot be protected.
3. Build a manuscript profile: article type, central question, thesis, key concepts, descriptive claims, interpretive claims, normative claims, and positions requiring author control.
4. If the target is uncertain, invoke `$journal-router`. Confirm the target journal before loading a journal pack or revising prose.
5. Diagnose fit before rewriting. Separate official requirements, observed tendencies, abstract-limited evidence, and editorial inference.
6. Revise in order: title/abstract/keywords; introduction/core argument/objections/conclusion; remaining high-risk passages.
7. Freeze the reference list and unsafe citation-bearing passages. Do not invent citations, evidence, data, clinical cases, or author experiences.
8. Compare the revised manuscript with the input. Flag thesis drift, stronger causal or empirical claims, citation changes, and unresolved author choices.

## Editing rules

- Preserve the author's thesis unless the author explicitly requests restructuring.
- Keep descriptive, interpretive, empirical, and normative claims distinct.
- Treat examples as illustrations, not empirical proof.
- Do not strengthen clinical, causal, or policy claims beyond the supplied evidence.
- Put any change that may alter the author's position in the confirmation file.
- Never overwrite the original manuscript.

## Required outputs

- `revised_manuscript.docx`: clean revised copy.
- `revision_log.md`: material changes and reasons.
- `journal_routing_report.md`: four-journal comparison, or a note that an existing confirmed route was reused.
- `journal_fit_report.md`: target-journal fit, evidence layers, remaining risks, and pre-submission checks.
- `author_confirmation_needed.md`: unresolved conceptual, normative, evidential, or formatting decisions.

Do not claim acceptance likelihood, authorship detection, or an AI-writing percentage.
