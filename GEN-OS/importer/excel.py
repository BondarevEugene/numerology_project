"""
====================================================
Genesis Excel Reader
====================================================

Читает Excel.
Никакой логики.
Никакой БД.

====================================================
"""

import pandas as pd

class ExcelImporter:

    @staticmethod
    def read(path):
        df = pd.read_excel(path)
        return df.to_dict(
            orient="records"
        )