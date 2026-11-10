# Day 36: Capstone Project, Weekly Assessment, and Mentor PR Review

---

## Syllabus Alignment & Overview

| Topic Code | Module Title | Duration | Core Focus & Real-World Objective |
| :--- | :--- | :--- | :--- |
| **Capstone** | **Full CI/CD Pipeline** | 2 hrs | End-to-end implementation of the `AskMyNotes` production MLOps system; wiring Code CI + Training DAG + Serving CD. |
| **Assessment**| **Weekly Assessment** | 1 hr | 25-question rigorous examination across Git, GitHub, Pytest, CI/CD, and MLOps with detailed explanatory answers. |
| **Review** | **Mentor PR Review** | Bonus | Senior code review rubric; constructive review etiquette; detecting security, anti-patterns, and testing gaps in peer code. |

---

## 1. The Capstone: Complete End-to-End AskMyNotes Implementation

The Capstone connects all five days of learning into a single cohesive, production-grade ML repository.

```
                                  CAPSTONE SYSTEM ARCHITECTURE
                                  
+----------------------------------------------------------------------------------------------------+
|                                    1. LOCAL REPOSITORY SETUP                                       |
|  - Unified pyproject.toml tooling (ruff, black, mypy, pytest)                                      |
|  - Git hygiene & pre-commit hooks (.pre-commit-config.yaml)                                        |
|  - DVC tracking for raw PDF corpora & golden evaluation set (dvc.yaml + params.yaml)               |
+----------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+----------------------------------------------------------------------------------------------------+
|                                      2. CODE CI WORKFLOW                                           |
|  - .github/workflows/ci.yml triggers on PR and push to main                                        |
|  - Quality Gates: Ruff lint -> Black format check -> Mypy typecheck                                |
|  - Automated Test Matrix (Python 3.11 & 3.12) enforcing >= 75% branch coverage                     |
+----------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+----------------------------------------------------------------------------------------------------+
|                                  3. AUTOMATED TRAINING PIPELINE                                    |
|  - .github/workflows/train.yml triggers on nightly cron, data change, or manual dispatch           |
|  - Steps: DVC pull -> Extract PDFs -> Chunk -> HuggingFace Embedding -> Build FAISS Index         |
|  - MLflow Tracking logs params, metrics, artifacts, Git commit SHA, and DVC data hashes            |
|  - Model Contract Gate: Schema check + Offline MAP@5 + Latency budget + Fairness across subgroups  |
|  - Promotion: Advance passing winner to @candidate -> @staging in MLflow Model Registry           |
+----------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+----------------------------------------------------------------------------------------------------+
|                                      4. CONTINUOUS DELIVERY                                        |
|  - .github/workflows/deploy.yml builds multi-stage Docker image on ghcr.io                         |
|  - Fast, secure non-root runtime container (<250MB)                                                |
|  - FastAPI serving app dynamically resolves model via models:/AskMyNotesRetriever@production       |
|  - Promotion to production: Instant alias flip + rolling restart (Zero Code Change!)               |
+----------------------------------------------------------------------------------------------------+
```

---

### 1.1 Complete Production `pyproject.toml`
The single source of truth for the entire Python toolchain:

```toml
[build-system]
requires = ["setuptools>=65.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "askmynotes"
version = "1.0.0"
description = "Production-grade RAG QA and semantic search engine"
readme = "README.md"
requires-python = ">=3.11"
authors = [{ name = "Abhiram Chittampally", email = "abhiram1.chittampally@gmail.com" }]
dependencies = [
    "fastapi>=0.110.0",
    "uvicorn>=0.28.0",
    "mlflow>=2.11.0",
    "sentence-transformers>=2.5.0",
    "faiss-cpu>=1.8.0",
    "pydantic>=2.6.0",
    "pypdf>=4.1.0",
    "boto3>=1.34.0",
]

[project.optional-dependencies]
dev = [
    "ruff>=0.4.4",
    "black>=24.4.2",
    "mypy>=1.10.0",
    "pre-commit>=3.7.0",
    "pytest>=8.1.0",
    "pytest-cov>=5.0.0",
    "pytest-mock>=3.14.0",
    "dvc[s3]>=3.48.0",
]

[tool.ruff]
line-length = 88
target-version = "py312"
select = ["E", "F", "I", "N", "W", "UP", "B", "A", "C4", "T20", "PT"]
ignore = ["E501"]

[tool.black]
line-length = 88
target-version = ["py311", "py312"]

[tool.mypy]
python_version = "3.12"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
minversion = "8.0"
testpaths = ["tests"]
addopts = "-v --tb=short --strict-markers"
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "contract: marks model contract gate tests",
    "integration: marks end-to-end integration tests",
]

[tool.coverage.run]
source = ["askmynotes"]
branch = true

[tool.coverage.report]
fail_under = 75
show_missing = true
exclude_lines = [
    "pragma: no cover",
    "if __name__ == .__main__.:",
    "raise NotImplementedError",
]
```

---

### 1.2 The Complete 12-Command Fresh Clone Bring-Up Sequence

To verify that your repository is production-ready, test this sequence on an empty machine or directory. If every command passes, your MLOps plumbing is 100% operational:

```bash
# 1. Clone repository
git clone https://github.com/abhiram/askmynotes.git
cd askmynotes

# 2. Create isolated Python virtual environment & activate
python -m venv .venv && source .venv/bin/activate

# 3. Install application package and development dependencies in editable mode
pip install -e .[dev]

# 4. Install local pre-commit git hooks
pre-commit install

# 5. Pull versioned datasets from S3 DVC remote
dvc pull

# 6. Start local MLflow tracking server in background
mlflow ui --port 5000 --backend-store-uri sqlite:///mlflow.db &
export MLFLOW_TRACKING_URI=http://localhost:5000

# 7. Execute DVC training pipeline (extract -> chunk -> embed -> evaluate)
dvc repro

# 8. Promote winning model run to @candidate alias
python experiments/promote_best_model.py --run-id $(cat /tmp/run_id.txt) --target-alias candidate

# 9. Run automated Model Contract test suite
pytest tests/contract/ -v

# 10. Advance verified model to @production alias
python -c "
from mlflow import MlflowClient
c = MlflowClient()
c.set_registered_model_alias('AskMyNotesRetriever', 'production', 1)
"

# 11. Launch production FastAPI serving microservice
uvicorn askmynotes.serving:app --host 0.0.0.0 --port 8080 &

# 12. Verify serving endpoint and prediction latency
curl http://localhost:8080/health
curl -X POST http://localhost:8080/rerank \
  -H 'Content-Type: application/json' \
  -d '{"query": "what is MLOps?", "candidates": ["MLOps automates ML pipelines", "Cats like milk"]}'
```

---

## 2. Weekly Assessment: 25 Rigorous Questions & Explanations

### Question 1 (Git Fundamentals)
**What is the core technical difference between `git fetch` and `git pull`?**
- A) `git fetch` updates your local files; `git pull` only inspects the remote.
- B) `git fetch` downloads remote objects and updates remote tracking branches (`origin/main`) without modifying your working tree; `git pull` performs a `git fetch` followed immediately by a `git merge`.
- C) `git fetch` requires an SSH key; `git pull` uses HTTP.
- D) `git fetch` deletes untracked files.
<details>
<summary><b>View Answer & Explanation</b></summary>
<b>Answer: B.</b> `git fetch` is safe and read-only with respect to your working directory. It downloads commits and updates `.git/refs/remotes/origin/*`. `git pull` immediately merges those changes into your current active checked-out branch, which may trigger unintended merge commits or conflicts.
</details>

---

### Question 2 (Git Internals)
**Which Git object type stores raw file contents without storing the file's name or permissions?**
- A) Tree
- B) Commit
- C) Blob
- D) Tag
<details>
<summary><b>View Answer & Explanation</b></summary>
<b>Answer: C.</b> A `blob` (binary large object) stores pure content bytes compressed with zlib. File names, modes, and directory hierarchies are stored in `tree` objects.
</details>

---

### Question 3 (Git Branching)
**Under what circumstance should `git rebase` strictly NEVER be used?**
- A) On a private local feature branch before creating a PR.
- B) When updating your local branch with commits from `main`.
- C) On public, shared branches (like `main` or team branches) that other developers have pulled and based work upon.
- D) When squashing intermediate fixup commits.
<details>
<summary><b>View Answer & Explanation</b></summary>
<b>Answer: C (The Golden Rule of Rebasing).</b> Rebasing rewrites commit SHA hashes. If other developers have based work on those commits, rebasing forces their histories to diverge, resulting in duplicate commits and messy conflict loops.
</details>

---

### Question 4 (Git Recovery)
**An engineer accidentally runs `git reset --hard HEAD~3` on `main`, deleting three commits. What tool allows them to recover the lost commits within 90 days?**
- A) `git revert`
- B) `git fsck --lost-found`
- C) `git reflog`
- D) `git restore`
<details>
<summary><b>View Answer & Explanation</b></summary>
<b>Answer: C.</b> `git reflog` records every update to `HEAD` locally. The engineer can find the commit SHA prior to the reset (e.g. `HEAD@{1}`) and restore it via `git reset --hard <sha>` or `git branch recovery <sha>`.
</details>

---

### Question 5 (Testing Theory)
**In testing economics, what is the primary reason the "Ice-Cream Cone" anti-pattern is detrimental to engineering velocity?**
- A) Unit tests are too expensive to write.
- B) Relying heavily on manual QA and end-to-end tests causes slow execution, high flakiness, and late defect discovery, drastically inflating bug-fix costs.
- C) End-to-end tests have 100% code coverage.
- D) Compilers make unit testing redundant.
<details>
<summary><b>View Answer & Explanation</b></summary>
<b>Answer: B.</b> End-to-end tests are slow, brittle, and non-deterministic. The healthy Test Pyramid places 60-70% of tests at the fast, isolated unit layer.
</details>

---

### Question 6 (Pytest Mechanics)
**What does `yield` do inside a pytest fixture function?**
- A) It returns multiple values in a loop to parametrize the test.
- B) It acts as the boundary separating setup code (executed before the test) from teardown code (guaranteed to execute after the test completes).
- C) It pauses the test for an asynchronous callback.
- D) It skips the test if an exception occurs.
<details>
<summary><b>View Answer & Explanation</b></summary>
<b>Answer: B.</b> Code before `yield` runs during test setup. The value yielded is passed to the test function. Code after `yield` runs during teardown/cleanup, even if assertions fail.
</details>

---

### Question 7 (Mocking)
**When using `mocker.patch`, why must you patch where the object is USED rather than where it is DEFINED?**
- A) Because Python imports bind references into the importing module's namespace; patching the definition module does not alter already-imported references in the target module.
- B) Because unittest.mock only works on local variables.
- C) Because external third-party packages are read-only.
- D) It does not matter; either location works identically.
<details>
<summary><b>View Answer & Explanation</b></summary>
<b>Answer: A.</b> If `retrieval.py` does `from transformers import AutoModel`, patching `transformers.AutoModel` does nothing to `retrieval.AutoModel`. You must patch `askmynotes.retrieval.AutoModel`.
</details>

---

### Question 8 (Code Coverage)
**Why is targeting 100% code coverage considered an anti-pattern in professional engineering?**
- A) Python cannot calculate coverage above 90%.
- B) It incentivizes engineers to write assertion-free tests solely to execute lines, increasing maintenance burden while yielding diminishing returns on actual defect prevention.
- C) Branch coverage and line coverage are mutually exclusive.
- D) High coverage makes CI run slower.
<details>
<summary><b>View Answer & Explanation</b></summary>
<b>Answer: B.</b> High-performing teams target 75-85% branch coverage and measure test effectiveness using mutation testing (`mutmut`) rather than chasing 100% vanity coverage.
</details>

---

### Question 9 (CI/CD Concepts)
**What distinguishes Continuous Delivery from Continuous Deployment?**
- A) Continuous Delivery requires Docker; Continuous Deployment does not.
- B) Continuous Delivery automates staging releases but requires a manual approval gate to deploy to production; Continuous Deployment automatically deploys all green builds directly to production without human intervention.
- C) Continuous Delivery applies only to frontend; Continuous Deployment applies to backend.
- D) Continuous Deployment is only used for machine learning.
<details>
<summary><b>View Answer & Explanation</b></summary>
<b>Answer: B.</b> Continuous Delivery ensures code is always in a releasable state, with human sign-off gating production. Continuous Deployment fully automates the release to production.
</details>

---

### Question 10 (GitHub Actions)
**In a GitHub Actions workflow, why is `needs: [lint]` used between jobs?**
- A) To share memory between runners.
- B) Because GitHub Actions runs all jobs in parallel by default; `needs:` defines DAG dependency sequencing to avoid running expensive test suites if quick lint checks fail.
- C) To pass environment variables.
- D) To grant administrator permissions.
<details>
<summary><b>View Answer & Explanation</b></summary>
<b>Answer: B.</b> Jobs in GitHub Actions are concurrent by default. Declaring `needs:` builds an explicit dependency graph.
</details>

---

### Question 11 (Deployment Strategies)
**Which deployment strategy spins up an identical new environment (Green) alongside the active environment (Blue) and switches traffic at the router level?**
- A) Recreate
- B) Rolling Update
- C) Blue/Green Deployment
- D) Canary Deployment
<details>
<summary><b>View Answer & Explanation</b></summary>
<b>Answer: C.</b> Blue/Green provides zero downtime and near-instantaneous rollback capability at the expense of doubling infrastructure capacity during deployment.
</details>

---

### Question 12 (Continuous Delivery)
**What does the "Build-Once-Deploy-Many" principle dictate?**
- A) You should run `docker build` separately on dev, staging, and production machines.
- B) You build a single immutable artifact (e.g. Docker image tagged with Git SHA) once in CI, and promote that exact artifact across all environments, changing only configuration and secrets.
- C) You only build containers on the master branch.
- D) You build code once a week.
<details>
<summary><b>View Answer & Explanation</b></summary>
<b>Answer: B.</b> Rebuilding containers between staging and production introduces subtle non-deterministic dependency differences. Promote the exact same binary hash.
</details>

---

### Question 13 (MLOps Core)
**Which of the following is a failure mode unique to machine learning that traditional software does not encounter?**
- A) Null pointer exceptions
- B) Memory leaks
- C) Data and concept drift (input distributions changing over time while the code runs without throwing errors)
- D) Port binding collisions
<details>
<summary><b>View Answer & Explanation</b></summary>
<b>Answer: C.</b> Traditional software fails loudly with crash logs. ML systems fail silently: the service returns HTTP 200 OK, but predictions degrade due to distribution shift.
</details>

---

### Question 14 (DVC Mechanics)
**Why does DVC use `.dvc` files in Git rather than committing datasets directly to Git?**
- A) Git cannot read JSON or CSV files.
- B) Storing multi-gigabyte binary datasets directly in Git causes repository bloat, permanently slowing down every clone and checkout operation for all developers.
- C) DVC files encrypt the data.
- D) Git deletes files over 1MB automatically.
<details>
<summary><b>View Answer & Explanation</b></summary>
<b>Answer: B.</b> Git's object database stores compressed full snapshots of binary changes. A 5GB dataset updated 4 times bloats a repo to 20GB. DVC keeps Git lean by storing only 200-byte content hashes.
</details>

---

### Question 15 (DVC Operations)
**What command downloads the actual dataset blobs from cloud remote storage based on the `.dvc` pointer files currently in the working directory?**
- A) `git pull`
- B) `dvc fetch --all`
- C) `dvc pull`
- D) `dvc checkout --force`
<details>
<summary><b>View Answer & Explanation</b></summary>
<b>Answer: C.</b> `dvc pull` combines `dvc fetch` (downloading missing blobs from remote storage into local cache) and `dvc checkout` (linking blobs into the active working tree).
</details>

---

### Question 16 (MLflow Tracking)
**What are the three components of the MLflow experiment tracking trichotomy?**
- A) Code, Data, Models
- B) Parameters (fixed inputs), Metrics (scalar performance values), and Artifacts (output files/weights)
- C) CPU, GPU, TPU
- D) Unit, Integration, E2E
<details>
<summary><b>View Answer & Explanation</b></summary>
<b>Answer: B.</b> MLflow structures telemetry into: `params` (logging configuration), `metrics` (logging floating-point evaluation numbers across steps), and `artifacts` (persisting files, plots, and models).
</details>

---

### Question 17 (MLflow Model Registry)
**In modern MLflow (2.8+), what replaced the deprecated legacy concept of fixed stages (`Staging`, `Production`)?**
- A) Git branches
- B) Mutable Aliases (e.g. `@candidate`, `@staging`, `@production`)
- C) Folders in S3
- D) Docker tags
<details>
<summary><b>View Answer & Explanation</b></summary>
<b>Answer: B.</b> Aliases act as mutable named pointers pointing to immutable model version numbers, providing greater flexibility and cleaner multi-environment deployment semantics.
</details>

---

### Question 18 (Serving Architecture)
**Why should model serving microservices NEVER hardcode model versions (e.g. `models:/Model/1`)?**
- A) Because MLflow cannot serve version 1.
- B) Because hardcoded versions require modifying code, opening PRs, running CI, and rebuilding containers for every single model update; loading by alias (`@production`) allows instantaneous model updates and rollbacks with zero code changes.
- C) Because version numbers are random strings.
- D) Because Python cannot parse integers in URLs.
<details>
<summary><b>View Answer & Explanation</b></summary>
<b>Answer: B.</b> Decoupling model release from code deployment is a foundational MLOps requirement. Serving code references `@production`, and the registry updates the pointer.
</details>

---

### Question 19 (Model Contracts)
**What is a Model Contract test?**
- A) A legal contract signed between the data scientist and product manager.
- B) An automated test suite executed in CI against a candidate model before promotion, validating input/output schemas, latency budgets, offline metric floors, and backwards compatibility.
- C) A runtime monitor that alerts when API costs exceed budgets.
- D) A database schema migration script.
<details>
<summary><b>View Answer & Explanation</b></summary>
<b>Answer: B.</b> Model contracts are the ML equivalent of unit tests for code, acting as an automated gate that prevents degraded models from reaching staging or production.
</details>

---

### Question 20 (Three-Pipeline Architecture)
**Why is combining Code CI and the ML Training Pipeline into a single workflow considered a major anti-pattern?**
- A) YAML syntax cannot support both.
- B) They operate on completely different clocks, require different compute resources, have different failure modes, and are owned by different personas; a code documentation fix should not trigger a 45-minute GPU training run.
- C) GitHub Actions only allows one workflow file per repo.
- D) It violates the Linux philosophy.
<details>
<summary><b>View Answer & Explanation</b></summary>
<b>Answer: B.</b> Code CI runs per commit on fast CPUs (<5 min). Training runs on cron, drift alerts, or manual dispatch on expensive GPUs. Coupling them burns compute and paralyzes team velocity.
</details>

---

### Question 21 (Data Lineage)
**Which combination of tools provides complete provenance linking a production prediction back to code, data, and parameters?**
- A) Git + Docker
- B) Git (commit SHA) + DVC (data content hash) + MLflow (run parameters & artifacts)
- C) Pytest + Black
- D) FastAPI + Uvicorn
<details>
<summary><b>View Answer & Explanation</b></summary>
<b>Answer: B.</b> MLflow logs `git.sha` and `dvc.data_hash` as run tags. This allows an engineer to check out the exact commit and pull the exact dataset to reproduce any historical model.
</details>

---

### Question 22 (Pre-Commit Gates)
**How does a team prevent configuration drift between local developer formatting and remote CI formatting checks?**
- A) By forbidding developers from using formatters locally.
- B) By running `pre-commit/action@v3` directly inside the GitHub Actions CI pipeline, using the exact same `.pre-commit-config.yaml` committed to the repo.
- C) By manually reviewing all spaces in pull requests.
- D) By disabling branch protection.
<details>
<summary><b>View Answer & Explanation</b></summary>
<b>Answer: B.</b> Using the same `.pre-commit-config.yaml` locally and in CI guarantees that checks executed on developer laptops match the remote CI gates with zero drift.
</details>

---

### Question 23 (Production Rollback)
**What is the fastest and safest way to roll back a degraded ML model in a mature MLOps system?**
- A) Retrain a new model from scratch.
- B) Revert the Git commit that trained the model.
- C) Flip the `@production` alias in the MLflow Model Registry to point to the prior known-good model version and execute a rolling restart of the serving pods (< 60 seconds).
- D) Delete the database.
<details>
<summary><b>View Answer & Explanation</b></summary>
<b>Answer: C.</b> Roll back first, diagnose second. Alias-based rollback requires no code change, no container rebuild, and restores safety in under a minute.
</details>

---

### Question 24 (Docker Multi-Stage)
**What is the primary benefit of multi-stage Docker builds for Python ML serving images?**
- A) They make Python execute faster.
- B) They keep the final runtime container image small (< 250MB) and secure by discarding compilers (`gcc`, `build-essential`), git, and build caches, copying only wheels and production code into the final runtime stage.
- C) They allow running multiple operating systems simultaneously.
- D) They bypass Linux permissions.
<details>
<summary><b>View Answer & Explanation</b></summary>
<b>Answer: B.</b> Multi-stage builds prevent build tools and intermediate bloat from leaking into production, reducing attack surface and container pull/start times.
</details>

---

### Question 25 (ML Pipeline Orchestration)
**When should a team graduate from GitHub Actions training workflows to an orchestrator like Prefect or Apache Airflow?**
- A) When they have more than 1 repository.
- B) When they manage 15+ complex pipelines requiring Python-native task semantics, dynamic retries with exponential backoff, cross-pipeline lineage, and dedicated data-platform infrastructure.
- C) As soon as they write their first Python script.
- D) Never; GitHub Actions is always sufficient for all enterprise workloads.
<details>
<summary><b>View Answer & Explanation</b></summary>
<b>Answer: B.</b> GitHub Actions is ideal for small teams and linear pipelines. When workflows scale to dozens of interrelated DAGs with complex retries and data dependencies, dedicated orchestrators become necessary.
</details>

---

## 3. Mentor PR Review Guide: Senior Engineering Rubric

When reviewing pull requests from teammates or junior engineers, evaluate the submission across five structured dimensions:

### 3.1 The 5-Point Code Review Rubric
1. **Correctness & Edge Cases**:
   - Does the logic handle empty inputs, null values, network timeouts, and boundary conditions?
2. **Test Quality & Coverage**:
   - Are new branches covered by unit tests? Do tests assert state rather than just calling functions? Are external APIs mocked?
3. **Security & Secrets**:
   - Are API keys, AWS credentials, or hardcoded passwords present? Does the code expose sensitive data in error traces?
4. **Performance & Resource Hygiene**:
   - Are files read into memory eagerly or streamed as generators? Are database/network connections reused via connection pooling?
5. **Architectural Consistency & Typing**:
   - Does the code adhere to project type annotations (`mypy`)? Are functions small and single-purpose?

---

### 3.2 Constructive Review Comment Framing
Use conventional prefixes to clarify the priority of review comments:
- **`[BLOCKING]`**: Must be addressed before merge (e.g. security risk, missing test for critical branch, data corruption bug).
- **`[SUGGESTION]`**: Non-blocking recommendation for improved readability, idiomatic Python, or minor optimization.
- **`[QUESTION]`**: Inquiring about design intent or requesting clarification on complex logic.
- **`[NIT]`**: Minor non-blocking style preference (e.g. variable naming clarity).

#### Example Senior Reviewer Feedback:
> `askmynotes/embedder.py:48`
> **`[BLOCKING]`**: Loading the SentenceTransformer model inside the function body causes the model weights to be re-instantiated from disk on every single request. Please move model loading to module scope or wrap in a `@lru_cache` fixture to prevent a 2-second latency penalty per query.
>
> `tests/test_retrieval.py:12`
> **`[SUGGESTION]`**: This test makes an outbound network call to HuggingFace to download weights during the test run. Let's use `pytest-mock` (`mocker.patch('askmynotes.retrieval.compute_embeddings')`) so unit tests run completely offline and finish in under 20ms.
