from pythagoras.analyser import PersonalityAdvancedAnalyser


class PersonalityService:

    @staticmethod
    def analyze(matrix):

        analyser = PersonalityAdvancedAnalyser(
            matrix
        )

        return analyser.get_full_analysis()