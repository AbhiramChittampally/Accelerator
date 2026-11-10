# Day 35: CI/CD for ML, Pipeline Automation, and the Hands-on MLOps Lab

---

## Syllabus Alignment & Overview

| Topic Code | Module Title | Duration | Core Focus & Real-World Objective |
| :--- | :--- | :--- | :--- |
| **6.12a** | **CI/CD for ML** | 45m | Testing models; retraining triggers; DVC Git-adjacent data versioning; full lineage chain (Git + DVC + MLflow); Model Contracts. |
| **6.12b** | **ML Pipeline Automation** | 30m | DAG orchestration landscape (Actions vs Prefect vs Airflow vs Kubeflow); automated training workflow (`train.yml`). |
| **Lab** | **Full Pipeline Lab** | 45m | The finished `AskMyNotes` repo architecture; 12-command fresh-clone bring-up; 3 integration verification tests; multi-stage Dockerfile. |
| **MLLab** | **MLflow + CI Lab** | 30m | Six-milestone hands-on walkthrough (M1-M6); parameter sweeps; contract gating; zero-code model swap and 10-second rollback. |
| **Rev** | **Consolidation & Q&A** | 30m | Synthesize Git $\rightarrow$ CI/CD $\rightarrow$ MLOps; 30 canonical interview questions; common trap questions; rehearsed 90-second elevator pitch. |

---

## 1. Topic 6.12a: CI/CD for ML & Data Versioning (DVC)

### 1.1 The Full Provenance Lineage Chain
To achieve true auditability and reproducibility in production ML, every single user prediction must be traceable back to its origin:

```
[ User Prediction at FastAPI Serving ]
                   |
                   v
[ Model Alias: @production resolves to Version 8 ]
                   |
                   v
[ MLflow Registry Version 8 links to Run ID: xyz789 ]
                   |
                   v
[ Run xyz789 Telemetry Tags & Parameters ]
   ├── Git SHA: a1b2c3d4e5       ---> Exact source code commit
   ├── DVC Data Hash: sha256:def ---> Exact training corpus blobs in S3
   ├── Hyperparameters           ---> chunk_size=500, model=bge-base-en
   └── Evaluation Metrics        ---> MAP@5=0.782, p95=182ms
```

---

### 1.2 DVC: Git-Adjacent Data Versioning Mechanics

```bash
# 1. Initialize DVC in the repository
pip install "dvc[s3]"
dvc init
git commit -m "chore: initialize DVC"

# 2. Add remote storage (S3 / GCS / Azure Blob)
dvc remote add -d storage s3://my-company-mlops/askmynotes-data
git add .dvc/config && git commit -m "chore: configure S3 DVC remote"

# 3. Track large data files (creates tiny .dvc pointer file, adds actual data to .gitignore)
dvc add data/raw_pdfs
dvc add data/golden_qa_v1.jsonl

# 4. Commit pointer files to Git
git add data/raw_pdfs.dvc data/golden_qa_v1.jsonl.dvc .gitignore
git commit -m "data: track raw PDFs and golden evaluation dataset v1"

# 5. Push data blobs to cloud remote
dvc push

# 6. On any other machine: fetch matching data with 1 command
git clone https://github.com/org/askmynotes.git
dvc pull  # Reads .dvc pointer files and downloads matching content from S3
```

---

### 1.3 Model Contract Tests: The ML Quality Gate
Model contracts are automated tests executed against a candidate model before advancing its alias.

```python
# tests/contract/test_retriever_contract.py
"""Automated Model Contract Gates for AskMyNotesRetriever.

Run against @candidate before promoting to @staging or @production.
"""

import time
import mlflow.pyfunc
import pytest
from askmynotes.data import load_golden_qa
from askmynotes.eval import compute_map_at_k, compute_recall_at_k

MODEL_URI = "models:/AskMyNotesRetriever@candidate"
PREV_PROD_URI = "models:/AskMyNotesRetriever@production"

# Contract Quality Thresholds
MIN_MAP_AT_5 = 0.75
MIN_RECALL_AT_10 = 0.82
MAX_P95_LATENCY_MS = 200
MAX_FAIRNESS_GAP = 0.05


@pytest.fixture(scope="module")
def candidate():
  """Load candidate model artifact from MLflow registry."""
  return mlflow.pyfunc.load_model(MODEL_URI)


@pytest.fixture(scope="module")
def prev_production():
  """Load existing production model for regression comparison (skip if first release)."""
  try:
    return mlflow.pyfunc.load_model(PREV_PROD_URI)
  except mlflow.exceptions.RestException:
    pytest.skip("No previous @production version - skipping compat check")


@pytest.fixture(scope="module")
def golden():
  """Load immutable golden benchmark dataset."""
  return load_golden_qa()


# Contract Test 1: Schema Conformance
def test_schema_conformance(candidate, golden):
  sample = {
      "query": golden[0].question,
      "candidates": golden[0].candidates[:5],
  }
  result = candidate.predict(sample)
  assert isinstance(result, list)
  assert len(result) == len(sample["candidates"])
  assert all(isinstance(x, float) for x in result)
  assert all(-1.0 <= x <= 1.0 for x in result)


# Contract Test 2: Offline Quality Floor
def test_offline_quality_floor(candidate, golden):
  map5 = compute_map_at_k(candidate, golden, k=5)
  assert (
      map5 >= MIN_MAP_AT_5
  ), f"MAP@5 = {map5:.3f} failed to beat floor {MIN_MAP_AT_5}"


# Contract Test 3: Inference Latency Budget
def test_latency_budget(candidate, golden):
  # Warm-up phase
  for q in golden[:5]:
    candidate.predict({"query": q.question, "candidates": q.candidates})

  latencies = []
  for q in golden[:200]:
    t0 = time.perf_counter()
    candidate.predict({"query": q.question, "candidates": q.candidates})
    latencies.append((time.perf_counter() - t0) * 1000)

  p95 = sorted(latencies)[int(len(latencies) * 0.95)]
  assert (
      p95 < MAX_P95_LATENCY_MS
  ), f"p95 latency {p95:.1f}ms exceeds {MAX_P95_LATENCY_MS}ms budget"


# Contract Test 4: Demographic / Domain Fairness Slices
@pytest.mark.parametrize("group", ["academic", "legal", "medical"])
def test_subgroup_fairness(candidate, golden, group):
  slice_data = [q for q in golden if q.group == group]
  if len(slice_data) < 20:
    pytest.skip(f"Subgroup {group} has insufficient samples")
  map5 = compute_map_at_k(candidate, slice_data, k=5)
  assert (
      map5 >= MIN_MAP_AT_5 - MAX_FAIRNESS_GAP
  ), f"Subgroup '{group}' quality dropped below acceptable fairness gap"


# Contract Test 5: Backwards Compatibility
def test_backwards_compatibility(candidate, prev_production, golden):
  sample = {
      "query": golden[0].question,
      "candidates": golden[0].candidates[:5],
  }
  new_res = candidate.predict(sample)
  old_res = prev_production.predict(sample)
  assert type(new_res) is type(old_res)
  assert len(new_res) == len(old_res)
```

---

## 2. Topic 6.12b: ML Pipeline Automation (The Orchestrator Landscape)

### 2.1 Tool Comparison

| Orchestrator | Execution Model | Pros | Cons | Best Fit |
| :--- | :--- | :--- | :--- | :--- |
| **GitHub Actions** | Event/Schedule YAML | Zero extra infrastructure; unified with Code CI; built-in secrets. | No native DAG visualization; 2GB artifact limit; runner costs. | Small teams (<15 eng, <5 models); learning projects. |
| **Prefect** | Python-native (`@flow`, `@task`) | Pure Python; dynamic task mapping; automatic retries; rich UI. | Requires running Prefect Server / Cloud. | Mid-sized teams (15–100 eng); Python-first data teams. |
| **Apache Airflow** | Python DAG scripts | Mature ecosystem; extensive enterprise connectors; large scale. | Heavy infrastructure footprint; slow local development. | Enterprise data engineering platform teams. |
| **Kubeflow Pipelines** | Container-native Kubernetes | Full resource isolation per pod; native GPU slicing; enterprise scale. | Extreme Kubernetes complexity; high operational maintenance. | Large organizations with dedicated MLOps platform teams. |

---

### 2.2 Production Training Workflow (`.github/workflows/train.yml`)

```yaml
name: ML Training Pipeline

on:
  schedule:
    - cron: '0 2 * * *'  # Runs nightly at 02:00 UTC
  workflow_dispatch:
    inputs:
      chunk_size:
        description: 'Text chunk length'
        default: '500'
        required: true
      embedders:
        description: 'Embedding model to evaluate'
        default: 'BAAI/bge-base-en-v1.5'
        required: true
      promote_to:
        description: 'Alias to promote to on passing contracts'
        default: 'staging'
        type: choice
        options: ['candidate', 'staging']

concurrency:
  group: train-${{ github.ref }}
  cancel-in-progress: false  # Never terminate an active training job

env:
  MLFLOW_TRACKING_URI: ${{ secrets.MLFLOW_URI }}
  MLFLOW_TRACKING_TOKEN: ${{ secrets.MLFLOW_TOKEN }}
  AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
  AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}

jobs:
  # Stage 1: Data Extraction & Preprocessing
  extract-data:
    runs-on: ubuntu-latest
    timeout-minutes: 20
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12', cache: 'pip' }
      - run: pip install -e .[dvc-s3]
      - name: Pull Datasets from DVC Remote
        run: dvc pull data/raw_pdfs data/golden_qa_v1.jsonl
      - name: Extract PDF Text
        run: python pipelines/extract_pdfs.py --in data/raw_pdfs --out data/text/
      - uses: actions/upload-artifact@v4
        with:
          name: preprocessed-text
          path: data/text/
          retention-days: 7

  # Stage 2: Chunking, Embedding & Evaluation (GPU Runner)
  chunk-and-embed:
    needs: [extract-data]
    runs-on: [self-hosted, gpu]  # Dispatches to GPU runner
    timeout-minutes: 60
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12', cache: 'pip' }
      - run: pip install -e .[dev]
      - uses: actions/download-artifact@v4
        with: { name: preprocessed-text, path: data/text/ }
      - name: Chunk Text
        run: python pipelines/chunk.py --in data/text/ --out data/chunks.jsonl --size ${{ inputs.chunk_size || '500' }}
      - name: Compute Embeddings
        run: python pipelines/embed.py --in data/chunks.jsonl --model ${{ inputs.embedders || 'BAAI/bge-base-en-v1.5' }} --out data/embeddings/
      - name: Build FAISS Vector Index
        run: python pipelines/build_index.py --in data/embeddings/ --out data/index.bin
      - name: Evaluate & Log to MLflow
        run: |
          python pipelines/evaluate_and_register.py \
            --index data/index.bin \
            --golden data/golden_qa_v1.jsonl \
            --embedder "${{ inputs.embedders || 'BAAI/bge-base-en-v1.5' }}" \
            --chunk-size ${{ inputs.chunk_size || '500' }}

  # Stage 3: Contract Testing & Promotion Gate
  contract-and-promote:
    needs: [chunk-and-embed]
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12', cache: 'pip' }
      - run: pip install -e .[dev]
      - name: Run Model Contract Suite Against @candidate
        run: pytest tests/contract/ -v --tb=short
      - name: Promote Model to Staging on Green Tests
        if: success() && inputs.promote_to == 'staging'
        run: python experiments/promote_best_model.py --target-alias staging
```

---

## 3. Topic Lab: The AskMyNotes Production Layout & Dockerfile

### 3.1 Repository File Tree

```
askmynotes/
├── pyproject.toml                     # Unified tool config (ruff, black, mypy, pytest)
├── .pre-commit-config.yaml            # Local git commit hooks
├── Dockerfile                         # Production multi-stage container
├── dvc.yaml                           # DVC pipeline DAG definition
├── params.yaml                        # DVC pipeline parameters
├── README.md                          # Quickstart, architecture, 5 badges
│
├── askmynotes/                        # Core Python Application Package
│   ├── __init__.py
│   ├── chunker.py                     # Text chunking logic
│   ├── loader.py                      # PDF loading & text extraction
│   ├── embedder.py                    # HuggingFace vector embedding
│   ├── vector_store.py                # FAISS vector indexing
│   ├── retrieval.py                   # Semantic search & reranker
│   ├── eval.py                        # MAP@K, MRR, NDCG calculation
│   ├── data.py                        # Golden Q&A loader
│   └── serving.py                     # FastAPI service loading model by alias
│
├── tests/                             # Automated Test Suites
│   ├── conftest.py                    # Shared fixtures & test config
│   ├── test_chunker.py                # Parametrized unit tests
│   ├── test_loader.py                 # PDF loader unit tests
│   ├── test_retrieval.py              # Mocked vector search tests
│   ├── integration/
│   │   └── test_end_to_end.py         # Full pipeline integration
│   └── contract/
│       └── test_retriever_contract.py # Model contract test suite
│
├── pipelines/                         # Standalone Training Pipeline Stages
│   ├── extract_pdfs.py
│   ├── chunk.py
│   ├── embed.py
│   ├── build_index.py
│   └── evaluate_and_register.py
│
├── experiments/                       # MLflow CLI & Promotion Scripts
│   ├── track_run.py
│   ├── find_best_run.py
│   └── promote_best_model.py
│
├── data/                              # DVC-Tracked Data Pointers
│   ├── raw_pdfs.dvc
│   └── golden_qa_v1.jsonl.dvc
│
└── .github/workflows/                 # CI/CD & Automation Pipelines
    ├── ci.yml                         # Code CI (per push/PR)
    ├── train.yml                      # Training DAG (cron/drift)
    └── deploy.yml                     # Continuous Delivery (per main push)
```

---

### 3.2 Production Multi-Stage `Dockerfile`

```dockerfile
# Multi-stage build: discards compilers and build tooling for a slim 250MB image
# ------------------------------------------------------------------------------
# Stage 1: Builder (Installs dependencies into wheels)
# ------------------------------------------------------------------------------
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
COPY askmynotes/__init__.py askmynotes/

RUN pip install --upgrade pip build && \
    pip wheel --wheel-dir=/wheels .

# ------------------------------------------------------------------------------
# Stage 2: Runtime (Minimal attack surface, non-root execution)
# ------------------------------------------------------------------------------
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080 \
    MODEL_NAME=AskMyNotesRetriever \
    MODEL_ALIAS=production

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Security: Run as unprivileged non-root user
RUN groupadd -r app && useradd -r -g app -d /app -s /sbin/nologin app
WORKDIR /app

# Install wheels directly from builder stage
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir --no-index --find-links=/wheels /wheels/*.whl && \
    rm -rf /wheels

COPY --chown=app:app askmynotes/ askmynotes/

USER app

# Kubernetes / Docker health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:' + '${PORT:-8080}' + '/health').read()" || exit 1

EXPOSE 8080

CMD ["sh", "-c", "uvicorn askmynotes.serving:app --host 0.0.0.0 --port ${PORT} --workers 2"]
```

---

## 4. Topic MLLab: The Six-Milestone Hands-on Walkthrough

```
[ M1: One Tracked Run ] --------------------> [ M2: Sweep of 5 Runs ] --------------------> [ M3: Winner Registered ]
UI shows params/metrics                          Compare view in UI                           @candidate assigned
          |                                                                                            |
          v                                                                                            v
[ M6: Serving by Alias ] <------------------- [ M5: Promote to @production ] <---------------- [ M4: Contract Tests Pass ]
FastAPI loads v1 via alias                       Alias points to v1                           Pytest gates all green
```

### Complete Command Sequence for M1-M6 + Bonus:

```bash
# ==============================================================================
# Terminal 1: Launch Local MLflow Server
# ==============================================================================
cd askmynotes
source .venv/bin/activate
mlflow ui --port 5000 --backend-store-uri sqlite:///mlflow.db

# ==============================================================================
# Terminal 2: Working Terminal
# ==============================================================================
export MLFLOW_TRACKING_URI=http://localhost:5000

# ---- M1: Single Tracked Run ----
python experiments/track_run.py --model 'BAAI/bge-base-en-v1.5' --chunk-size 500 --chunk-overlap 50
# Verify in UI: http://localhost:5000 -> Experiment 'askmynotes-retrieval' -> 1 run exists.

# ---- M2: Parameter Sweep (5 Runs) ----
for size in 200 400 500 600 800; do
  python experiments/track_run.py --model 'BAAI/bge-base-en-v1.5' --chunk-size $size --chunk-overlap 50
done
# Verify in UI: Select all runs -> Click 'Compare' -> inspect MAP@5 vs Latency parallel coordinates.

# ---- M3: Register Best Run to Model Registry ----
python experiments/promote_best_model.py --run-id <winning_run_id> --target-alias candidate
# Verify: Models tab in UI shows AskMyNotesRetriever with @candidate alias.

# ---- M4: Execute Model Contract Quality Gate ----
pytest tests/contract/ -v --tb=short
# Expected: 7 passed, 1 skipped (skip is normal for first release with no prior production version).

# ---- M5: Promote Candidate to @production ----
python -c "
from mlflow import MlflowClient
c = MlflowClient()
mv = c.get_model_version_by_alias('AskMyNotesRetriever', 'candidate')
c.set_registered_model_alias('AskMyNotesRetriever', 'production', mv.version)
print(f'Promoted v{mv.version} -> @production')
"

# ==============================================================================
# Terminal 3: Launch Serving App
# ==============================================================================
export MLFLOW_TRACKING_URI=http://localhost:5000
export MODEL_NAME=AskMyNotesRetriever
export MODEL_ALIAS=production
uvicorn askmynotes.serving:app --host 0.0.0.0 --port 8080

# ==============================================================================
# Terminal 2: Test Live Predictions
# ==============================================================================
curl http://localhost:8080/health
# Response: {"status":"healthy","model_alias":"production"}

curl -X POST http://localhost:8080/rerank \
  -H 'Content-Type: application/json' \
  -d '{"query": "what is chunking?", "candidates": ["chunking splits text into pieces", "paris is in france"]}'
# Response: {"scores": [0.87, 0.12], "model_alias": "production"}

# ==============================================================================
# BONUS: Zero-Code-Change Model Swap & 10-Second Rollback
# ==============================================================================
# 1. Train and register v2:
python experiments/track_run.py --chunk-size 400
python experiments/promote_best_model.py --run-id <run_2_id> --target-alias candidate

# 2. Move @production alias from v1 to v2:
python -c "from mlflow import MlflowClient; MlflowClient().set_registered_model_alias('AskMyNotesRetriever', 'production', 2)"

# 3. Restart serving process (in Terminal 3: Ctrl+C and rerun uvicorn).
# Serving now serves v2. Zero lines of code modified!

# 4. Instant Rollback to v1:
python -c "from mlflow import MlflowClient; MlflowClient().set_registered_model_alias('AskMyNotesRetriever', 'production', 1)"
# Restart serving process. Rollback complete in 10 seconds.
```

---

## 5. Topic Rev: The 90-Second Interview Walkthrough & Traps

### 5.1 The Rehearsed 90-Second Walkthrough
> *"AskMyNotes is a production-baseline RAG system operating on a three-pipeline architecture.*
>
> *First is **Code CI**, running in GitHub Actions on every push. It enforces a three-layer quality defense—Ruff for linting, Black for formatting, Mypy for static typing, and Pytest enforcing 75% branch coverage before branch protection allows a merge.*
>
> *Second is the **Training Pipeline**, triggered nightly on cron or on data drift alerts. It pulls versioned PDF corpora and golden Q&A benchmarks from S3 via DVC, trains vector indices across GPU runners, and logs all metrics and artifacts to MLflow tagged with the Git commit SHA and DVC data hashes for full audit lineage. If the model beats baseline, it is registered under the `@candidate` alias and evaluated against a Pytest Model Contract suite—verifying schema conformance, offline MAP@5 quality floors, latency budgets, fairness across subgroups, and backwards compatibility.*
>
> *Third is **Serving CD**, deployed as a multi-stage Docker container on GHCR. Serving code resolves models dynamically by alias (`models:/AskMyNotesRetriever@production`) rather than hardcoded version numbers. This decouples model release from code deployment—enabling zero-code-change model swaps and 10-second instant rollbacks simply by flipping the alias pointer in the registry."*

---

### 5.2 The 5 Canonical Trap Questions

1. **"What is your target test coverage?"**
   - *Wrong*: "100%."
   - *Right*: "75% to 85% branch coverage. 100% coverage is an anti-pattern that encourages gaming the metric with empty assertions. I prioritize test quality verified through mutation testing over vanity numbers."
2. **"How often should you deploy to production?"**
   - *Wrong*: "Once every two-week sprint."
   - *Right*: "As frequently as changes pass automated safety gates—ideally multiple times per day. DORA research proves higher deployment frequency correlates with lower incident rates because batch sizes are tiny and rollbacks are fast."
3. **"How do you handle a failing or degraded model in production?"**
   - *Wrong*: "Immediately retrain a new model and redeploy."
   - *Right*: "Roll back first, diagnose second. Flip the `@production` alias to the previous known-good version and perform a rolling restart (under 60 seconds). Then inspect data drift, logs, and retrain offline."
4. **"Should every deployment use a Canary strategy?"**
   - *Wrong*: "Yes, Canary is always the safest."
   - *Right*: "Match deployment strategy to blast radius. Rolling updates are ideal for routine infrastructure or non-breaking API changes. Canary is reserved for high-risk ML model changes and user-facing ranking logic requiring live metric telemetry."
5. **"Why can't data science teams just ship Jupyter notebooks?"**
   - *Wrong*: "Because notebooks are bad."
   - *Right*: "Notebooks are fantastic for exploratory data analysis, but dangerous for production auditability. They allow out-of-order cell execution, lack automated linting, hide dependencies, and fail to generate a cryptographic provenance chain linking predictions back to git SHAs and data hashes."
