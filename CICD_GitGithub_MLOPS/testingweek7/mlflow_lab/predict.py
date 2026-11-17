import mlflow
import pandas as pd

mlflow.set_tracking_uri("sqlite:///mlflow.db")

model_uri = "models:/Week7LinearRegression@champion"

model = mlflow.pyfunc.load_model(model_uri)

input_data = pd.DataFrame({"x": [6, 7, 8, 9, 10]})

predictions = model.predict(input_data)

for x, prediction in zip(input_data["x"], predictions):
    print(f"Input: {x}, Prediction: {prediction}")
