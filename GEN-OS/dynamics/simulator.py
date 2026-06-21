#Самое главное.
from .calculator import Calculator


class Simulator:

    def __init__(self):

        self.calculator=Calculator()

    def simulate(

        self,

        state,

        actions

    ):

        for action in actions:

            state=self.calculator.apply(

                state,

                action.effect

            )

        return state