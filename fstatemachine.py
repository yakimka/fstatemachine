__version__ = '1.0.0'


class WrongTransition(Exception):
    """Wrong Transition Error class"""


empty = object()


class StateMachine:
    """
    StateMachine class

    :param current: initial state of machine
    :param states: list of available states
    :param transitions: dict of transitions between states
        where key is initial state and value is list of legit states for transitions
    """
    def __init__(self, *, current, states, transitions: dict):
        self.states = list(states)
        self.transitions = parse_transitions(self.states, transitions)
        self.current = current

    @property
    def current(self):
        """
        Current state of machine
        """
        return getattr(self, '_current', empty)

    @current.setter
    def current(self, value):
        self.check(value)
        self._current = value

    def check(self, new):
        """
        Check if new state is valid transitions for machine

        :param new: new state for check
        :raises WrongTransition:
        """
        if new not in self.states:
            raise ValueError(f'Unknown state: {new}')

        if self.current is empty or self.current == new:
            return

        if new not in self.transitions.get(self.current, []):
            raise WrongTransition(f'from {self.current} to {new}')


def parse_transitions(states: list, transitions_schema):
    transitions = {}
    known_states = set(states)
    for from_state, to_states in transitions_schema.items():
        if to_states == '__all__':
            to_states = list(known_states - {from_state})
        elif to_states is None:
            continue
        else:
            unknown = set(to_states) - known_states
            if unknown:
                raise ValueError(f'Unknown states: {", ".join(sorted(unknown))}')
        transitions[from_state] = to_states
    return transitions
