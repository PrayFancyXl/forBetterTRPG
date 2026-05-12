from __future__ import annotations

import uuid
from typing import Optional

from pydantic import BaseModel, Field

from .character import CharacterCard
from .enums import CreationStep


class ValidationResult(BaseModel):
    valid: bool = True
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    unlocked: dict = Field(default_factory=dict)


class CreationSession(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    current_step: CreationStep = CreationStep.SPIRIT_POWER
    character: CharacterCard = Field(default_factory=CharacterCard)
    completed_steps: list[CreationStep] = Field(default_factory=list)
    validation_results: dict[int, ValidationResult] = Field(default_factory=dict)
