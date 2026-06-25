"""
Genesis CSV Reader
"""

import pandas as pd


class CsvImporter:
    @staticmethod
    def read(path):
        df = pd.read_csv(path)
        return df.to_dict(
            orient="records"
        )