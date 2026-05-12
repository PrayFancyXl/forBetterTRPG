from enum import Enum


class AttributeLevel(str, Enum):
    E = "E"
    D = "D"
    C = "C"
    B = "B"
    A = "A"
    S = "S"
    SS = "SS"
    SSS = "SSS"
    SSS_PLUS = "SSS+"


ATTRIBUTE_TABLE = {
    AttributeLevel.E: {"value": 1, "strength": 0},
    AttributeLevel.D: {"value": 2, "strength": 1},
    AttributeLevel.C: {"value": 3, "strength": 1},
    AttributeLevel.B: {"value": 4, "strength": 2},
    AttributeLevel.A: {"value": 5, "strength": 2},
    AttributeLevel.S: {"value": 6, "strength": 3},
    AttributeLevel.SS: {"value": 7, "strength": 3},
    AttributeLevel.SSS: {"value": 8, "strength": 4},
    AttributeLevel.SSS_PLUS: {"value": 9, "strength": 4},
}


class CreationStep(int, Enum):
    SPIRIT_POWER = 1
    BOND = 2
    CHARACTER_INFO = 3
    ATTRIBUTES = 4
    SKILLS = 5
    ABILITIES = 6


class SpellCategory(str, Enum):
    BASIC = "基础"
    TALISMAN = "符箓"
    OTHER = "其他"


class UltimateTier(str, Enum):
    TIER_1 = "一挡"
    TIER_2 = "二挡"
