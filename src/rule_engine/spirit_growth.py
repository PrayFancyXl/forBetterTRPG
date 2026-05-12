SPIRIT_GROWTH_TABLE = [
    {"level": 10, "reward": "feat_1", "description": "获得一项自选专长"},
    {"level": 12, "reward": "soul_weapon", "description": "获得你的灵魂武器"},
    {"level": 14, "reward": "ultimate_1", "description": "习得一挡狩魂绝技"},
    {"level": 16, "reward": "feat_2", "description": "获得另一项新的自选专长"},
    {"level": 18, "reward": "ultimate_2", "description": "习得二挡狩魂绝技"},
]


def compute_spirit_unlocks(spirit_awareness: int) -> dict:
    unlocks = {
        "feat_count": 0,
        "has_soul_weapon": False,
        "ultimate_tier_1": False,
        "ultimate_tier_2": False,
    }
    for entry in SPIRIT_GROWTH_TABLE:
        if spirit_awareness >= entry["level"]:
            if entry["reward"] == "feat_1":
                unlocks["feat_count"] = max(unlocks["feat_count"], 1)
            elif entry["reward"] == "feat_2":
                unlocks["feat_count"] = 2
            elif entry["reward"] == "soul_weapon":
                unlocks["has_soul_weapon"] = True
            elif entry["reward"] == "ultimate_1":
                unlocks["ultimate_tier_1"] = True
            elif entry["reward"] == "ultimate_2":
                unlocks["ultimate_tier_2"] = True
    return unlocks
