import mlflow
from mlflow import MlflowClient

TRACKING_URI = "sqlite:///mlflow.db"
MODEL_NAME = "Week7LinearRegression"
MODEL_VERSION = 4
ALIAS = "production"


def main() -> None:
    mlflow.set_tracking_uri(TRACKING_URI)
    client = MlflowClient(tracking_uri=TRACKING_URI)

    # Retrieve the exact model version that passed M4
    version = client.get_model_version(
        name=MODEL_NAME,
        version=MODEL_VERSION,
    )

    if version.status != "READY":
        raise RuntimeError(f"Model version is not READY: {version.status}")

    # Promote the verified version
    client.set_registered_model_alias(
        name=MODEL_NAME,
        alias=ALIAS,
        version=MODEL_VERSION,
    )

    # Verify that the alias points to the intended version
    production_model = client.get_model_version_by_alias(
        name=MODEL_NAME,
        alias=ALIAS,
    )

    if production_model.version != MODEL_VERSION:
        raise RuntimeError("Production alias verification failed")

    print("MODEL PROMOTION SUCCESSFUL")
    print(f"Model: {MODEL_NAME}")
    print(f"Production alias: @{ALIAS}")
    print(f"Production version: {production_model.version}")


if __name__ == "__main__":
    main()
