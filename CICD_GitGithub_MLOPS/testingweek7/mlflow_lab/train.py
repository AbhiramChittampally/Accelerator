import csv
from pathlib import Path

import mlflow

DATA_PATH = Path("data/training.csv")


def load_training_data() -> list[tuple[float, float]]:
    """Load training examples from the versioned CSV dataset."""
    data: list[tuple[float, float]] = []

    with DATA_PATH.open("r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            data.append((float(row["x"]), float(row["y"])))

    if not data:
        raise ValueError("Training dataset is empty")

    return data


def train_model(
    data: list[tuple[float, float]],
    learning_rate: float,
    epochs: int,
) -> tuple[float, float]:
    """Train linear regression using gradient descent."""
    if not data:
        raise ValueError("Training data cannot be empty")
    weight = 0.0

    for _ in range(epochs):
        gradient = 0.0

        for x, y in data:
            prediction = weight * x
            gradient += 2 * x * (prediction - y)

        gradient /= len(data)
        weight -= learning_rate * gradient

    total_loss = 0.0

    for x, y in data:
        prediction = weight * x
        total_loss += (prediction - y) ** 2

    mse = total_loss / len(data)

    return weight, mse


def main() -> None:
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment("Week7_Linear_Regression")

    data = load_training_data()

    learning_rates = [0.001, 0.01, 0.02]
    epochs = 100

    print(f"Loaded {len(data)} training rows from {DATA_PATH}")

    for learning_rate in learning_rates:
        with mlflow.start_run(run_name=f"learning_rate_{learning_rate}"):
            weight, mse = train_model(data, learning_rate, epochs)

            mlflow.log_param("learning_rate", learning_rate)
            mlflow.log_param("epochs", epochs)
            mlflow.log_param("algorithm", "linear_regression")
            mlflow.log_param("dataset_rows", len(data))
            mlflow.log_param("dataset_path", str(DATA_PATH))

            mlflow.log_metric("mse", mse)
            mlflow.log_metric("final_weight", weight)

            report = Path("model_summary.txt")
            report.write_text(
                f"Dataset: {DATA_PATH}\n"
                f"Dataset rows: {len(data)}\n"
                f"Learning rate: {learning_rate}\n"
                f"Epochs: {epochs}\n"
                f"Learned weight: {weight}\n"
                f"MSE: {mse}\n"
            )

            mlflow.log_artifact(str(report))

            print(f"LR: {learning_rate}, " f"Weight: {weight:.6f}, MSE: {mse:.8f}")


if __name__ == "__main__":
    main()
