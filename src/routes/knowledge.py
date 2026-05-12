from typing import Optional

from fastapi import APIRouter, Query

from ..services.knowledge_loader import knowledge

router = APIRouter(prefix="/api/knowledge", tags=["knowledge"])


@router.get("/martial-arts")
def get_martial_arts(secret: bool = False):
    return knowledge.get_available_martial_arts(can_secret=secret)


@router.get("/spells")
def get_spells(secret: bool = False, category: Optional[str] = Query(None)):
    return knowledge.get_available_spells(can_secret=secret, category=category)


@router.get("/feats")
def get_feats():
    return knowledge.feats


@router.get("/ultimates")
def get_ultimates(tier: Optional[str] = Query(None)):
    return knowledge.get_available_ultimates(tier=tier)


@router.get("/spirit-marks")
def get_spirit_marks():
    return knowledge.spirit_marks


@router.get("/stylish-moves")
def get_stylish_moves():
    return knowledge.stylish_moves


@router.get("/effects")
def get_effects():
    return knowledge.effects


@router.get("/attributes")
def get_attributes():
    return knowledge.attributes
