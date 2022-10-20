from typing import Dict, Callable


class StateTransition:
    """
    Contains information about one of the possible states of the application:
    its name, the dictionary of possible next states, and the means
    to switch the state from the current state to a possible state.
    """
    def __init__(self, state: str, input_to_state_dict: Dict[int, str], input_generator: Callable[[], int]):
        """
        Creates an instance of a state switcher.

        :param state: The current state
        :param input_to_state_dict: the dictionary of the predefined state names
        which current state can be switched to
        :param input_generator: The function for generating one of input_to_state_dict keys
        """
        self._state = state
        self._input_to_state_dict = input_to_state_dict
        self._input_generator = input_generator

    def next_state(self) -> str:
        """
        Generates the key and returns the corresponding value
        (the name of one of the possible next states)
        """
        return self._input_to_state_dict.get(self._input_generator())

    @property
    def state_name(self):
        return self._state
