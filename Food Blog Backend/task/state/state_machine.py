from typing import Dict

from .state_transition import StateTransition


class StateMachineRunner:
    """
    A class for switching states, for the State Machine implementation,
    until the current state becomes a terminal one
    """
    def __init__(self, transition_dict: Dict[str, StateTransition], initial_state: str):
        self._transition_dict = transition_dict
        self._state = initial_state

    def run(self):
        while len(self._state):
            self._state = self._transition_dict.get(self._state).next_state()
