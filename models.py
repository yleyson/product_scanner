from dataclasses import dataclass
from typing import List


@dataclass
class IngredientResponse:
    ingredient: str # ingredient name
    found: bool # ingredient have description or not
    description: str = ""
    maybe: List[str] = None # list of choice to ingredient that doesnt have description

    def to_dict(self) -> dict:
        return {
            "ingredient": self.ingredient,
            "found": self.found,
            "description": self.description,
            "maybe": self.maybe
        }
