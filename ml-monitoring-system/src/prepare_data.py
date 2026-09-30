import pandas as pd
from pathlib import Path


# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

RAW_PATH = BASE_DIR / "data" / "raw" / "BankChurners.csv"

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


FEATURES = [
    "Customer_Age",
    "Credit_Limit",
    "Total_Trans_Amt",
    "Total_Trans_Ct",
    "Avg_Utilization_Ratio"
]


def load_dataset():

    if not RAW_PATH.exists():
        raise FileNotFoundError(
            f"\nDataset not found:\n{RAW_PATH}\n\n"
            "Put BankChurners.csv inside data/raw/"
        )

    return pd.read_csv(RAW_PATH)


def prepare_data(df):

    missing = [
        feature
        for feature in FEATURES
        if feature not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing columns: {missing}"
        )

    data = df[FEATURES].copy()

    data = data.dropna()

    return data


def create_datasets(data):

    data = data.sample(
        frac=1,
        random_state=42
    ).reset_index(drop=True)

    split_index = int(len(data) * 0.8)

    reference = data.iloc[:split_index].copy()

    production = data.iloc[split_index:].copy()

    production["Total_Trans_Amt"] *= 1.5

    return reference, production


def save_datasets(reference, production):

    REFERENCE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    PRODUCTION_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    reference.to_csv(
        REFERENCE_PATH,
        index=False
    )

    production.to_csv(
        PRODUCTION_PATH,
        index=False
    )


def main():

    print("Loading dataset...")

    df = load_dataset()

    print(f"Original rows: {len(df)}")

    data = prepare_data(df)

    print(f"Usable rows: {len(data)}")

    reference, production = create_datasets(data)

    save_datasets(
        reference,
        production
    )

    print()
    print("Data preparation complete.")
    print(f"Reference: {REFERENCE_PATH}")
    print(f"Production: {PRODUCTION_PATH}")


if __name__ == "__main__":
    main()