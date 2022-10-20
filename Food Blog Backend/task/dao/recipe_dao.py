from abc import ABC, abstractmethod
from recipe_item import RecipeItem


class RecipeDao(ABC):

    #todo Implement the method
    @abstractmethod
    def save_recipe(self, recipe_item: RecipeItem):
        print(f'Debug message: a recipe saved: {recipe_item}')


