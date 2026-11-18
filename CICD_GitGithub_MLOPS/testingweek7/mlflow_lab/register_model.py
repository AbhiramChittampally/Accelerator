from pathlib import Path

import mlflow
import pandas as pd
from mlflow import MlflowClient

TRACKING_URI = "sqlite:///mlflow.db"
MODEL_NAME = "Week7LinearRegression"
EXPERIMENT_NAME = "Week7_Linear_Regression"
BEST_RUN_FILE = Path("mlflow_lab/best_run_id.txt")


class LinearRegressionModel(mlflow.pyfunc.PythonModel):
    def __init__(self, weight: float):
        self.weight = weight

    def predict(self, context, model_input, params=None):
        return model_input["x"] * self.weight


def main() -> None:
    mlflow.set_tracking_uri(TRACKING_URI)
    client = MlflowClient(tracking_uri=TRACKING_URI)

    if not BEST_RUN_FILE.exists():
        raise FileNotFoundError(f"Winner run ID file not found: {BEST_RUN_FILE}")

    best_run_id = BEST_RUN_FILE.read_text(encoding="utf-8").strip()

    if not best_run_id:
        raise ValueError("Winner run ID file is empty")

    # Retrieve the actual winning sweep run
    source_run = client.get_run(best_run_id)

    if source_run.info.status != "FINISHED":
        raise ValueError("Winning MLflow run has not finished successfully")

    weight = source_run.data.metrics["final_weight"]
    learning_rate = source_run.data.params["learning_rate"]
    epochs = source_run.data.params["epochs"]

    print(f"Source run: {best_run_id}")
    print(f"Winning learning rate: {learning_rate}")
    print(f"Learned weight: {weight}")

    # Register the model using the winning run's learned weight
    experiment = client.get_experiment_by_name(EXPERIMENT_NAME)

    if experiment is None:
        raise ValueError(f"Experiment not found: {EXPERIMENT_NAME}")

    with mlflow.start_run(
        experiment_id=experiment.experiment_id,
        run_name="register_winning_model",
    ):
        mlflow.log_param("source_run_id", best_run_id)
        mlflow.log_param("source_learning_rate", learning_rate)
        mlflow.log_param("source_epochs", epochs)
        mlflow.log_metric("source_mse", source_run.data.metrics["mse"])

        mlflow.set_tag("milestone", "M3")
        mlflow.set_tag("model_source", "winning_sweep_run")

        model_info = mlflow.pyfunc.log_model(
            name="model",
            python_model=LinearRegressionModel(weight),
            input_example=pd.DataFrame({"x": [1.0, 2.0, 3.0]}),
            registered_model_name=MODEL_NAME,
        )

        print(f"Model URI: {model_info.model_uri}")

    versions = client.search_model_versions(f"name='{MODEL_NAME}'")

    registered_version = next(
        (version for version in versions if version.run_id == model_info.run_id),
        None,
    )

    if registered_version is None:
        raise RuntimeError("Registered model version was not found")

    print("\nMODEL REGISTRATION SUCCESSFUL")
    print(f"Model name: {MODEL_NAME}")
    print(f"Model version: {registered_version.version}")
    print(f"Source sweep run: {best_run_id}")
    print(f"Registered weight: {weight}")


if __name__ == "__main__":
    main()
