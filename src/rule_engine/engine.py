from ..models.character import CharacterCard
from ..models.creation_state import ValidationResult
from ..models.enums import CreationStep
from .attribute_rules import compute_unlocked_info
from .spirit_growth import compute_spirit_unlocks
from .skill_rules import validate_skill_allocation


def validate_step(character: CharacterCard, step: CreationStep) -> ValidationResult:
    if step == CreationStep.SPIRIT_POWER:
        return _validate_spirit_power(character)
    elif step == CreationStep.BOND:
        return _validate_bond(character)
    elif step == CreationStep.CHARACTER_INFO:
        return _validate_character_info(character)
    elif step == CreationStep.ATTRIBUTES:
        return _validate_attributes(character)
    elif step == CreationStep.SKILLS:
        return _validate_skills(character)
    elif step == CreationStep.ABILITIES:
        return _validate_abilities(character)
    return ValidationResult()


def _validate_spirit_power(character: CharacterCard) -> ValidationResult:
    errors = []
    warnings = []
    sp = character.spirit_power

    if not sp.name:
        errors.append("灵能力名称不能为空")
    if not sp.description:
        errors.append("灵能力描述不能为空")
    if len(sp.description) > 80:
        errors.append(f"灵能力描述不能超过80字（当前{len(sp.description)}字）")
    if len(sp.tags) > 3:
        errors.append("灵能力标签最多3个")
    if len(sp.tags) == 0:
        warnings.append("建议至少设置1个灵能力标签")

    return ValidationResult(valid=len(errors) == 0, errors=errors, warnings=warnings)


def _validate_bond(character: CharacterCard) -> ValidationResult:
    errors = []
    if not character.basic_info.bond:
        errors.append("请选择一项狩魂者羁绊")
    return ValidationResult(valid=len(errors) == 0, errors=errors)


def _validate_character_info(character: CharacterCard) -> ValidationResult:
    errors = []
    warnings = []
    info = character.basic_info

    if not info.name:
        errors.append("姓名不能为空")
    if not info.codename:
        errors.append("代号不能为空")
    if not info.backstory:
        warnings.append("建议填写背景故事")

    return ValidationResult(valid=len(errors) == 0, errors=errors, warnings=warnings)


def _validate_attributes(character: CharacterCard) -> ValidationResult:
    errors = []
    warnings = []
    attrs = character.attributes

    unlocked = compute_unlocked_info(attrs.physique, attrs.wisdom, attrs.spirit)

    if unlocked["can_learn_secret_martial"]:
        warnings.append("体魄SS级及以上：可学习秘传武技")
    if unlocked["can_learn_secret_spells"]:
        warnings.append("智慧SS级及以上：可学习秘传术法")

    return ValidationResult(valid=len(errors) == 0, errors=errors, warnings=warnings, unlocked=unlocked)


def _validate_skills(character: CharacterCard) -> ValidationResult:
    skills = character.skills
    free_points = {
        "athletics": skills.athletics.free_points,
        "operation": skills.operation.free_points,
        "stealth": skills.stealth.free_points,
        "investigation": skills.investigation.free_points,
        "insight": skills.insight.free_points,
        "persuasion": skills.persuasion.free_points,
        "hunter_lore": skills.hunter_lore.free_points,
    }
    valid, errors = validate_skill_allocation(free_points, character.attributes.wisdom)
    return ValidationResult(valid=valid, errors=errors)


def _validate_abilities(character: CharacterCard) -> ValidationResult:
    errors = []
    warnings = []
    attrs = character.attributes
    unlocked = compute_unlocked_info(attrs.physique, attrs.wisdom, attrs.spirit)
    spirit_unlocks = compute_spirit_unlocks(character.resources.spirit_awareness)

    martial_count = len(character.martial_arts)
    max_martial = unlocked["martial_arts_count"]
    if martial_count > max_martial:
        errors.append(f"武技数量超出上限：已选{martial_count}个，最多{max_martial}个")

    for art in character.martial_arts:
        if art.secret and not unlocked["can_learn_secret_martial"]:
            errors.append(f"体魄未达SS级，无法学习秘传武技「{art.name}」")

    spell_count = len(character.spells)
    max_spells = unlocked["spell_count"]
    if spell_count > max_spells:
        errors.append(f"术法数量超出上限：已选{spell_count}个，最多{max_spells}个")

    for spell in character.spells:
        if spell.secret and not unlocked["can_learn_secret_spells"]:
            errors.append(f"智慧未达SS级，无法学习秘传术法「{spell.name}」")

    feat_count = len(character.feats)
    max_feats = spirit_unlocks["feat_count"]
    if feat_count > max_feats:
        errors.append(f"专长数量超出上限：已选{feat_count}个，灵识等级允许{max_feats}个")

    if character.soul_weapon and not spirit_unlocks["has_soul_weapon"]:
        errors.append("灵识未达12级，尚未获得灵魂武器")

    for ult in character.ultimates:
        if ult.tier == "一挡" and not spirit_unlocks["ultimate_tier_1"]:
            errors.append("灵识未达14级，无法习得一挡绝技")
        if ult.tier == "二挡" and not spirit_unlocks["ultimate_tier_2"]:
            errors.append("灵识未达18级，无法习得二挡绝技")

    mark_count = len(character.spirit_marks)
    max_marks = unlocked["spirit_mark_count"]
    if mark_count > max_marks:
        errors.append(f"灵能印记数量超出上限：已选{mark_count}个，最多{max_marks}个")

    return ValidationResult(valid=len(errors) == 0, errors=errors, warnings=warnings)
