from abc import ABC, abstractmethod
from recipe_item import RecipeItem


class RecipeDao(ABC):

    @abstractmethod
    def save_recipe(self, recipe_item: RecipeItem):
        ...
