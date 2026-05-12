import json
from pathlib import Path
from typing import Optional

from ..config import settings


class KnowledgeBase:
    def __init__(self):
        self.attributes: dict = {}
        self.skills: dict = {}
        self.martial_arts: list[dict] = []
        self.spells: list[dict] = []
        self.spirit_marks: list[dict] = []
        self.feats: list[dict] = []
        self.ultimates: list[dict] = []
        self.stylish_moves: dict = {}
        self.effects: list[dict] = []
        self.card_template: dict = {}
        self.rules_graph: dict = {}

    def load(self, knowledge_dir: Optional[Path] = None):
        base = knowledge_dir or settings.KNOWLEDGE_DIR
        self.attributes = self._load_json(base / "attributes.json")
        self.skills = self._load_json(base / "skills.json")
        self.martial_arts = self._load_json(base / "martial_arts.json")
        self.spells = self._load_json(base / "spells.json")
        self.spirit_marks = self._load_json(base / "spirit_marks.json")
        self.feats = self._load_json(base / "feats.json")
        self.ultimates = self._load_json(base / "ultimates.json")
        self.stylish_moves = self._load_json(base / "stylish_moves.json")
        self.effects = self._load_json(base / "effects.json")
        self.card_template = self._load_json(base / "card_template.json")
        self.rules_graph = self._load_json(base / "rules_graph.json")

    def _load_json(self, path: Path):
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        return {}

    def get_available_martial_arts(self, can_secret: bool = False) -> list[dict]:
        if can_secret:
            return self.martial_arts
        return [a for a in self.martial_arts if not a.get("secret", False)]

    def get_available_spells(self, can_secret: bool = False, category: Optional[str] = None) -> list[dict]:
        result = self.spells
        if not can_secret:
            result = [s for s in result if not s.get("secret", False)]
        if category:
            result = [s for s in result if s.get("category") == category]
        return result

    def get_available_ultimates(self, tier: Optional[str] = None) -> list[dict]:
        if tier:
            return [u for u in self.ultimates if u.get("tier") == tier]
        return self.ultimates


knowledge = KnowledgeBase()
