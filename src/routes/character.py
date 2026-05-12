from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from ..models.character import CharacterCard
from ..models.creation_state import CreationSession, ValidationResult
from ..models.enums import CreationStep
from ..rule_engine.engine import validate_step

router = APIRouter(prefix="/api/sessions", tags=["sessions"])

sessions: dict[str, CreationSession] = {}


class StepData(BaseModel):
    data: dict


@router.post("", response_model=CreationSession)
def create_session():
    session = CreationSession()
    sessions[session.id] = session
    return session


@router.get("/{session_id}", response_model=CreationSession)
def get_session(session_id: str):
    session = sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.put("/{session_id}/steps/{step}")
def submit_step(session_id: str, step: int, body: StepData):
    session = sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    creation_step = CreationStep(step)
    _apply_step_data(session, creation_step, body.data)

    result = validate_step(session.character, creation_step)
    session.validation_results[step] = result

    if result.valid and creation_step not in session.completed_steps:
        session.completed_steps.append(creation_step)
        if step < 6:
            session.current_step = CreationStep(step + 1)

    return {"validation": result, "session": session}


def _apply_step_data(session: CreationSession, step: CreationStep, data: dict):
    card = session.character

    if step == CreationStep.SPIRIT_POWER:
        card.spirit_power.name = data.get("name", card.spirit_power.name)
        card.spirit_power.description = data.get("description", card.spirit_power.description)
        card.spirit_power.tags = data.get("tags", card.spirit_power.tags)
        card.spirit_power.weakness_tag = data.get("weakness_tag", card.spirit_power.weakness_tag)
        card.spirit_power.specializations = data.get("specializations", card.spirit_power.specializations)

    elif step == CreationStep.BOND:
        card.basic_info.bond = data.get("bond", card.basic_info.bond)

    elif step == CreationStep.CHARACTER_INFO:
        for field in ["name", "codename", "gender", "age", "backstory", "appearance"]:
            if field in data:
                setattr(card.basic_info, field, data[field])
        if "karma_tags" in data:
            card.basic_info.karma_tags = data["karma_tags"]
        if "experience_tags" in data:
            card.basic_info.experience_tags = data["experience_tags"]

    elif step == CreationStep.ATTRIBUTES:
        if "physique" in data:
            card.attributes.physique = data["physique"]
        if "wisdom" in data:
            card.attributes.wisdom = data["wisdom"]
        if "spirit" in data:
            card.attributes.spirit = data["spirit"]

    elif step == CreationStep.SKILLS:
        skills_data = data.get("skills", {})
        for skill_name, points in skills_data.items():
            if hasattr(card.skills, skill_name):
                entry = getattr(card.skills, skill_name)
                entry.free_points = points

    elif step == CreationStep.ABILITIES:
        if "martial_arts" in data:
            from ..models.character import MartialArtSelection
            card.martial_arts = [MartialArtSelection(**a) for a in data["martial_arts"]]
        if "spells" in data:
            from ..models.character import SpellSelection
            card.spells = [SpellSelection(**s) for s in data["spells"]]
        if "feats" in data:
            from ..models.character import Feat
            card.feats = [Feat(**f) for f in data["feats"]]
        if "spirit_marks" in data:
            from ..models.character import SpiritMark
            card.spirit_marks = [SpiritMark(**m) for m in data["spirit_marks"]]
        if "soul_weapon" in data:
            from ..models.character import SoulWeapon
            card.soul_weapon = SoulWeapon(**data["soul_weapon"])
        if "ultimates" in data:
            from ..models.character import Ultimate
            card.ultimates = [Ultimate(**u) for u in data["ultimates"]]
        if "stylish_moves" in data:
            from ..models.character import StylishMove
            card.stylish_moves = [StylishMove(**s) for s in data["stylish_moves"]]
