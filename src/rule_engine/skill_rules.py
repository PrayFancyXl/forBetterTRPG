from ..models.enums import AttributeLevel
from .attribute_rules import get_attribute_value, compute_skill_points

SKILL_NAMES = ["athletics", "operation", "stealth", "investigation", "insight", "persuasion", "hunter_lore"]

SKILL_ATTRIBUTE_MAP = {
    "athletics": "physique",
    "operation": "physique",
    "stealth": "wisdom",
    "investigation": "wisdom",
    "insight": "spirit",
    "persuasion": "spirit",
    "hunter_lore": None,
}

MAX_SKILL_LEVEL = 5


def compute_attribute_bonus(skill_name: str, physique: AttributeLevel, wisdom: AttributeLevel, spirit: AttributeLevel) -> int:
    attr = SKILL_ATTRIBUTE_MAP.get(skill_name)
    if attr == "physique":
        return get_attribute_value(physique)
    elif attr == "wisdom":
        return get_attribute_value(wisdom)
    elif attr == "spirit":
        return get_attribute_value(spirit)
    return 0


def validate_skill_allocation(free_points: dict[str, int], wisdom: AttributeLevel) -> tuple[bool, list[str]]:
    errors = []
    total_budget = compute_skill_points(wisdom)
    total_used = sum(free_points.values())

    if total_used > total_budget:
        errors.append(f"技能点超出预算：已分配{total_used}点，可用{total_budget}点")

    for skill, points in free_points.items():
        if points < 0:
            errors.append(f"{skill}的自由分配点数不能为负")
        if points > MAX_SKILL_LEVEL:
            errors.append(f"{skill}的自由分配点数不能超过{MAX_SKILL_LEVEL}")

    return len(errors) == 0, errors
