from sys import argv

from ini_db import ini_db
from dao.recipe_dao import RecipeDao
from food_blog_menus import FoodBlogMenus
from state_machine_factory import StateMachineFactory, State
from state.state_machine import StateMachineRunner

if __name__ == '__main__':
    _, db_name = argv
    ini_db(db_name)

    recipe_dao = RecipeDao(db_name)
    food_blog_menus = FoodBlogMenus(recipe_dao)
    state_dict = StateMachineFactory(food_blog_menus).get_state_dict()
    initial_state = State.WELCOME_MSG.name
    smr = StateMachineRunner(state_dict, initial_state)

    smr.run()
