from GENESIS.architecture.platform import PLATFORM


class SystemHealth:

    @staticmethod
    def platform():

        return {

            "platform":

                PLATFORM["name"],

            "version":

                PLATFORM["version"],

            "engines":

                len(
                    PLATFORM["engines"]
                ),

            "engineering":

                len(
                    PLATFORM["engineering"]
                )
        }