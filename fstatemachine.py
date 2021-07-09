__version__ = '1.0.0'


class WrongTransition(Exception):
    pass


class StateMachine:
    def __init__(self, current, states, transitions):
        self.current = current
        self.states = list(states)
        self.transitions = parse_transitions(self.states, transitions)

    def check(self, new):
        if new not in self.states:
            raise ValueError(f'Unknown state: {new}')

        if self.current == new:
            return

        if new not in self.transitions.get(self.current, []):
            raise WrongTransition(new)


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
