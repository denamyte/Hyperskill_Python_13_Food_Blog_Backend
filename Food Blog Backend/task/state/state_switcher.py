from typing import Dict

from state_transition import StateTransition


class StateSwitcher:
    """todo make documentation here"""
    def __init__(self, transition_dict: Dict[str, StateTransition], initial_state: str):
        self._transition_dict = transition_dict
        self._state = initial_state

    def run(self):
        while len(self._state):
            self._state = self._transition_dict.get(self._state).next_state()

    # def state_valid(self):
    #     return self._state is not None and len(self._state)
