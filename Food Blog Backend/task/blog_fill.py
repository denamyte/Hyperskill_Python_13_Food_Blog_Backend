from dao.recipe_dao import RecipeDao
from food_blog_menus import FoodBlogMenus
from state_machine_factory import StateMachineFactory, State
from state.state_machine import StateMachineRunner


def blog_fill(db_name: str):
    recipe_dao = RecipeDao(db_name)
    food_blog_menus = FoodBlogMenus(recipe_dao)
    state_dict = StateMachineFactory(food_blog_menus).get_state_dict()
    initial_state = State.ENTER_RECIPE_NAME.name
    smr = StateMachineRunner(state_dict, initial_state)

    smr.run()
