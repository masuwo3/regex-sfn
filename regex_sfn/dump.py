import json

class Dumper:
    def __init__(self, dfa):
        self.dfa = dfa
        self.que = set([dfa.start])
        self.done = set()
        self.cur_stat = None
        self.definition = {
            "States": {
                "error": {"Type": "Fail",
                          "Cause": "invalid input"},
                "succeed": {"Type": "Succeed"}
            }
        }

    def dump_sf_definition(self):
        while self.que:
            self.cur_stat = self.que.pop()

            state_name = stat2str(self.cur_stat)

            if self.cur_stat == self.dfa.start:
                self.definition["StartAt"] = state_name

            self.done.add(self.cur_stat)

            transitions = []
            if self.cur_stat in self.dfa.accepts:
                transitions.append(('EOL', 'succeed'))

            for chr_ in alphabet():
                tran = self.do_transition(chr_)
                if tran is not None:
                    transitions.append(tran)

            self.definition["States"][state_name] = create_state(transitions)

        return json.dumps(self.definition)

    def do_transition(self, chr_):
        next_stat = self.dfa.transition(self.cur_stat, chr_)
        if not next_stat:
            return None
        transition = self.transited(chr_, next_stat)

        return transition

    def transited(self, chr_, next_stat):
        transition = (chr_, stat2str(next_stat))
        if next_stat not in self.done:
            self.que.add(next_stat)

        return transition

def create_state(transitions):
    if len(transitions) == 0:
        state = {
            "Type": "Fail",
            "Comment": "No transition"
        }
    else:
        state = {
            "Type": "Choice",
            "OutputPath": "$[1:]",
            "Default": "error"
        }

        choice_rules = []
        for tran in transitions:
            char = tran[0]
            _next = tran[1]
            choice_rules.append({
                "Variable": "$[0]",
                "StringEquals": char,
                "Next": _next
            })
        state["Choices"] = choice_rules

        return state

def stat2str(stat):
    return '-'.join(map(str, stat))

def alphabet():
    return (chr(i) for i in range(0, 0x10000))
