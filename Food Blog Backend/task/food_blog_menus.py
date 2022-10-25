from dao.recipe_dao import RecipeDao, RecipeItem, ServeItem


def return_0(fn):
    def wrapper(*args):
        fn(*args)
        return 0

    return wrapper


class FoodBlogMenus:
    def __init__(self, recipe_dao: RecipeDao):
        self._recipe_dao = recipe_dao
        self._current_recipe = RecipeItem()
        self._saved_recipe_id = 0
        meal_items = recipe_dao.read_meal_items()
        self._meal_items_dict = {meal.id: meal for meal in meal_items}
        self._serve_dish_for_meal_prompt = '  '.join(f'{meal.id}) {meal.name}' for meal in meal_items)

    @return_0
    def welcome_msg(self):
        print('Pass the empty recipe name to exit.')

    def read_recipe_name(self) -> int:
        name = input('Recipe name: ')
        if not name:
            return 0
        self._current_recipe.name = name
        return 1

    @return_0
    def read_recipe_desc(self):
        self._current_recipe.description = input('Recipe description: ')
        self._saved_recipe_id = self._recipe_dao.save_recipe(self._current_recipe)
        self._current_recipe = RecipeItem()

    @return_0
    def read_meals_for_dish(self):
        raw = input(self._serve_dish_for_meal_prompt +
                    '\nWhen the dish can be served: ')
        meal_ids = [int(meal_id) for meal_id in raw.split()]
        serve_items = [ServeItem(recipe_id=self._saved_recipe_id, meal_id=meal_id) for meal_id in meal_ids]
        self._recipe_dao.save_serve_items(serve_items)
