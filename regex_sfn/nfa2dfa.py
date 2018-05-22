from regex_sfn.dfa import DeterministicFiniteAutomaton as DFA
from regex_sfn.non_disjoint_sets import NonDisjointSets

def nfa2dfa(nfa):
    def transition(set_, alpha):
        ret = set()
        for elem in set_:
            ret |= nfa.transition(elem, alpha)
        return nfa.epsilon_expand(frozenset(ret))

    return DFA(transition,
               nfa.epsilon_expand(frozenset([nfa.start])),
               NonDisjointSets(nfa.accepts))
