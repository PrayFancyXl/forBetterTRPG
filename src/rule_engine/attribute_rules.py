from ..models.enums import AttributeLevel, ATTRIBUTE_TABLE


def get_attribute_value(level: AttributeLevel) -> int:
    return ATTRIBUTE_TABLE[level]["value"]


def get_attribute_strength(level: AttributeLevel) -> int:
    return ATTRIBUTE_TABLE[level]["strength"]


def compute_martial_arts_count(physique: AttributeLevel) -> int:
    count_map = {
        AttributeLevel.E: 0,
        AttributeLevel.D: 1,
        AttributeLevel.C: 2,
        AttributeLevel.B: 2,
        AttributeLevel.A: 3,
        AttributeLevel.S: 3,
        AttributeLevel.SS: 4,
        AttributeLevel.SSS: 4,
        AttributeLevel.SSS_PLUS: 5,
    }
    return count_map[physique]


def can_learn_secret_martial(physique: AttributeLevel) -> bool:
    return get_attribute_value(physique) >= 7  # SS+


def compute_spell_count(wisdom: AttributeLevel) -> int:
    count_map = {
        AttributeLevel.E: 0,
        AttributeLevel.D: 2,
        AttributeLevel.C: 4,
        AttributeLevel.B: 4,
        AttributeLevel.A: 6,
        AttributeLevel.S: 6,
        AttributeLevel.SS: 8,
        AttributeLevel.SSS: 8,
        AttributeLevel.SSS_PLUS: 10,
    }
    return count_map[wisdom]


def can_learn_secret_spells(wisdom: AttributeLevel) -> bool:
    return get_attribute_value(wisdom) >= 7  # SS+


def compute_skill_points(wisdom: AttributeLevel) -> int:
    points_map = {
        AttributeLevel.E: 0,
        AttributeLevel.D: 1,
        AttributeLevel.C: 2,
        AttributeLevel.B: 3,
        AttributeLevel.A: 4,
        AttributeLevel.S: 5,
        AttributeLevel.SS: 6,
        AttributeLevel.SSS: 7,
        AttributeLevel.SSS_PLUS: 8,
    }
    return points_map[wisdom]


def compute_spirit_mark_count(spirit: AttributeLevel) -> int:
    value = get_attribute_value(spirit)
    if value >= 5:  # A级及以上额外+1
        return 3
    if value >= 2:  # D级及以上
        return 2
    return 1


def compute_unlocked_info(physique: AttributeLevel, wisdom: AttributeLevel, spirit: AttributeLevel) -> dict:
    return {
        "martial_arts_count": compute_martial_arts_count(physique),
        "can_learn_secret_martial": can_learn_secret_martial(physique),
        "martial_strength": get_attribute_strength(physique),
        "spell_count": compute_spell_count(wisdom),
        "can_learn_secret_spells": can_learn_secret_spells(wisdom),
        "spell_strength": get_attribute_strength(wisdom),
        "skill_points": compute_skill_points(wisdom),
        "spirit_mark_count": compute_spirit_mark_count(spirit),
        "spirit_strength": get_attribute_strength(spirit),
    }
