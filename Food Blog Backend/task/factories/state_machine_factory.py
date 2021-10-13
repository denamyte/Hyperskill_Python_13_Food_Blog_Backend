from enum import Enum, auto
from typing import Dict

from ..state.state_transition import StateTransition
from ..food_blog_menus import FoodBlogMenus


class State(Enum):
    WELCOME_MSG = auto()
    ENTER_RECIPE_NAME = auto()
    ENTER_RECIPE_DESC = auto()

    EXIT = auto()


class StateMachineFactory:

    def __init__(self, menus: FoodBlogMenus):
        self._menus = menus

    def get_state_dict(self) -> Dict[str, StateTransition]:
        trans_list = [
            StateTransition(State.WELCOME_MSG.name,
                            {0: State.ENTER_RECIPE_NAME.name},
                            self._menus.welcome_msg),

            StateTransition(State.ENTER_RECIPE_NAME.name,
                            {1: State.ENTER_RECIPE_DESC.name,
                             0: State.EXIT.name},
                            self._menus.read_recipe_name),

            StateTransition(State.ENTER_RECIPE_DESC.name,
                            {0: State.ENTER_RECIPE_NAME.name},
                            self._menus.read_recipe_desc)

        ]
        return {st.state_name: st for st in trans_list}

