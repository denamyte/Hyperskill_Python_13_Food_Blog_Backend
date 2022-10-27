from dao.recipe_dao import RecipeDao, RecipeItem, ServeItem, QuantityItem


class FoodBlogMenus:
    def __init__(self, recipe_dao: RecipeDao):
        self._recipe_dao = recipe_dao
        self._current_recipe = RecipeItem()
        self._saved_recipe_id = 0
        meal_items = recipe_dao.read_meal_items()
        self._serve_dish_for_meal_prompt = '  '.join(f'{meal.id}) {meal.name}' for meal in meal_items)

    def welcome_msg(self) -> int:
        print('Pass the empty recipe name to exit.')
        return 0

    def read_recipe_name(self) -> int:
        name = input('Recipe name: ')
        if not name:
            return 0
        self._current_recipe.name = name
        return 1

    def read_recipe_desc(self) -> int:
        self._current_recipe.description = input('Recipe description: ')
        self._saved_recipe_id = self._recipe_dao.save_recipe(self._current_recipe)
        self._current_recipe = RecipeItem()
        return 0

    def read_meals_for_dish(self) -> int:
        raw = input(self._serve_dish_for_meal_prompt +
                    '\nWhen the dish can be served: ')
        meal_ids = [int(meal_id) for meal_id in raw.split()]
        serve_items = [ServeItem(recipe_id=self._saved_recipe_id, meal_id=meal_id) for meal_id in meal_ids]
        self._recipe_dao.save_serve_items(serve_items)
        return 0

    def read_quantity(self) -> int:
        raw = input('Input quantity of ingredient <press enter to stop>: ')
        if not raw:
            return 0
        q_list = raw.split()
        [q, m, i] = q_list if len(q_list) == 3 else [q_list[0], '', q_list[1]]

        measure = self._recipe_dao.get_measure_by_name(m)
        if not measure:
            return self.print_not_conclusive_error('measure')

        ingredient = self._recipe_dao.get_ingredient_by_name(i)
        if not ingredient:
            return self.print_not_conclusive_error('ingredient')

        q_item = QuantityItem(quantity=int(q),
                              recipe_id=self._saved_recipe_id,
                              measure_id=measure.id,
                              ingredient_id=ingredient.id)
        self._recipe_dao.save_quantity_item(q_item)
        return 1

    @staticmethod
    def print_not_conclusive_error(name) -> int:
        print(f'The {name} is not conclusive!')
        return 1
