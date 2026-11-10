# Day 34: Quality Gates, Continuous Delivery (CD), and MLOps Foundations

---

## Syllabus Alignment & Overview

| Topic Code | Module Title | Duration | Core Focus & Real-World Objective |
| :--- | :--- | :--- | :--- |
| **6.9** | **Quality-Gate Workflow** | 45m | The Three-Layer Quality Defense; `ruff`, `black`, `mypy`, `bandit`; `.pre-commit-config.yaml`; zero config drift in CI. |
| **6.10** | **CD Basics** | 45m | Build-once-deploy-many; environment promotion ladder (`dev` $\rightarrow$ `staging` $\rightarrow$ `canary` $\rightarrow$ `prod`); 5 deployment strategies; SLO-driven rollback. |
| **M1** | **What is MLOps? (Basics)** | 30m | Notebooks vs Production ML; 3 unique ML failure modes (silent failures, drift, reproducibility rot); Google MLOps Maturity Levels 0-2. |
| **6.11a** | **MLflow: Experiment Tracking** | 45m | The tracking trichotomy (params, metrics, artifacts); tags for reproducibility; MLflow UI comparison; programmatic queries via `search_runs`. |
| **6.11b** | **MLflow: Model Registry** | 30m | Registered models, immutable versions, mutable aliases (`@candidate`, `@staging`, `@production`); load-by-alias serving. |

---

## 1. Topic 6.9: The Three-Layer Quality Defense & Pre-Commit

Quality checks should be shifted as far **left** (earliest in developer lifecycle) as possible to catch issues before code reaches peer review or production.

```
+---------------------------------------------------------------------------------------------------------+
|                                  THE THREE-LAYER QUALITY DEFENSE                                        |
+---------------------------------------------------------------------------------------------------------+
| 1. LAYER 1: Editor / IDE (On Save)        | Ruff & Black extensions auto-format and underline syntax.   |
| 2. LAYER 2: Local Pre-Commit Hook (On Commit) | Git hook halts `git commit` if linting, types, or tests fail.|
| 3. LAYER 3: Remote CI Pipeline (On Push / PR)| GitHub Actions independently runs checks before merge.  |
+---------------------------------------------------------------------------------------------------------+
```

### 1.1 The Modern Python Toolchain
- **`ruff`**: An extremely fast Python linter written in Rust. Replaces `flake8`, `isort`, `pydocstyle`, and `pyupgrade` while running $10\times - 100\times$ faster.
- **`black`**: The deterministic, uncompromising Python code formatter that enforces PEP 8 compliance without arguments.
- **`mypy`**: Static type analysis that verifies type hints (`list[str]`, `dict[str, Any]`, `Optional[int]`), preventing runtime `TypeError` and `AttributeError`.
- **`bandit`**: Static security scanner that detects hardcoded passwords, insecure SQL queries, and unsafe deserialization (`pickle.load`).

---

### 1.2 Production Boilerplate `.pre-commit-config.yaml`

```yaml
# .pre-commit-config.yaml
# Configures automated git hooks that execute prior to git commit
default_language_version:
  python: python3.12

repos:
  # General file hygiene
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace       # Removes useless trailing spaces
      - id: end-of-file-fixer         # Ensures files end with a clean newline
      - id: check-yaml                # Verifies syntax of YAML configuration files
      - id: check-added-large-files   # Blocks accidental commits of files > 500KB
        args: ['--maxkb=500']
      - id: detect-private-key        # Scans for accidental private key commits

  # Ruff: Ultra-fast linting & import sorting
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.4
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]

  # Black: Deterministic code formatting
  - repo: https://github.com/psf/black
    rev: 24.4.2
    hooks:
      - id: black

  # Mypy: Static type checking
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.10.0
    hooks:
      - id: mypy
        additional_dependencies: [types-requests, types-PyYAML]
        args: [--ignore-missing-imports, --check-untyped-defs]
```

#### Hands-On Pre-Commit Execution:
```bash
# 1. Install pre-commit framework
pip install pre-commit

# 2. Install the git hook scripts into your local .git/hooks directory
pre-commit install
# Output: pre-commit installed at .git/hooks/pre-commit

# 3. Manually run all hooks across the entire codebase
pre-commit run --all-files
```

#### Zero Config Drift Principle:
To ensure developers and CI run identical checks with identical tool versions, CI calls `pre-commit/action@v3` directly. If a developer uses `--no-verify` to bypass local hooks, the CI pipeline catches and blocks it immediately.

---

## 2. Topic 6.10: CD Basics & Production Deployment Strategies

### 2.1 The Cardinal Rule of Continuous Delivery: Build-Once-Deploy-Many
> **Never recompile code or rebuild a Docker image between environments.**
> Build a single immutable container image tagged with the commit SHA (`ghcr.io/org/app:sha-a1b2c3d`). Test that exact image in `dev`, promote that exact image to `staging`, and promote that exact image to `production`. Only environment variables and secrets change between stages.

```
[ Git SHA: a1b2c3d ]
        |
        v
[ Docker Build ] ---> Image: ghcr.io/org/askmynotes:sha-a1b2c3d
                            |
           +----------------+----------------+
           |                                 |
           v                                 v
   [ Dev / Staging ]                 [ Production ]
   (Config: DEV_ENV)                 (Config: PROD_ENV)
```

---

### 2.2 Comparison of the 5 Major Deployment Strategies

| Deployment Strategy | How It Operates | Downtime? | Rollback Speed | Compute Cost | Best Use Case |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Recreate** | Terminate version A completely; boot version B. | **YES** | Slow (minutes) | Lowest ($1\times$) | Dev environments; batch processing systems. |
| **Rolling Update** | Incrementally replace pods running version A with version B (e.g., 25% at a time). | **NO** | Moderate | Medium ($1.25\times$) | Standard microservices, routine infrastructure upgrades. |
| **Blue/Green** | Deploy version B (Green) alongside version A (Blue) on full capacity. Switch router/DNS instantly to Green. | **NO** | **Instant (seconds)** | High ($2\times$) | High-stakes consumer web apps; database migrations requiring instant switch. |
| **Canary** | Route 5% of user traffic to version B; monitor error rates and latency SLOs. Gradually increase to 25%, 50%, 100%. | **NO** | Fast (seconds) | Moderate | Risky algorithmic changes, recommendation engines, ML serving. |
| **Feature Flags** | Deploy code dark (hidden behind boolean flags). Toggle feature live via API without redeploying. | **NO** | Instant (sub-second) | Lowest | Rapid experimentation, trunk-based continuous deployment. |

---

### 2.3 Production Delivery Pipeline (`.github/workflows/deploy.yml`)

```yaml
name: Continuous Delivery

on:
  push:
    branches: [main]  # Triggers only after code is merged into main

jobs:
  # Step 1: Build & Publish Single Immutable Container Image
  build-and-push:
    name: Build & Push Container Image
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Log in to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and Push Docker Image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            ghcr.io/${{ github.repository }}:sha-${{ github.sha }}
            ghcr.io/${{ github.repository }}:latest

  # Step 2: Deploy to Staging (Automated)
  deploy-staging:
    name: Deploy to Staging Environment
    needs: [build-and-push]
    runs-on: ubuntu-latest
    environment:
      name: staging
      url: https://staging.askmynotes.internal
    steps:
      - name: Rollout Staging Service
        run: |
          echo "Deploying image ghcr.io/${{ github.repository }}:sha-${{ github.sha }} to staging"

  # Step 3: Deploy to Production (Manual Approval Gate Required)
  deploy-prod:
    name: Deploy to Production (Gated)
    needs: [deploy-staging]
    runs-on: ubuntu-latest
    environment:
      name: production  # Configured in GitHub Settings with required human reviewer
      url: https://askmynotes.com
    steps:
      - name: Rollout Production Service (Canary 5%)
        run: |
          echo "Promoting ghcr.io/${{ github.repository }}:sha-${{ github.sha }} to production canary"
```

---

## 3. Topic M1: What is MLOps? (From Notebook to Production)

### 3.1 Why MLOps is Fundamentally Harder Than Traditional DevOps

Traditional software engineering manages **one asset**: Code.
Machine Learning systems manage **four interconnected assets**:
$$\text{Production ML System} = \text{Code} + \text{Data} + \text{Model Weights} + \text{Hyperparameters}$$

```
+---------------------------------------------------------------------------------------------------------+
|                                    THE THREE UNIQUE ML FAILURE MODES                                    |
+---------------------------------------------------------------------------------------------------------+
| 1. Reproducibility Rot | A model trained 3 months ago cannot be reproduced because dataset or numpy    |
|                        | version changed silently without tracking.                                      |
| 2. Data & Concept Drift| User inputs change over time (e.g. holiday shopping patterns, new legal terms), |
|                        | degrading prediction quality while serving code runs without errors.           |
| 3. Silent Failure      | The service returns HTTP 200 OK with formatted JSON, but the model outputs     |
|                        | completely nonsensical hallucinated rankings. No exception is ever thrown.      |
+---------------------------------------------------------------------------------------------------------+
```

### 3.2 The Google MLOps Maturity Model

```
Level 0: Manual Process (The "Data Science Wilderness")
- Manual execution of Jupyter notebooks.
- Data scientists email `.pkl` files or save weights to Dropbox.
- Serving code hardcodes model paths.
- Zero tracking of data lineage or training code SHA.

Level 1: Automated ML Pipeline (Continuous Training)
- Model training is an automated DAG (extract -> preprocess -> train -> evaluate).
- Experiment tracking (MLflow) records all runs, params, and metrics.
- Validated models automatically registered in a Model Registry.
- Pipelines trigger on new data arrivals or schedules.

Level 2: Full CI/CD Pipeline Automation (The Gold Standard)
- Code CI automatically tests and builds pipeline components.
- CD pipeline deploys automated training pipelines and serving microservices.
- Feedback loop closed: Production drift monitors automatically trigger retraining,
  contract tests validate new models, and alias flips roll out new versions.
```

---

## 4. Topic 6.11a: MLflow Experiment Tracking

MLflow Tracking organizes machine learning experimentation into **Experiments** (logical groups) and **Runs** (individual training executions).

### 4.1 The Experiment Tracking Trichotomy

```
                                      +--------------------------+
                                      |        MLFLOW RUN        |
                                      +--------------------------+
                                                    |
             +--------------------------------------+--------------------------------------+
             |                                      |                                      |
             v                                      v                                      v
   1. PARAMETERS (Inputs)                 2. METRICS (Outputs)                  3. ARTIFACTS (Files)
   - embedding_model: bge-base-en        - map_at_5: 0.782                     - index.bin (FAISS)
   - chunk_size: 500                      - recall_at_10: 0.854                 - loss_curve.png
   - chunk_overlap: 50                    - p95_latency_ms: 182                 - requirements.txt
```

### 4.2 Production Experiment Tracking Script (`experiments/track_run.py`)

```python
# experiments/track_run.py
"""Executes and logs a reproducible AskMyNotes retriever training run to MLflow."""

import argparse
import datetime
import os
from pathlib import Path
import subprocess
import time
import mlflow
from askmynotes.eval import evaluate_retriever


def get_git_commit_sha() -> str:
  """Retrieve the active Git commit hash for provenance tracking."""
  try:
    return (
        subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
    )
  except Exception:
    return "untracked"


def train_and_track(
    embedding_model: str, chunk_size: int, chunk_overlap: int
) -> str:
  """Run retriever evaluation, log all telemetry to MLflow, and return the run_id."""
  # Line 1: Configure active MLflow experiment
  mlflow.set_experiment("askmynotes-retrieval")

  # Line 2: Generate human-readable run name
  run_name = (
      f"{embedding_model.split('/')[-1]}-cs{chunk_size}-ov{chunk_overlap}"
  )

  # Line 3: Start tracked MLflow execution
  with mlflow.start_run(run_name=run_name) as run:
    run_id = run.info.run_id
    print(f"Starting MLflow Run [{run_id}] - {run_name}")

    # Line 4: Log Hyperparameters (Inputs)
    mlflow.log_params({
        "embedding_model": embedding_model,
        "chunk_size": chunk_size,
        "chunk_overlap": chunk_overlap,
        "distance_metric": "cosine",
    })

    # Line 5: Log Provenance & Lineage Tags
    mlflow.set_tags({
        "git.sha": get_git_commit_sha(),
        "runner.user": os.getenv("USER", "engineer"),
        "pipeline.type": "offline_experiment",
        "timestamp": datetime.datetime.utcnow().isoformat(),
    })

    # Line 6: Execute simulated training & evaluation benchmark
    t0 = time.perf_counter()
    eval_metrics = evaluate_retriever(
        model_name=embedding_model,
        chunk_size=chunk_size,
        overlap=chunk_overlap,
    )
    duration_sec = time.perf_counter() - t0

    # Line 7: Log Performance Metrics (Outputs)
    mlflow.log_metrics({
        "map_at_5": eval_metrics["map_at_5"],
        "recall_at_10": eval_metrics["recall_at_10"],
        "p95_latency_ms": eval_metrics["p95_latency_ms"],
        "training_duration_seconds": duration_sec,
    })

    # Line 8: Log Artifacts (Evaluation charts, text files)
    artifacts_dir = Path("metrics_output")
    artifacts_dir.mkdir(exist_ok=True)
    with open(artifacts_dir / "summary.txt", "w") as f:
      f.write(f"Run {run_id} completed with MAP@5={eval_metrics['map_at_5']}")

    mlflow.log_artifacts(str(artifacts_dir))
    print(f"Logged run: {run_id} | MAP@5 = {eval_metrics['map_at_5']:.4f}")

    return run_id


if __name__ == "__main__":
  parser = argparse.ArgumentParser(
      description="Track AskMyNotes Retriever Experiment"
  )
  parser.add_argument(
      "--model", default="BAAI/bge-base-en-v1.5", help="Embedding model name"
  )
  parser.add_argument(
      "--chunk-size", type=int, default=500, help="Chunk character length"
  )
  parser.add_argument(
      "--chunk-overlap", type=int, default=50, help="Overlap length"
  )
  args = parser.parse_args()

  train_and_track(args.model, args.chunk_size, args.chunk_overlap)
```

---

### 4.3 Programmatic Querying & Winner Selection
Instead of clicking around the web UI, automated CI/CD workflows query runs using the MLflow Python Client:

```python
# experiments/find_best_run.py
import mlflow

# Connect to tracking server
mlflow.set_tracking_uri("http://localhost:5000")

# Programmatically query the best run based on MAP@5 metric
runs_df = mlflow.search_runs(
    experiment_names=["askmynotes-retrieval"],
    filter_string="metrics.p95_latency_ms < 200",  # Latency constraint
    order_by=["metrics.map_at_5 DESC"],  # Sort by highest quality
    max_results=5,
)

best_run = runs_df.iloc[0]
print(f"Top Model Run ID: {best_run['run_id']}")
print(f"Best MAP@5: {best_run['metrics.map_at_5']:.4f}")
print(f"Chunk Size: {best_run['params.chunk_size']}")
```

---

## 5. Topic 6.11b: MLflow Model Registry & Load-by-Alias Serving

### 5.1 The Modern Alias-Based Registry Architecture
In older versions of MLflow, models were categorized into hardcoded stages (`Staging`, `Production`, `Archived`).
In modern MLflow (2.8+), stages are deprecated in favor of **Mutable Aliases**:

- **Model Name**: The registered entity name (e.g., `AskMyNotesRetriever`).
- **Model Version**: An **immutable** integer version number (`v1`, `v2`, `v3`). Code, weights, and run links never change once registered.
- **Model Alias**: A **mutable pointer** (`@candidate`, `@staging`, `@production`) pointing to a specific version number.

```
Registered Model: AskMyNotesRetriever
├── Version 1 (Immutable) <------ @production
├── Version 2 (Immutable)
└── Version 3 (Immutable) <------ @staging, @candidate
```

---

### 5.2 Promotion Automation Script (`experiments/promote_best_model.py`)

```python
# experiments/promote_best_model.py
import argparse
import datetime
from mlflow import MlflowClient

MODEL_NAME = "AskMyNotesRetriever"


def promote_run_to_alias(run_id: str, alias: str):
  """Register model artifact from run_id and assign the specified alias."""
  client = MlflowClient()

  # Line 1: Register model from MLflow run artifacts into the registry
  model_uri = f"runs:/{run_id}/model"
  mv = client.create_model_version(
      name=MODEL_NAME,
      source=model_uri,
      run_id=run_id,
      description=f"Model registered from run {run_id}",
  )
  print(f"Created {MODEL_NAME} version {mv.version}")

  # Line 2: Assign alias (e.g. 'candidate', 'staging', 'production')
  client.set_registered_model_alias(
      name=MODEL_NAME, alias=alias, version=mv.version
  )
  print(f"Assigned alias @{alias} -> Version {mv.version}")

  # Line 3: Add governance metadata tag
  client.set_model_version_tag(
      name=MODEL_NAME,
      version=mv.version,
      key="promoted_at",
      value=datetime.datetime.utcnow().isoformat(),
  )


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument(
      "--run-id", required=True, help="MLflow Run ID of winning model"
  )
  parser.add_argument(
      "--target-alias",
      default="candidate",
      choices=["candidate", "staging", "production"],
  )
  args = parser.parse_args()

  promote_run_to_alias(args.run_id, args.target_alias)
```

---

### 5.3 Serving by Alias: The Zero-Code-Change Model Swap

#### The Anti-Pattern: Hardcoded Version Numbers
```python
# DANGEROUS: Every model update requires code editing, git commit, PR review, and redeploy!
model = mlflow.pyfunc.load_model("models:/AskMyNotesRetriever/1")
```

#### The Production Standard: Dynamic Alias Resolution
```python
# askmynotes/serving.py
from functools import lru_cache
import os
from fastapi import FastAPI
import mlflow.pyfunc
from pydantic import BaseModel

app = FastAPI(title="AskMyNotes Model Serving Service")

MODEL_NAME = os.getenv("MODEL_NAME", "AskMyNotesRetriever")
MODEL_ALIAS = os.getenv("MODEL_ALIAS", "production")


class QueryRequest(BaseModel):
  query: str
  candidates: list[str]


@lru_cache(maxsize=1)
def get_model():
  """Load model once into memory at process boot using the alias."""
  model_uri = f"models:/{MODEL_NAME}@{MODEL_ALIAS}"
  print(f"Loading model dynamically from {model_uri}...")
  return mlflow.pyfunc.load_model(model_uri)


@app.get("/health")
def health():
  return {"status": "healthy", "model_alias": MODEL_ALIAS}


@app.post("/rerank")
def rerank(req: QueryRequest):
  model = get_model()
  scores = model.predict({"query": req.query, "candidates": req.candidates})
  return {"scores": scores, "model_alias": MODEL_ALIAS}
```

> [!TIP]
> **The 10-Second Production Rollback**:
> If version 2 misbehaves in production, **no code is touched**. An engineer flips `@production` back to version 1:
> ```bash
> python -c "from mlflow import MlflowClient; MlflowClient().set_registered_model_alias('AskMyNotesRetriever', 'production', 1)"
> ```
> A rolling restart of the Kubernetes pod or container forces the serving process to reload `@production` (now version 1). Total recovery time: under 60 seconds.
