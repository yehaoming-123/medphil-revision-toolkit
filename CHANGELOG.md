# Changelog

All notable project changes are recorded here.

## 0.1.0-rc.1 - 2026-07-11

### Added

- Machine-checkable revision-specification schema and validator.
- Safe paragraph inventory with citation, reference, field, hyperlink, drawing, and mixed-format protection.
- Exact-match DOCX revision engine with fail-closed preflight and author-confirmation routing.
- Five-file delivery-bundle builder with Chinese reports and preserved evidence labels.
- Synthetic MHCP end-to-end revision fixture and expected reports.
- Windows-safe DOCX QA renderer using standards-compliant file URIs.

### Verified

- Thirty-nine automated tests pass.
- Synthetic source hash remains unchanged while three eligible paragraphs are revised.
- Citation-bearing introduction paragraphs and the reference list remain frozen.
- The revised DOCX renders to two visually valid pages.

### Limitations

- v0.1 edits only simple eligible paragraphs and does not promise lossless mutation of complex Word objects.
- Public repository publication and marketplace distribution are not yet configured.

## 0.1.0-alpha.2 - 2026-07-11

### Added

- Deterministic DOCX manifests with file hashes, structure counts, headings, citations, and reference fingerprints.
- Conservative identifier screening for email, phone, Chinese national-ID-shaped strings, and MRN markers.
- Immutable working-copy creation with post-copy hash verification.
- Protected-field checks for citations, references, tables, sections, comments, and footnotes.
- Markdown revision logs that omit local absolute paths.
- Synthetic two-page DOCX fixtures and end-to-end regression coverage.

### Verified

- Twenty-three automated tests pass.
- Source and working-copy fixtures each render to two pages with identical per-page hashes.
- Visual inspection found no clipping, overlap, missing glyphs, broken tables, or pagination drift.

### Limitations

- This release does not yet perform model-driven prose revision.
- Pattern-based identifier screening is not proof of semantic de-identification.

## 0.1.0-alpha.1 - 2026-07-11

### Added

- Codex plugin manifest and UI metadata.
- `medphil-revision` and `journal-router` skills.
- MHCP, JME, Bioethics, and JMP journal packs.
- Machine-checkable source provenance and 90-day freshness validation.
- Four-case offline routing regression baseline.
- Editorial safety and source policies.
- Thirteen automated tests.

### Limitations

- This foundation release does not yet edit DOCX files.
- Recent-article corpus profiles remain preliminary editorial inferences until separately sourced.
- Public marketplace distribution is not configured.
