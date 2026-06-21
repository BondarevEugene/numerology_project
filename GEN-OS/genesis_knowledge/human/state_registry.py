"""
GENESIS HR®

State Registry
"""

class StateRegistry:

    def __init__(self):

        self.variables={}

    def add(self,variable):

        self.variables[

            variable.code

        ]=variable

    def get(self,code):

        return self.variables.get(code)

    def all(self):

        return list(

            self.variables.values()

        )