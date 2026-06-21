"""
GENESIS HR®

State Validator
"""


class StateValidator:

    @staticmethod
    def validate(variable):
        return (
                variable.minimum
                <=
                variable.value
                <=
                variable.maximum
        )
