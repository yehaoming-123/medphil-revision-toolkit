# Contributing

Contributions should improve a reusable workflow, a journal pack, deterministic validation, or an authorized evaluation fixture.

## Safety and source requirements

- Use official publisher pages, legal open-access sources, or materials you are authorized to share.
- Do not bypass a paywall or access control.
- Do not commit article full text, unpublished manuscripts, reviewer reports, or identifiable patient information.
- Paraphrase source claims concisely and record the evidence type, URL, verification date, scope, and status.
- Keep official requirements separate from observed tendencies and editorial inference.

## Journal-pack contributions

Every pack must contain the six files defined in `references/journal_pack_schema.md`. Add at least one positive and one negative routing example. Recheck official requirements within 90 days of the contribution date.

Validate a pack with:

```powershell
python scripts/validate_journal_pack.py journal-packs/<journal-id>
```

## Tests

Run the full suite before submitting a change:

```powershell
python -m unittest discover -s evals/tests -v
```

New behavior requires a failing test before implementation. Do not change expected cases merely to hide an incorrect result.

## Skill changes

Keep triggering conditions in YAML frontmatter and workflow instructions in the body. Preserve the evidence labels, author-confirmation gate, reference freeze, and prohibition on acceptance prediction.

## Revision-engine changes

- Update `references/revision_spec_schema.json` and its tests together when the contract changes.
- Keep exact original-text matching and source SHA-256 validation mandatory.
- Do not make citation-bearing, reference, field, hyperlink, drawing, table, or mixed-format paragraphs eligible merely to satisfy an evaluation.
- Add a failing safety test before widening the editable paragraph classes.
- Render any changed DOCX fixture page by page with `scripts/render_docx_qa.py` before submitting.

## Licensing

By contributing, you agree that your contribution is licensed under Apache-2.0. External sources and journal content remain under their original rights.
