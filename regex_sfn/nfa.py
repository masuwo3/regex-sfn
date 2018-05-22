class NondeterministicFiniteAutomaton:
    def __init__(self, transition, start, accepts):
        self.transition = transition
        self.start = start
        self.accepts = accepts

    def epsilon_expand(self, set_):
        que = set(set_)
        done = set()
        while que:
            stat = que.pop()
            nexts = self.transition(stat, "")
            done.add(stat)
            for next_stat in nexts:
                if not next_stat in done:
                    que.add(next_stat)

        return frozenset(done)
