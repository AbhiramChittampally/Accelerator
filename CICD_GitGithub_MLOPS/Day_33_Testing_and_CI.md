# Day 33: Testing & Continuous Integration (CI)

---

## Syllabus Alignment & Overview

| Topic Code | Module Title | Duration | Core Focus & Real-World Objective |
| :--- | :--- | :--- | :--- |
| **T1** | **Why Test? (Basics)** | 30m | The bug-cost curve; the confidence argument; FIRST principles of production testing. |
| **6.6** | **pytest Advanced** | 45m | Shared fixtures (`conftest.py`), fixture scopes, `yield` teardown, `@pytest.mark.parametrize`, mocking external APIs (`mocker`, `monkeypatch`). |
| **6.7** | **Coverage & Test Pyramid** | 45m | Unit vs Integration vs E2E; the ice-cream cone anti-pattern; line vs branch coverage (`pytest-cov`); mutation testing (`mutmut`). |
| **CI1** | **What is CI/CD? (Basics)** | 30m | Definitions of CI, CD, and Continuous Deployment; pipeline concept; DORA metrics for high-performing teams. |
| **6.8** | **GitHub Actions** | 45m | Workflows, jobs, steps, runners, dependency graphs (`needs:`), matrix strategy, pip dependency caching, production `ci.yml`. |

---

## 1. Topic T1: Why Test? (The Economic & Confidence Argument)

### 1.1 The Exponential Bug-Cost Curve
Finding and fixing software defects is not uniformly expensive. The cost increases by roughly $10\times$ at every stage of the delivery lifecycle:

```
Cost to Fix
    ^
$10,000 |                                                         [ Production Outage ]
        |                                                        (Data loss, SLA penalty)
 $1,000 |                                            [ Staging / QA ]
        |                                       (Manual ticket, re-testing)
   $100 |                           [ CI Pipeline ]
        |                      (Blocked PR, 3 min fix)
    $10 |      [ Local Unit Test ]
        |   (Red underline in editor)
        +----------------------------------------------------------------------------->
             Coding            CI Build            Staging             Production
```

### 1.2 The Confidence Argument
Automated testing is not written to prove that code works today. It is written to provide **fearless refactoring** tomorrow. Without automated tests, engineers become terrified of touching working code, technical debt compounds, and velocity slows to a halt.

### 1.3 The F.I.R.S.T. Principles of Unit Testing
1. **Fast**: Tests must execute in milliseconds. If a test suite takes 20 minutes, engineers will bypass it.
2. **Independent**: No test should depend on the state or execution order of another test. Tests must be able to run concurrently.
3. **Repeatable**: A test must yield the exact same result whether run on a developer laptop, inside a GitHub Actions runner, or on a staging server, with zero external network dependencies.
4. **Self-Validating**: The test must have a binary outcome (pass or fail). No human inspection of print statements or log files is required.
5. **Timely**: Tests should be written concurrently with or immediately before the production code (TDD).

---

## 2. Topic 6.6: Advanced pytest (Fixtures, Parametrization, Mocking)

`pytest` is the undisputed industry standard testing framework for Python and ML systems.

### 2.1 Fixture Mechanics, Scopes, and Teardown
Fixtures provide a reliable, modular way to set up data, connections, or state before tests run and clean them up afterward.

#### Fixture Scopes:
- `function` *(default)*: Created and destroyed for every single test function.
- `class`: Shared across all methods within a test class.
- `module`: Created once per test file (`.py`). Ideal for loading heavy ML models or database connections.
- `session`: Created once for the entire test run across all files.

#### Comprehensive `conftest.py` with Setup and Teardown:
```python
# tests/conftest.py
"""Shared pytest fixtures across unit, integration, and contract test suites."""

from pathlib import Path
import tempfile
import pytest


# Shared sample documents fixture
@pytest.fixture(scope="session")
def sample_documents() -> list[dict[str, str]]:
  """Session-scoped fixture providing dummy documents for chunker and embedder tests."""
  return [
      {
          "id": "doc_1",
          "text": (
              "MLOps stands for Machine Learning Operations. It encompasses"
              " continuous integration, data versioning, and automated"
              " deployment."
          ),
      },
      {
          "id": "doc_2",
          "text": (
              "Pytest fixtures manage test setup and teardown cleanly across"
              " multiple scopes."
          ),
      },
  ]


# Yield fixture demonstrating resource allocation and guaranteed cleanup
@pytest.fixture(scope="function")
def temporary_data_dir() -> Path:
  """Function-scoped yield fixture providing an isolated temporary directory.

  Ensures guaranteed teardown/cleanup even if the test fails.
  """
  temp_dir = tempfile.TemporaryDirectory()
  dir_path = Path(temp_dir.name)

  # Hand control to the test function
  yield dir_path

  # Teardown logic runs automatically after test completion
  temp_dir.cleanup()
```

---

### 2.2 Table-Driven Testing with `@pytest.mark.parametrize`
Instead of writing 5 copy-pasted test functions for different edge cases, parametrize executes the same test logic across multiple input-output tuples with independent test reporting.

```python
# tests/test_chunker.py
import pytest
from askmynotes.chunker import chunk_text


@pytest.mark.parametrize(
    "text, chunk_size, overlap, expected_chunk_count",
    [
        ("Short sentence under fifty chars.", 500, 50, 1),  # Simple small text
        ("Word " * 250, 500, 50, 3),  # Multi-chunk text
        ("", 500, 50, 0),  # Empty string edge case
        ("Exact length test", 17, 0, 1),  # Exact boundary
    ],
    ids=["single_chunk", "multiple_chunks", "empty_input", "exact_boundary"],
)
def test_chunk_text_various_lengths(
    text: str, chunk_size: int, overlap: int, expected_chunk_count: int
):
  # Line 1: Call production chunking function with parametrized arguments
  chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)

  # Line 2: Assert expected chunk count matches specification
  assert len(chunks) == expected_chunk_count

  # Line 3: Ensure no chunk exceeds declared chunk_size
  for chunk in chunks:
    assert len(chunk) <= chunk_size
```

---

### 2.3 Mocking External Dependencies (`pytest-mock` & `monkeypatch`)

#### The Golden Rule of Mocking:
> **"Patch where the object is USED, not where it was DEFINED."**
> If `askmynotes/retrieval.py` imports `openai` and calls `openai.embeddings.create`, patch `askmynotes.retrieval.openai`, NOT `openai.embeddings.create`.

#### Complex Production Example: Mocking Hugging Face API Call
```python
# tests/test_retrieval.py
from askmynotes.retrieval import semantic_search
import pytest


def test_semantic_search_with_mocked_model(mocker, sample_documents):
  """Verify semantic search logic without downloading a 500MB Hugging Face model."""
  # Line 1: Define a fake return value for vector embeddings (3-dimensional vectors)
  fake_embeddings = [[0.1, 0.2, 0.3], [0.9, 0.8, 0.7]]

  # Line 2: Patch the embedding generator function where it is imported inside retrieval.py
  mock_embedder = mocker.patch(
      "askmynotes.retrieval.compute_embeddings", return_value=fake_embeddings
  )

  # Line 3: Execute the function under test
  results = semantic_search(query="What is MLOps?", docs=sample_documents, top_k=1)

  # Line 4: Assertions on the mock execution
  assert mock_embedder.call_count == 1
  mock_embedder.assert_called_with(["What is MLOps?"])

  # Line 5: Assert business logic correctness on returned candidates
  assert len(results) == 1
  assert results[0]["id"] == "doc_1"
```

---

## 3. Topic 6.7: Coverage & The Test Pyramid

### 3.1 The Test Pyramid vs The Ice-Cream Cone

```
      THE HEALTHY TEST PYRAMID                       THE ICE-CREAM CONE ANTI-PATTERN
               /\                                                /==============\
              /  \                                              /   Manual QA    \  (Slow, Flaky,
             / E2E\  (5-10%, Real End-to-End)                  /   & UI Tests     \  Expensive)
            /------\                                          /--------------------\
           / Integr \  (20-30%, Component wiring)            /   Integration Tests  \
          /----------\                                      /------------------------\
         /    Unit    \  (60-70%, Fast, isolated)          /        Unit Tests        \ (Neglected, sparse)
        /--------------\                                  /----------------------------\
```

### 3.2 Line Coverage vs Branch Coverage

```bash
# Run pytest with branch coverage reporting
pytest --cov=askmynotes --cov-report=term-missing --cov-branch --cov-fail-under=75
```

#### Why Line Coverage Lies:
```python
def classify_latency(latency_ms: float) -> str:
  status = "normal"
  if latency_ms > 200:
    status = "high"
  return status
```
If you test this function *only* with `classify_latency(250)`, **line coverage is 100%**!
However, the branch where `latency_ms <= 200` was **never executed**. **Branch coverage** tracks every possible decision branch (`True` and `False`) through control structures (`if/else`, `try/except`), exposing untested paths.

#### Target Coverage Thresholds:
- **75% – 85% Branch Coverage**: The production sweet spot for backend services and ML pipelines.
- **100% Coverage Target**: A dangerous anti-pattern. Engineers game the metric by writing superficial tests without assertions just to touch lines, while spending disproportionate time testing trivial getters and boilerplate.

### 3.3 Mutation Testing (`mutmut`)
How do you know your tests are actually catching bugs?
**Mutation testing** automatically introduces deliberate faults (mutants) into your source code (e.g., changing `>` to `<`, `+` to `-`, or replacing a return value with `None`) and re-runs your test suite.
- If your tests fail: The mutant was **killed** (High quality test!).
- If your tests pass: The mutant **survived** (Weak test with missing assertions!).

---

## 4. Topic CI1: What is CI/CD? (Basics & Metrics)

### 4.1 The Core Definitions

```
[ Developer Commit ] ---> [ Continuous Integration (CI) ] ---> [ Continuous Delivery (CD) ] ---> [ Continuous Deployment ]
                                (Build, Lint, Test)              (Automated Deploy to Staging,       (Automated Deploy
                                                                 Manual Gate to Production)          Directly to Production)
```

1. **Continuous Integration (CI)**:
   - Developers merge code frequently (daily) into a shared mainline branch.
   - Every commit triggers an automated build and test pipeline.
   - Goal: Immediate feedback; catch integration bugs within minutes.
2. **Continuous Delivery (CD)**:
   - Builds on CI. Every change that passes automated tests is automatically packaged into a release artifact (Docker container, wheel) and deployed to staging.
   - Promotion to production is a **one-click manual human approval**.
3. **Continuous Deployment (CD)**:
   - Takes Continuous Delivery one step further: eliminates the manual human approval gate. Every change that passes all automated tests and safety gates rolls directly into production automatically.

### 4.2 The Four DORA Metrics (DevOps Research and Assessment)
1. **Deployment Frequency**: How often code is successfully deployed to production (Elite teams: multiple times per day).
2. **Lead Time for Changes**: Time elapsed from commit to running in production (Elite: < 1 hour).
3. **Change Failure Rate**: Percentage of deployments requiring immediate hotfix or rollback (Elite: 0% - 15%).
4. **Time to Restore Service (MTTR)**: Time taken to recover from a production outage (Elite: < 1 hour).

---

## 5. Topic 6.8: GitHub Actions Workflow Architecture

### 5.1 The Core Concepts
1. **Workflow**: An automated configurable process defined in a `.github/workflows/<name>.yml` file.
2. **Event (`on:`)**: Triggers that start the workflow (e.g. `push`, `pull_request`, `schedule`, `workflow_dispatch`).
3. **Job**: A sequence of steps executed on a specific virtual runner. Jobs run in **parallel by default**. You create sequential dependencies using `needs: [job_name]`.
4. **Step**: An individual task executing either a pre-built Action (`uses:`) or shell script commands (`run:`).
5. **Runner**: The VM or container executing the job (e.g., `ubuntu-latest`, `windows-latest`, `self-hosted`).

### 5.2 Production-Grade `.github/workflows/ci.yml`

```yaml
name: Continuous Integration

# Triggers: Run on pushes to main and every pull request targeting main
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

concurrency:
  # Cancel redundant in-flight builds if a developer pushes new commits to the same PR
  group: ci-${{ github.ref }}
  cancel-in-progress: true

jobs:
  # ----------------------------------------------------------------------------
  # Job 1: Static Analysis & Code Hygiene (Fast feedback, fails early)
  # ----------------------------------------------------------------------------
  lint:
    name: Lint & Type Check
    runs-on: ubuntu-latest
    timeout-minutes: 10

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Setup Python 3.12
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: "pip"  # Caches downloaded wheels across workflow runs

      - name: Install Development Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install ruff black mypy

      - name: Run Ruff (Rust-fast Linter)
        run: ruff check .

      - name: Check Formatting with Black
        run: black --check .

      - name: Static Type Checking with Mypy
        run: mypy askmynotes/

  # ----------------------------------------------------------------------------
  # Job 2: Automated Unit & Integration Tests (Matrix across Python versions)
  # ----------------------------------------------------------------------------
  test:
    name: Test (Python ${{ matrix.python-version }})
    needs: [lint]  # Only run test matrix if linting and formatting pass!
    runs-on: ubuntu-latest
    timeout-minutes: 15

    strategy:
      fail-fast: false  # Don't cancel Python 3.12 if 3.11 fails; see all results
      matrix:
        python-version: ["3.11", "3.12"]

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Setup Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: "pip"

      - name: Install Package and Test Tools
        run: |
          python -m pip install --upgrade pip
          pip install -e .[test]

      - name: Execute pytest with Branch Coverage
        run: |
          pytest --cov=askmynotes \
                 --cov-report=term-missing \
                 --cov-report=xml \
                 --cov-branch \
                 --cov-fail-under=75

      - name: Upload Coverage Artifact
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report-py${{ matrix.python-version }}
          path: coverage.xml
          retention-days: 14
```

#### Line-by-Line Breakdown of `ci.yml`:
- `concurrency.group: ci-${{ github.ref }}`: Groups runs by branch/PR reference.
- `cancel-in-progress: true`: If you push commit A, and 10 seconds later push commit B, GitHub immediately terminates commit A's run, saving CI runner minutes.
- `runs-on: ubuntu-latest`: Provisions a fresh Ubuntu 22.04 LTS runner VM.
- `cache: 'pip'`: Uses SHA-256 hashes of `pyproject.toml` or `requirements.txt` to cache downloaded wheels in GitHub's distributed cache, cutting setup time from 90 seconds to 4 seconds.
- `needs: [lint]`: Defines DAG sequencing. `test` will not waste compute if basic syntax or linting is broken.
- `strategy.matrix`: Multiplies the job across Python 3.11 and 3.12 runners in parallel.
- `fail-fast: false`: Ensures both matrix jobs run to completion so you know if a bug is specific to Python 3.11 or affects all versions.
- `--cov-fail-under=75`: Enforces the quality gate. If branch coverage drops to 74.9%, pytest returns exit code 1, the step fails, the check turns red, and GitHub branch protection blocks the merge.

---

## 6. Comprehensive Command Reference for Day 33

```bash
# pytest Invocations
pytest                             # Run all tests in tests/
pytest -v                          # Verbose output (lists each test name and pass/fail)
pytest -k "chunker or loader"      # Run only tests matching substring expression
pytest -m "not slow"               # Run tests excluding those marked with @pytest.mark.slow
pytest -s                          # Disable stdout capture (show print statements)
pytest --maxfail=1                 # Stop execution immediately on first failure
pytest --pdb                       # Drop into interactive Python debugger on failure

# Coverage Commands
pytest --cov=askmynotes            # Measure line coverage for package
pytest --cov=askmynotes --cov-branch # Measure branch coverage
pytest --cov=askmynotes --cov-report=html # Generate interactive HTML report in htmlcov/
pytest --cov=askmynotes --cov-fail-under=80 # Enforce 80% coverage threshold

# GitHub CLI for Local Actions Testing
gh workflow list                   # List workflows in active repository
gh workflow run ci.yml             # Manually trigger workflow dispatch
gh run list                        # Inspect status of recent CI runs
gh run watch                       # Tail live CI log output in your terminal
```
