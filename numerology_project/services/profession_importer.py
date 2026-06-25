import pandas as pd


def preview_excel(path):
    df = pd.read_excel(path)
    return {
        "rows": len(df),
        "columns": list(df.columns),
        "preview":
            df.head(20)
            .to_dict(
                orient='records'
            )
    }
