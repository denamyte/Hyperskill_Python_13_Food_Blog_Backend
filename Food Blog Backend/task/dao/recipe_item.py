from dataclasses import dataclass


@dataclass
class RecipeItem:
    id: int = 0
    name: str = ''
    description: str = ''
