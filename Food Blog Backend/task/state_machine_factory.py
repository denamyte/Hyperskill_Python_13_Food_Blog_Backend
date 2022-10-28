from enum import Enum, auto
from typing import Dict

from state.state_transition import StateTransition
from food_blog_menus import FoodBlogMenus


class State(Enum):
    WELCOME_MSG = auto()
    ENTER_RECIPE_NAME = auto()
    ENTER_RECIPE_DESC = auto()
    ENTER_MEALS_NUMBERS_FOR_DISH = auto()
    ENTER_INGREDIENTS_QUANTITY = auto()

    EXIT = auto()


class StateMachineFactory:

    def __init__(self, menus: FoodBlogMenus):
        self._menus = menus

    def get_state_dict(self) -> Dict[str, StateTransition]:
        trans_list = [
            StateTransition(State.ENTER_RECIPE_NAME.name,
                            {0: State.EXIT.name,
                             1: State.ENTER_RECIPE_DESC.name},
                            self._menus.read_recipe_name),

            StateTransition(State.ENTER_RECIPE_DESC.name,
                            {0: State.ENTER_MEALS_NUMBERS_FOR_DISH.name},
                            self._menus.read_recipe_desc),

            StateTransition(State.ENTER_MEALS_NUMBERS_FOR_DISH.name,
                            {0: State.ENTER_INGREDIENTS_QUANTITY.name},
                            self._menus.read_meals_for_dish),

            StateTransition(State.ENTER_INGREDIENTS_QUANTITY.name,
                            {0: State.ENTER_RECIPE_NAME.name,
                             1: State.ENTER_INGREDIENTS_QUANTITY.name},
                            self._menus.read_quantity),

            StateTransition(State.EXIT.name,
                            {0: ''},
                            lambda: 0)

        ]
        return {st.state_name: st for st in trans_list}

