"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®
Excel Preview
BUILD:0071
DESCRIPTION
Предпросмотр Excel
до импорта.
═══════════════════════════════════════════════════════════════════════
"""

import pandas as pd


class ExcelPreview:

    @staticmethod
    def preview(path):
        df = pd.read_excel(path)
        return {
            "columns":
                list(df.columns),
            "rows":
                df.head(25).to_dict(
                    orient="records"
                ),
            "count":
                len(df)

        }