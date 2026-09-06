"""Evidence-type taxonomy (Phase 2B).

CONTROLLED_TOY: hand-designed analytical substrate (2A).
LEARNED_MODEL_EXPERIMENT: our meta-trained neural substrate (2B).
OUR_REPRODUCTION: rerun of a published setup (reserved).
PUBLISHED_RESULT: paper-reported number (cite only).
OFFICIAL_RESULT: Pathway-released artifact number (cite only).
ILLUSTRATION: conceptual viz, no computational claim.
"""
CONTROLLED_TOY = "CONTROLLED_TOY"
LEARNED_MODEL_EXPERIMENT = "LEARNED_MODEL_EXPERIMENT"
OUR_REPRODUCTION = "OUR_REPRODUCTION"
PUBLISHED_RESULT = "PUBLISHED_RESULT"
OFFICIAL_RESULT = "OFFICIAL_RESULT"
ILLUSTRATION = "ILLUSTRATION"

LEARNED_STRATEGIES = {"learned_state", "learned_tta", "learned_ttt"}


def evidence_for(strategies):
    if any(s in LEARNED_STRATEGIES for s in strategies):
        return LEARNED_MODEL_EXPERIMENT
    return CONTROLLED_TOY
