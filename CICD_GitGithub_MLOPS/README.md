# Week 7: CI/CD, Git/GitHub, and MLOps Masterclass

[![CI](https://github.com/abhiram/askmynotes/actions/workflows/ci.yml/badge.svg)](https://github.com/abhiram/askmynotes/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/coverage-85%25-brightgreen)](https://github.com/abhiram/askmynotes)
[![Quality Gate](https://img.shields.io/badge/quality--gate-ruff%20%7C%20black%20%7C%20mypy-blue)](https://github.com/abhiram/askmynotes)
[![Docker](https://img.shields.io/badge/docker-ghcr.io-blue)](https://github.com/abhiram/askmynotes)
[![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue)](https://www.python.org/)

---

## Executive Overview & Master Repository Navigation

This repository contains the complete curriculum, implementation guides, production code templates, and interview prep material for **Week 7: CI/CD + Git/GitHub + MLOps Basics (Days 31–36)** of the KMIT Talent Accelerator Program.

All concepts, code samples, architecture patterns, and assessment rubrics are anchored around **`AskMyNotes`**, a production-grade RAG QA and semantic search engine.

```
+---------------------------------------------------------------------------------------------------------+
|                                          SYSTEM ARCHITECTURE                                            |
|                                                                                                         |
|       [ Git (Code SHA) ]      +      [ DVC (Data MD5) ]      +      [ MLflow (Tracking & Registry) ]     |
|              |                              |                                      |                    |
|              v                              v                                      v                    |
|   +---------------------+        +---------------------+                +---------------------+         |
|   |   1. CODE CI (CI)   |        | 2. TRAINING PIPELINE|                |  3. SERVING CD (CD) |         |
|   |---------------------|        |---------------------|                |---------------------|         |
|   | • Trigger: git push |        | • Trigger: cron/    |                | • Trigger: alias    |         |
|   | • Ruff + Black +    |        |   drift/dispatch    |                |   move (@production)|         |
|   |   Mypy + Pytest     |        | • DVC pull -> train |                | • Multi-stage Docker|         |
|   | • Branch Protection |        | • Model Contracts   |                |   deployment        |         |
|   | • Cadence: minutes  |        | • MLflow @candidate |                | • 10-sec rollback   |         |
|   +---------------------+        +---------------------+                +---------------------+         |
+---------------------------------------------------------------------------------------------------------+
```

---

## Table of Contents & Syllabus Cross-Walk

| File | Day & Track | Focus Modules & Topics Covered |
| :--- | :--- | :--- |
| **[Day 31: Git Fundamentals](Day_31_Git_Fundamentals.md)** | **MON (Day 31)**<br>Git Basics | • **B1**: Why Version Control Exists (The folder of death, centralized vs distributed)<br>• **B2**: Git vs GitHub (Local engine vs cloud platform, cryptographic identity)<br>• **B3**: Core Git Workflow (Working tree $\rightarrow$ Staging index $\rightarrow$ Repo history)<br>• **B4**: Repositories & Remotes (`clone`, `fetch`, `merge`, `pull`, `push`)<br>• **B5**: `.gitignore` & Commit Hygiene (Secrets hygiene, Conventional Commits) |
| **[Day 32: Git & GitHub Mastery](Day_32_Git_GitHub_Mastery.md)** | **TUE (Day 32)**<br>6A Git Mastery | • **6.1**: Branching Strategies (Trunk-Based vs GitHub Flow vs GitFlow)<br>• **6.2**: Rebasing & Cherry-Picking (`rebase -i`, squash, clean linear history)<br>• **6.3**: Merge Conflict Resolution (Anatomy of markers, 5-step ritual, aborts)<br>• **6.4**: PR Etiquette & Review (<400 lines, PR templates, branch protection)<br>• **6.5**: Git Internals & Recovery (Blobs, trees, commits, tags, `reflog`, `reset`) |
| **[Day 33: Testing & Continuous Integration](Day_33_Testing_and_CI.md)** | **WED (Day 33)**<br>6B Testing & CI | • **T1**: Why Test? (The bug-cost curve, confidence argument, FIRST principles)<br>• **6.6**: pytest Advanced (Fixtures, scopes, yield teardown, parametrize, mocking)<br>• **6.7**: Coverage & Test Pyramid (Unit/Integration/E2E, branch coverage, mutmut)<br>• **CI1**: What is CI/CD? (Definitions, pipeline concept, DORA metrics)<br>• **6.8**: GitHub Actions (Workflows, jobs, steps, runners, pip caching, matrix builds) |
| **[Day 34: Quality Gates, CD, and MLOps](Day_34_Quality_Gates_CD_and_MLOps.md)** | **THU (Day 34)**<br>Quality & MLOps | • **6.9**: Quality-Gate Workflow (Three-layer defense, `ruff`, `black`, `mypy`, pre-commit)<br>• **6.10**: Continuous Delivery Basics (Build-once-deploy-many, 5 deploy strategies)<br>• **M1**: What is MLOps? (Notebooks vs prod, 3 unique ML failure modes, Google L0-L2)<br>• **6.11a**: MLflow Tracking (Params, metrics, artifacts, UI comparison, search_runs)<br>• **6.11b**: MLflow Model Registry (Immutable versions, mutable aliases, dynamic loading) |
| **[Day 35: CI/CD for ML & Lab Walkthrough](Day_35_CICD_for_ML_Pipelines.md)** | **FRI (Day 35)**<br>ML Pipelines | • **6.12a**: CI/CD for ML (DVC data versioning, full provenance lineage, model contracts)<br>• **6.12b**: ML Pipeline Automation (DAG mental model, orchestrator landscape, train.yml)<br>• **Lab**: Full Pipeline Lab (AskMyNotes repo tree, 12-command bring-up, Dockerfile)<br>• **MLLab**: MLflow + CI Lab (M1-M6 milestones, zero-code swap, 10-sec rollback)<br>• **Rev**: Consolidation & Q&A (30 interview questions, 5 trap questions, 90-sec pitch) |
| **[Day 36: Capstone Project & Assessment](Day_36_Capstone_and_Assessment.md)** | **SAT (Day 36)**<br>Capstone & Review | • **Capstone**: Full CI/CD Pipeline (`AskMyNotes` end-to-end implementation & configs)<br>• **Assessment**: 25-Question Comprehensive Weekly Assessment with Answers<br>• **Review**: Senior Mentor PR Review Rubric & Constructive Feedback Guide |

---

## The 12-Command Fresh Clone Bring-Up

Run these 12 commands on any fresh machine or container to bring up the complete local MLOps stack:

```bash
# 1. Clone repository
git clone https://github.com/abhiram/askmynotes.git && cd askmynotes

# 2. Virtual environment setup
python -m venv .venv && source .venv/bin/activate

# 3. Install dependencies in editable mode
pip install -e .[dev]

# 4. Install local git hooks
pre-commit install

# 5. Pull DVC versioned datasets from S3 remote
dvc pull

# 6. Start local MLflow server
mlflow ui --port 5000 --backend-store-uri sqlite:///mlflow.db &
export MLFLOW_TRACKING_URI=http://localhost:5000

# 7. Run training pipeline locally via DVC
dvc repro

# 8. Promote winning run to @candidate alias
python experiments/promote_best_model.py --run-id $(cat /tmp/run_id.txt) --target-alias candidate

# 9. Run automated Model Contract test suite
pytest tests/contract/ -v

# 10. Advance verified model to @production alias
python -c "from mlflow import MlflowClient; MlflowClient().set_registered_model_alias('AskMyNotesRetriever', 'production', 1)"

# 11. Launch production FastAPI serving app
uvicorn askmynotes.serving:app --host 0.0.0.0 --port 8080 &

# 12. Verify serving endpoint and prediction latency
curl http://localhost:8080/health
curl -X POST http://localhost:8080/rerank -H 'Content-Type: application/json' -d '{"query":"what is MLOps?","candidates":["MLOps automates ML","unrelated"]}'
```

---

## The Rehearsed 90-Second Interview Walkthrough

> *"AskMyNotes is a production-baseline RAG system operating on a three-pipeline architecture.*
>
> *First is **Code CI**, running in GitHub Actions on every push. It enforces a three-layer quality defense—Ruff for linting, Black for formatting, Mypy for static typing, and Pytest enforcing 75% branch coverage before branch protection allows a merge.*
>
> *Second is the **Training Pipeline**, triggered nightly on cron or on data drift alerts. It pulls versioned PDF corpora and golden Q&A benchmarks from S3 via DVC, trains vector indices across GPU runners, and logs all metrics and artifacts to MLflow tagged with the Git commit SHA and DVC data hashes for full audit lineage. If the model beats baseline, it is registered under the `@candidate` alias and evaluated against a Pytest Model Contract suite—verifying schema conformance, offline MAP@5 quality floors, latency budgets, fairness across subgroups, and backwards compatibility.*
>
> *Third is **Serving CD**, deployed as a multi-stage Docker container on GHCR. Serving code resolves models dynamically by alias (`models:/AskMyNotesRetriever@production`) rather than hardcoded version numbers. This decouples model release from code deployment—enabling zero-code-change model swaps and 10-second instant rollbacks simply by flipping the alias pointer in the registry."*
