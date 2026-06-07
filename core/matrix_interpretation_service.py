class MatrixInterpretationService:

    @staticmethod
    def get_cell_status(matrix, num_str):
        val = matrix.get(
            num_str,
            ''
        )
        if not val:
            return "Не проявлено"
        if len(val) <= 2:
            return f"Норма ({len(val)})"
        return f"Усилено ({len(val)})"