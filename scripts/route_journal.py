"""Provide a deterministic routing regression aid.

This lexical baseline detects journal-pack configuration regressions. It is not
the final semantic router and must never be treated as an acceptance predictor.
"""

from pathlib import Path

import yaml


def route_text(text, packs_root):
    haystack = text.casefold()
    ranking = []
    for profile_path in sorted(Path(packs_root).glob("*/profile.yaml")):
        profile = yaml.safe_load(profile_path.read_text(encoding="utf-8"))
        positive = [
            term
            for term in profile["fit_signals"]
            if str(term).casefold() in haystack
        ]
        negative = [
            term
            for term in profile["mismatch_signals"]
            if str(term).casefold() in haystack
        ]
        ranking.append(
            {
                "journal": profile["id"],
                "score": (2 * len(positive)) - len(negative),
                "matched_fit_signals": positive,
                "matched_mismatch_signals": negative,
            }
        )
    return sorted(ranking, key=lambda item: (-item["score"], item["journal"]))
