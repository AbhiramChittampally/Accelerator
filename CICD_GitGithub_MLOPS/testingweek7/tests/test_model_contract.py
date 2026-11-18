from pathlib import Path

import mlflow
import pandas as pd
import pytest


@pytest.fixture(scope="module")
def registered_model():
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    if not Path("mlflow.db").exists():
        pytest.skip("Local MLflow registry is not available")
    return mlflow.pyfunc.load_model("models:/Week7LinearRegression/4")


def test_model_accepts_dataframe(registered_model):
    data = pd.DataFrame({"x": [1.0, 2.0, 3.0]})
    predictions = registered_model.predict(data)

    assert len(predictions) == 3


def test_model_predictions_are_correct(registered_model):
    data = pd.DataFrame({"x": [1.0, 2.0, 3.0]})
    predictions = registered_model.predict(data)

    assert list(predictions) == pytest.approx([2.0, 4.0, 6.0])


def test_model_handles_single_input(registered_model):
    data = pd.DataFrame({"x": [5.0]})
    predictions = registered_model.predict(data)

    assert len(predictions) == 1
    assert float(predictions[0]) == pytest.approx(10.0)
