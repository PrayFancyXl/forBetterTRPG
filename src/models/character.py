from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

from .enums import AttributeLevel, UltimateTier


class SpiritPower(BaseModel):
    name: str = ""
    description: str = Field("", max_length=80)
    tags: list[str] = Field(default_factory=list, max_length=3)
    weakness_tag: str = ""
    specializations: list[str] = Field(default_factory=list, max_length=2)


class BasicInfo(BaseModel):
    name: str = ""
    codename: str = ""
    gender: str = ""
    age: str = ""
    bond: str = ""
    karma_tags: list[str] = Field(default_factory=list)
    backstory: str = ""
    appearance: str = ""
    experience_tags: list[str] = Field(default_factory=list)


class Attributes(BaseModel):
    physique: AttributeLevel = AttributeLevel.E
    wisdom: AttributeLevel = AttributeLevel.E
    spirit: AttributeLevel = AttributeLevel.E


class Resources(BaseModel):
    hp_max: int = 0
    hp_current: int = 0
    spirit_power_max: int = 0
    spirit_power_current: int = 0
    stylish_points: int = 10
    item_points: int = 3
    exp: int = 0
    spirit_awareness: int = 10


class SkillEntry(BaseModel):
    attribute_bonus: int = 0
    free_points: int = 0

    @property
    def total(self) -> int:
        return self.attribute_bonus + self.free_points


class Skills(BaseModel):
    athletics: SkillEntry = Field(default_factory=SkillEntry)
    operation: SkillEntry = Field(default_factory=SkillEntry)
    stealth: SkillEntry = Field(default_factory=SkillEntry)
    investigation: SkillEntry = Field(default_factory=SkillEntry)
    insight: SkillEntry = Field(default_factory=SkillEntry)
    persuasion: SkillEntry = Field(default_factory=SkillEntry)
    hunter_lore: SkillEntry = Field(default_factory=SkillEntry)


class MartialArtSelection(BaseModel):
    name: str
    cost: str = ""
    target: str = ""
    assist: bool = False
    secret: bool = False
    effect: str = ""
    flavor: str = ""


class SpellSelection(BaseModel):
    name: str
    cost: str = ""
    target: str = ""
    category: str = ""
    secret: bool = False
    spell_type: str = ""
    effect: str = ""
    flavor: str = ""


class SpiritMark(BaseModel):
    mark_type: str = ""
    corresponding_soul: str = ""


class SoulWeapon(BaseModel):
    name: str = ""
    marks: list[SpiritMark] = Field(default_factory=list)
    description: str = ""


class Ultimate(BaseModel):
    name: str = ""
    soul: str = ""
    domain: str = ""
    effect: str = ""
    description: str = ""
    tier: UltimateTier = UltimateTier.TIER_1


class Feat(BaseModel):
    name: str = ""
    description: str = ""


class StylishMove(BaseModel):
    style: str = ""
    cost: str = ""
    action: str = ""


class CharacterCard(BaseModel):
    spirit_power: SpiritPower = Field(default_factory=SpiritPower)
    basic_info: BasicInfo = Field(default_factory=BasicInfo)
    attributes: Attributes = Field(default_factory=Attributes)
    resources: Resources = Field(default_factory=Resources)
    skills: Skills = Field(default_factory=Skills)
    martial_arts: list[MartialArtSelection] = Field(default_factory=list)
    spells: list[SpellSelection] = Field(default_factory=list)
    spirit_marks: list[SpiritMark] = Field(default_factory=list, max_length=4)
    soul_weapon: Optional[SoulWeapon] = None
    ultimates: list[Ultimate] = Field(default_factory=list)
    feats: list[Feat] = Field(default_factory=list, max_length=2)
    stylish_moves: list[StylishMove] = Field(default_factory=list)
