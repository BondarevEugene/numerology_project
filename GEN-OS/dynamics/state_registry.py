class StateRegistry:

    def __init__(self):

        self.states=[]

    def save(self,state):

        self.states.append(state)

    def latest(self):

        if not self.states:

            return None

        return self.states[-1]