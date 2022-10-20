from typing import Dict

from state_transition import StateTransition


class StateSwitcher:
    """
    A class for switching states for the State Machin implementation
    until the current state become a terminal one
    """
    def __init__(self, transition_dict: Dict[str, StateTransition], initial_state: str):
        self._transition_dict = transition_dict
        self._state = initial_state

    def run(self):
        while len(self._state):
            self._state = self._transition_dict.get(self._state).next_state()
