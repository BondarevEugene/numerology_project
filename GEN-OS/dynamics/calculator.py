#Математика изменений.
class Calculator:

    def apply(

        self,

        state,

        effect

    ):

        for modifier in effect.modifiers:

            state.variables[modifier.variable]=(

                state.variables.get(

                    modifier.variable,

                    0

                )+modifier.delta

            )

        return state