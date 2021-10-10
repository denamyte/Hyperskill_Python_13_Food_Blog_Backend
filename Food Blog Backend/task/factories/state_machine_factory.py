from enum import Enum, auto
from typing import Dict

from ..state.state_transition import StateTransition
from ..state.state_switcher import StateSwitcher


class State(Enum):
    WELCOME_MSG = auto()
    ENTER_RECIPE_NAME = auto()
    ENTER_RECIPE_DESC = auto()


class StateMachineFactory:

    def __init__(self):
        ...

    @staticmethod
    def get_state_dict() -> Dict[str, StateTransition]:
        ...
