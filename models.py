from dataclasses import dataclass
from typing import List


@dataclass
class IngredientResponse:
    ingredient: str
    found: bool
    description: str = ""
    maybe: List[str] = None

    def to_dict(self) -> dict:
        return {
            "ingredient": self.ingredient,
            "found": self.found,
            "description": self.description,
            "maybe": self.maybe
        }
