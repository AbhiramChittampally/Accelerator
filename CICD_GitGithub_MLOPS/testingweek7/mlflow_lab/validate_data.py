import csv
from pathlib import Path

DATA_PATH = Path("data/training.csv")


def validate_data() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

    with DATA_PATH.open("r", newline="") as file:
        reader = csv.DictReader(file)

        required_columns = {"x", "y"}

        if not required_columns.issubset(reader.fieldnames or []):
            raise ValueError("CSV must contain x and y columns")

        rows = list(reader)

    if not rows:
        raise ValueError("Dataset cannot be empty")

    for index, row in enumerate(rows, start=2):
        if not row["x"] or not row["y"]:
            raise ValueError(f"Missing value at CSV row {index}")

        try:
            float(row["x"])
            float(row["y"])
        except ValueError as error:
            raise ValueError(f"Non-numeric value at CSV row {index}") from error

    print(f"Data validation successful: {len(rows)} rows")


if __name__ == "__main__":
    validate_data()
