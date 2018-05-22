class NonDisjointSets:
    def __init__(self, sub):
        self.sub = sub
    def __contains__(self, a_set):
        return a_set & self.sub
