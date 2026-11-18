import mlflow

from mlflow_lab.train import DATA_PATH, load_training_data, train_model


def main() -> None:
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    experiment = mlflow.set_experiment("Week7_Linear_Regression")

    data = load_training_data()

    learning_rates = [0.001, 0.005, 0.01, 0.015, 0.02]
    epochs = 100

    results: list[dict[str, float | str]] = []

    print(f"Dataset rows: {len(data)}")
    print(f"Running {len(learning_rates)} experiments...\n")

    for learning_rate in learning_rates:
        weight, mse = train_model(
            data=data,
            learning_rate=learning_rate,
            epochs=epochs,
        )

        with mlflow.start_run(
            experiment_id=experiment.experiment_id,
            run_name=f"sweep_lr_{learning_rate}",
        ):
            mlflow.log_param("algorithm", "linear_regression")
            mlflow.log_param("learning_rate", learning_rate)
            mlflow.log_param("epochs", epochs)
            mlflow.log_param("dataset_rows", len(data))
            mlflow.log_param("dataset_path", str(DATA_PATH))

            mlflow.log_metric("mse", mse)
            mlflow.log_metric("final_weight", weight)

            mlflow.set_tag("milestone", "M2")
            mlflow.set_tag("experiment_type", "learning_rate_sweep")

            run_id = mlflow.active_run().info.run_id

        results.append(
            {
                "run_id": run_id,
                "learning_rate": learning_rate,
                "weight": weight,
                "mse": mse,
            }
        )

        print(
            f"LR: {learning_rate:.3f} | "
            f"Weight: {weight:.6f} | "
            f"MSE: {mse:.10f} | "
            f"Run ID: {run_id}"
        )

    best_run = min(results, key=lambda result: float(result["mse"]))

    print("\n========== BEST MODEL ==========")
    print(f"Learning rate: {best_run['learning_rate']}")
    print(f"Weight:        {best_run['weight']:.6f}")
    print(f"MSE:           {best_run['mse']:.10f}")
    print(f"Run ID:        {best_run['run_id']}")

    with open("mlflow_lab/best_run_id.txt", "w", encoding="utf-8") as file:
        file.write(str(best_run["run_id"]))

    print("\nBest run ID saved to mlflow_lab/best_run_id.txt")


if __name__ == "__main__":
    main()
