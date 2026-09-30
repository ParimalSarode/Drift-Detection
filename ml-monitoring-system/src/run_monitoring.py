from pathlib import Path

from src.data.loader import load_csv
from src.drift.detector import check_all_features
from src.drift.report import create_report, save_report


BASE_DIR = Path(__file__).resolve().parent.parent

REFERENCE_PATH = (
    BASE_DIR
    / "data"
    / "reference"
    / "reference_data.csv"
)

PRODUCTION_PATH = (
    BASE_DIR
    / "data"
    / "production"
    / "production_data.csv"
)

REPORT_PATH = (
    BASE_DIR
    / "reports"
    / "drift_report.csv"
)


FEATURES = [
    "Customer_Age",
    "Credit_Limit",
    "Total_Trans_Amt",
    "Total_Trans_Ct",
    "Avg_Utilization_Ratio"
]


def main():

    if not REFERENCE_PATH.exists():
        raise FileNotFoundError(
            "Reference data does not exist.\n"
            "Run prepare_data.py first."
        )

    if not PRODUCTION_PATH.exists():
        raise FileNotFoundError(
            "Production data does not exist.\n"
            "Run prepare_data.py first."
        )

    print("Loading data...")

    reference = load_csv(
        REFERENCE_PATH
    )

    production = load_csv(
        PRODUCTION_PATH
    )

    print("Running drift detection...")

    results = check_all_features(
        reference,
        production,
        FEATURES
    )

    report = create_report(results)

    save_report(
        report,
        REPORT_PATH
    )

    print()
    print("DRIFT REPORT")
    print("=" * 70)
    print(report.to_string(index=False))
    print()
    print(f"Report saved to: {REPORT_PATH}")


if __name__ == "__main__":
    main()