from typing import List

from dao.recipe_dao import RecipeDao, RecipeItem


def blog_search(db_name: str, ingredients: List[str], meals: List[str]):
    dao = RecipeDao(db_name)
    recipes = dao.get_recipes_by_ingredients_and_meals_names(ingredients, meals)
    if recipes:
        r_list = ', '.join(r.name for r in recipes)
        print('Recipes selected for you:', r_list)
    else:
        print('There are no such recipes in the database.')
