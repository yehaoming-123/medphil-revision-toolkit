# Controlled Revision Workflow

## Non-negotiable order

1. Strictly inspect the source DOCX.
2. Build the revision inventory and manuscript profile.
3. Route among all four journals or record that a previously confirmed route is reused.
4. Load only the confirmed journal pack and diagnose fit with separated evidence layers.
5. Draft and validate the JSON revision specification.
6. Apply only exact-match eligible paragraph revisions to a new DOCX.
7. Compare protected fields and stop on any violation.
8. Assemble and verify the five-file delivery bundle.
9. Render the revised DOCX and inspect every page before delivery.

## Revision specification rules

- Copy `source_sha256` from the current source manifest.
- Use the stable `paragraph_index` and exact `original_text` from the current inventory.
- Make one auditable change per revision item.
- Use `author_confirmation: true` for any change that may alter the thesis, normative position, evidential strength, clinical implication, or author voice.
- Never create revision items for protected paragraphs.

## Failure behavior

Fail closed when intake, validation, application, protected-field comparison, or rendering fails. Keep the original unchanged, do not substitute a text-only output for the DOCX, and explain the specific blocked element to the user in Chinese.
