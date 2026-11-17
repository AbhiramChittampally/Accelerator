import mlflow
import pandas as pd
from mlflow import MlflowClient

# Connect to our local MLflow database
mlflow.set_tracking_uri("sqlite:///mlflow.db")

EXPERIMENT_NAME = "Week7_Linear_Regression"
MODEL_NAME = "Week7LinearRegression"

# Select the best model configuration from our experiment
learning_rate = 0.01
epochs = 100

data = [
    (1, 2),
    (2, 4),
    (3, 6),
    (4, 8),
    (5, 10),
]

# Train the selected model
weight = 0.0

for epoch in range(epochs):
    gradient = 0.0

    for x, y in data:
        prediction = weight * x
        gradient += 2 * x * (prediction - y)

    gradient /= len(data)
    weight -= learning_rate * gradient


class LinearRegressionModel(mlflow.pyfunc.PythonModel):

    def __init__(self, weight):
        self.weight = weight

    def predict(self, context, model_input, params=None):
        return model_input["x"] * self.weight


# Register the trained model
with mlflow.start_run(
    experiment_id=mlflow.get_experiment_by_name(EXPERIMENT_NAME).experiment_id,
    run_name="champion_model_training",
):

    mlflow.log_param("learning_rate", learning_rate)
    mlflow.log_param("epochs", epochs)
    mlflow.log_metric("final_weight", weight)

    mlflow.pyfunc.log_model(
        name="model",
        python_model=LinearRegressionModel(weight),
        input_example=pd.DataFrame({"x": [1, 2, 3]}),
        registered_model_name=MODEL_NAME,
    )

    print(f"Model registered: {MODEL_NAME}")
    print(f"Learned weight: {weight}")


# Assign the champion alias to the latest registered version
client = MlflowClient()

versions = client.search_model_versions(f"name='{MODEL_NAME}'")

latest_version = max(versions, key=lambda version: int(version.version))

client.set_registered_model_alias(
    MODEL_NAME,
    "champion",
    latest_version.version,
)

print(f"Champion alias assigned to version {latest_version.version}")
