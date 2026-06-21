class ActionRegistry:

    def __init__(self):

        self.actions={}

    def add(self,action):

        self.actions[action.id]=action

    def get(self,code):

        return self.actions.get(code)

    def all(self):

        return list(self.actions.values())