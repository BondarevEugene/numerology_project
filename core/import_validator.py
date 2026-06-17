class ImportValidator:

    @staticmethod
    def validate_profession(row):

        errors = []

        if not row.get("title"):
            errors.append(
                "Title is required"
            )

        return errors