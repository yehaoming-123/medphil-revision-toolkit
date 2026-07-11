# Journal Pack Schema

Each journal pack contains exactly six required files:

- `profile.yaml`
- `source_registry.md`
- `official_requirements.md`
- `editorial_profile.md`
- `routing_examples.md`
- `eval_cases.yaml`

## `profile.yaml`

Required fields:

- `id`: Lower-case journal identifier.
- `name`: Full journal title.
- `publisher`: Current publisher.
- `scope_summary`: Concise scope statement supported by official sources.
- `article_types`: Supported manuscript types.
- `fit_signals`: Transparent routing terms or concepts.
- `mismatch_signals`: Terms or concepts that reduce fit.
- `official_urls`: HTTPS publisher or journal URLs.
- `checked_at`: Most recent verification date in `YYYY-MM-DD` format.

## `source_registry.md`

Start with YAML front matter containing a `sources` list. Every source contains:

- `claim_id`
- `claim`
- `evidence_type`
- `url`
- `checked_at`
- `applies_to`
- `status`

Allowed evidence types:

- `official_requirement`
- `observed_tendency`
- `editorial_inference`
- `abstract_limited`

Use HTTPS URLs. Recheck official requirements within 90 days. A stale source remains visible but cannot be presented as a confirmed current requirement.

## Content separation

Put only current publisher requirements in `official_requirements.md`. Put corpus observations and tool judgments in `editorial_profile.md`, labeled by evidence type. Do not store article full text or distinctive source wording.
