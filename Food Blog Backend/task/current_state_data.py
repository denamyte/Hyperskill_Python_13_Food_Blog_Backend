from dao.recipe_dao import RecipeDao
from dao.recipe_item import RecipeItem


class RecipeDataFacade:

    def __init__(self, recipe_dao: RecipeDao):
        self.recipe_dao = recipe_dao
        self._recipe: RecipeItem = RecipeItem()

    def set_name(self, name: str):
        self._recipe.name = name

    def set_desc(self, desc: str):
        self._recipe.desc = desc

    def save_recipe(self):
        self.recipe_dao.save_recipe(self._recipe)
        self._recipe = RecipeItem()
