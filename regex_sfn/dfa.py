class DeterministicFiniteAutomaton:
    def __init__(self, transition, start, accepts):
        self.transition = transition
        self.start = start
        self.accepts = accepts

    def get_runtime(self):
        return DFARuntime(self)

class DFARuntime:
    def __init__(self, dfa):
        self.dfa = dfa
        self.cur_state = self.dfa.start

    def do_transition(self, char):
        self.cur_state = self.dfa.transition(self.cur_state, char)

    def is_accept_state(self):
        return self.cur_state in self.dfa.accepts

    def does_accept(self, input_str):
        for alphabet in input_str:
            self.do_transition(alphabet)
        return self.is_accept_state()
