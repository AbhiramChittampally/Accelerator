import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PIPELINE_DIR = PROJECT_ROOT / "mlflow_lab"


def run_stage(stage_name: str, script_name: str) -> None:
    script_path = PIPELINE_DIR / script_name

    print(f"\n{'=' * 50}", flush=True)
    print(f"STARTING: {stage_name}", flush=True)
    print(f"{'=' * 50}", flush=True)

    subprocess.run(
        [sys.executable, str(script_path)],
        cwd=PROJECT_ROOT,
        check=True,
    )

    print(f"COMPLETED: {stage_name}", flush=True)


def main() -> None:
    print("ML PIPELINE STARTED", flush=True)

    try:
        run_stage("Data Validation", "validate_data.py")
        run_stage("Model Training", "train.py")

    except subprocess.CalledProcessError as error:
        print(
            f"\nPIPELINE FAILED with exit code {error.returncode}",
            flush=True,
        )
        sys.exit(error.returncode)

    print("\nML PIPELINE COMPLETED SUCCESSFULLY", flush=True)


if __name__ == "__main__":
    main()
