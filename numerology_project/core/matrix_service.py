from utils import (
    calculate_full_matrix_logic,
    sum_digits
)


class MatrixService:

    @staticmethod
    def build(day, month, year):
        matrix, *_ = calculate_full_matrix_logic(
            day,
            month,
            year
        )

        destiny_number = str(
            sum_digits(
                day + month + year
            )
        )

        return matrix, destiny_number
