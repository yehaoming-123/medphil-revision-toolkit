---
name: journal-router
description: Use when the target journal is undecided among MHCP, JME, Bioethics, and JMP, or when manuscript fit needs comparison before revision.
---

# Journal Router

Compare journal fit without predicting editorial decisions. Evaluate MHCP, JME, Bioethics, and JMP independently.

## Inputs

Extract the manuscript's title, abstract, article type, central problem, thesis, method of argument, clinical or policy connection, and key concepts. Ask for missing information only when the manuscript does not supply it.

## Evidence loading

For each journal, read `../../journal-packs/<id>/profile.yaml` and `source_registry.md`. Load `official_requirements.md` and `editorial_profile.md` only when their detail affects the recommendation.

Use these evidence labels exactly:

- `official_requirement`
- `observed_tendency`
- `editorial_inference`
- `abstract_limited`

Never merge an editorial inference into an official requirement. Treat stale sources as needing re-verification.

## Routing method

1. Compare scope, article type, philosophical depth, clinical relevance, policy relevance, and intended readership.
2. Record positive signals and mismatch reasons for every journal, including the leading candidate.
3. Rank all four journals. Use the offline router only as a transparent regression aid; perform the final judgment from the manuscript and sourced journal profiles.
4. Explain close calls, especially MHCP versus JMP and JME versus Bioethics.
5. Never provide an acceptance probability or use impact factor as the sole criterion.
6. Stop before revision until the author confirms the target.

## Output

Create `journal_routing_report.md` with:

| Rank | Journal | Fit reasons | Mismatch reasons | Evidence limits |
|---:|---|---|---|---|

End with one recommended target, one alternative, and the specific manuscript changes that would alter the ranking.
