import pytest

from mlflow_lab import train, validate_data
from mlflow_lab.train import load_training_data, train_model

# -----------------------------
# CSV loading tests
# -----------------------------


def test_load_training_data_valid_csv(tmp_path, monkeypatch):
    csv_file = tmp_path / "training.csv"
    csv_file.write_text("x,y\n1,2\n2,4\n3,6\n")

    monkeypatch.setattr(train, "DATA_PATH", csv_file)

    data = load_training_data()

    assert data == [(1.0, 2.0), (2.0, 4.0), (3.0, 6.0)]


def test_load_training_data_empty_csv(tmp_path, monkeypatch):
    csv_file = tmp_path / "training.csv"
    csv_file.write_text("x,y\n")

    monkeypatch.setattr(train, "DATA_PATH", csv_file)

    with pytest.raises(ValueError, match="Training dataset is empty"):
        load_training_data()


# -----------------------------
# Data validation tests
# -----------------------------


def test_validate_data_success(tmp_path, monkeypatch):
    csv_file = tmp_path / "training.csv"
    csv_file.write_text("x,y\n1,2\n2,4\n")

    monkeypatch.setattr(validate_data, "DATA_PATH", csv_file)

    validate_data.validate_data()


def test_validate_data_missing_file(tmp_path, monkeypatch):
    csv_file = tmp_path / "missing.csv"
    monkeypatch.setattr(validate_data, "DATA_PATH", csv_file)

    with pytest.raises(FileNotFoundError):
        validate_data.validate_data()


def test_validate_data_missing_column(tmp_path, monkeypatch):
    csv_file = tmp_path / "training.csv"
    csv_file.write_text("x,z\n1,2\n")

    monkeypatch.setattr(validate_data, "DATA_PATH", csv_file)

    with pytest.raises(ValueError, match="must contain x and y"):
        validate_data.validate_data()


def test_validate_data_empty_dataset(tmp_path, monkeypatch):
    csv_file = tmp_path / "training.csv"
    csv_file.write_text("x,y\n")

    monkeypatch.setattr(validate_data, "DATA_PATH", csv_file)

    with pytest.raises(ValueError, match="cannot be empty"):
        validate_data.validate_data()


def test_validate_data_missing_value(tmp_path, monkeypatch):
    csv_file = tmp_path / "training.csv"
    csv_file.write_text("x,y\n1,\n")

    monkeypatch.setattr(validate_data, "DATA_PATH", csv_file)

    with pytest.raises(ValueError, match="Missing value"):
        validate_data.validate_data()


def test_validate_data_non_numeric_value(tmp_path, monkeypatch):
    csv_file = tmp_path / "training.csv"
    csv_file.write_text("x,y\n1,INVALID\n")

    monkeypatch.setattr(validate_data, "DATA_PATH", csv_file)

    with pytest.raises(ValueError, match="Non-numeric value"):
        validate_data.validate_data()


# -----------------------------
# Model training tests
# -----------------------------


def test_train_model_learns_expected_weight():
    data = [
        (1.0, 2.0),
        (2.0, 4.0),
        (3.0, 6.0),
        (4.0, 8.0),
        (5.0, 10.0),
    ]

    weight, mse = train_model(
        data=data,
        learning_rate=0.01,
        epochs=100,
    )

    assert weight == pytest.approx(2.0, abs=0.001)
    assert mse < 0.001


def test_train_model_rejects_empty_data():
    with pytest.raises(ValueError, match="Training data cannot be empty"):
        train_model(
            data=[],
            learning_rate=0.01,
            epochs=100,
        )
