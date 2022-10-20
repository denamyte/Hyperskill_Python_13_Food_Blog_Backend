from dao.recipe_dao import RecipeDao
from dao.recipe_item import RecipeItem


class CurrentStateDataFacade:

    def __init__(self, recipe_dao: RecipeDao):
        self.recipe_dao = recipe_dao
        self._recipe_name = ''

    def set_name(self, name: str):
        self._recipe_name = name

    def set_desc(self, desc: str):
        item = RecipeItem(self._recipe_name, desc)
        self.recipe_dao.save_recipe(item)
