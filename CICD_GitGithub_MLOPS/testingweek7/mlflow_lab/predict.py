import mlflow
import pandas as pd

TRACKING_URI = "sqlite:///mlflow.db"
MODEL_URI = "models:/Week7LinearRegression@production"


def main():
    mlflow.set_tracking_uri(TRACKING_URI)

    print("Loading production model...")
    model = mlflow.pyfunc.load_model(MODEL_URI)

    input_data = pd.DataFrame({"x": [6.0, 7.0, 8.0, 9.0, 10.0]})

    predictions = model.predict(input_data)

    print("\nPRODUCTION MODEL PREDICTIONS")

    for x, prediction in zip(input_data["x"], predictions):
        print(f"Input: {x}, Prediction: {prediction}")


if __name__ == "__main__":
    main()
