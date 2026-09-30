import pandas as pd


def create_report(results):
    return pd.DataFrame(results)


def save_report(report, path):

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    report.to_csv(
        path,
        index=False
    )