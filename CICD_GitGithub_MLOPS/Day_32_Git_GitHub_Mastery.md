# Day 32: Git & GitHub Mastery — Branching, Rebasing, Conflicts, and Internals

---

## Syllabus Alignment & Overview

| Topic Code | Module Title | Duration | Core Focus & Real-World Objective |
| :--- | :--- | :--- | :--- |
| **6.1** | **Branching Strategies** | 45m | Trunk-Based Development vs GitHub Flow vs GitFlow; feature branch lifecycle; deployment velocity. |
| **6.2** | **Rebasing & Cherry-Picking** | 45m | `git rebase`, interactive rebase (`-i`), linear history vs merge bubbles, `cherry-pick`, golden rule of rebasing. |
| **6.3** | **Merge Conflict Resolution** | 45m | Root cause of conflicts; conflict markers anatomy; 5-step deterministic resolution ritual; aborting safely. |
| **6.4** | **PR Etiquette & Code Review** | 30m | The <400 line rule; PR templates; constructive review rubrics; GitHub branch protection rules. |
| **6.5** | **Git Internals & Recovery** | 30m | 4 Git object types (blob, tree, commit, tag); SHA-1 hashing; HEAD and refs; `reflog` disaster recovery; `git reset` modes. |

---

## 1. Topic 6.1: Branching Strategies in Production Engineering

In Git, a **branch** is not an isolated folder or a heavy copy. It is simply a lightweight, movable 41-byte pointer file located in `.git/refs/heads/<branch-name>` containing a 40-character commit SHA.

```
       commit C1 <--- commit C2 <--- commit C3  [main]
                                         ^
                                         |
                                    [feature]
```

### 1.1 Comparison of Industry Branching Strategies

```
A. GitFlow (Legacy / Scheduled Releases)
   main --------------------------------------------* [v1.0 Release]
          \                                       /
   develop --------*---------*--------*----------*
                    \       /          \        /
   feature           *-----*            *------*

B. Trunk-Based Development (Modern High-Velocity / DevOps Standard)
   main (Trunk) -----------------------------------------------------> Continuous Deploy
                  \   /       \   /         \   /
                   *-*         *-*           *-*  (Short-lived feature branches < 1-2 days)
```

| Strategy | Structure | Pros | Cons | Best Fit |
| :--- | :--- | :--- | :--- | :--- |
| **Trunk-Based Development** | Developers branch from `main`, make small changes (<1-2 days), merge back to `main` via short-lived PRs. Continuous integration runs constantly. | Fast feedback loops, eliminates massive "merge hell", enables true continuous delivery. | Requires robust automated test suites, feature flags, and high engineering discipline. | High-growth startups, SaaS teams, modern MLOps systems. |
| **GitHub Flow** | Branch from `main`, open PR, discuss/review, deploy to staging/canary from branch, merge to `main` after verified in production. | Extremely simple, frictionless, perfect for continuous web deployments. | Not designed for multi-version parallel maintenance. | Web APIs, microservices, cloud applications. |
| **GitFlow** | Two permanent long-lived branches (`main` for releases, `develop` for integration), plus `feature/*`, `release/*`, and `hotfix/*` branches. | High control over planned release cycles with strict stabilization phases. | High overhead, complex branching topology, delayed feedback, frequent merge conflicts. | Enterprise boxed software, mobile apps with App Store review cycles, medical devices. |

---

## 2. Topic 6.2: Rebasing, Interactive Rebase & Cherry-Picking

### 2.1 Merge vs Rebase: The Fundamental Distinction

Suppose your feature branch branched from commit `B`. While you worked on commits `F1` and `F2`, teammates pushed `C` and `D` to `main`.

```
          F1 --- F2  [feature]
         /
A --- B --- C --- D  [main]
```

#### Approach 1: Merge (`git merge main`)
* Joins the two histories by creating a **3-way merge commit** (`M`) with two parents (`F2` and `D`).
* **Pros**: 100% preserves chronological topology and historical accuracy.
* **Cons**: Clutters git history with hundreds of non-informative `"Merge branch 'main' into feature"` bubbles.

#### Approach 2: Rebase (`git rebase main`)
* Finds the common ancestor (`B`), temporarily stashes `F1` and `F2`, fast-forwards your branch to `D`, and **re-applies** each feature commit onto `D` one by one, generating brand new commit SHAs (`F1'`, `F2'`).
* **Pros**: Produces a clean, pristine, linear commit history without merge bubbles.
* **Cons**: Rewrites commit hashes. If other developers are working on that exact branch, their histories will diverge.

```
A --- B --- C --- D --- F1' --- F2'  [feature]
```

> [!CAUTION]
> **The Golden Rule of Rebasing**:
> **Never rebase commits that exist outside your local repository and have been based upon by other collaborators.**
> Rebasing shared public branches (`main`, `develop`, or shared team branches) causes severe repository divergence and duplicate commits. Rebase freely on your private feature branches before opening a PR.

---

### 2.2 Interactive Rebase: Curating Your Commit History
Interactive rebase (`git rebase -i`) is the tool used to clean up messy local commits before submitting a PR.

```bash
# Interactively rebase the last 4 commits on your current branch
git rebase -i HEAD~4
```

This launches your default text editor with an instruction sheet:
```text
pick a1b2c3d feat(loader): add PDF text extractor
pick b2c3d4e fix: fix typo in regex
pick c3d4e5f fix: fix another bug in pdf parser
pick d4e5f6a test(loader): add unit tests for PDF extraction

# Commands:
# p, pick = use commit
# r, reword = use commit, but edit the commit message
# e, edit = use commit, but stop for amending
# s, squash = meld into previous commit (discard commit message or combine)
# f, fixup = like "squash", but discard this commit's log message
# d, drop = remove commit
```

#### Curating Into Clean Atomic Commits:
Change the instruction sheet to:
```text
pick a1b2c3d feat(loader): add PDF text extractor
fixup b2c3d4e fix: fix typo in regex
fixup c3d4e5f fix: fix another bug in pdf parser
pick d4e5f6a test(loader): add unit tests for PDF extraction
```
When saved and closed, Git merges the two intermediate fixups directly into `feat(loader)` without creating extra noise. The PR now contains just two clean, logical, atomic commits.

#### Pushing a Rebased Branch:
Because rebasing rewrites commit SHAs, a normal `git push` will be rejected by GitHub:
```bash
# SAFE: Only forces push if no one else has pushed to your remote branch in the meantime
git push --force-with-lease origin feature/pdf-loader

# DANGEROUS: Destroys remote history blindly (NEVER use in collaborative settings)
git push --force origin feature/pdf-loader
```

---

### 2.3 Cherry-Picking: Selective Commit Extraction
`git cherry-pick <commit-sha>` copies the diff of a specific commit from anywhere in the repository and applies it directly on top of your current branch as a new commit.

```bash
# Scenario: A critical bugfix was committed to 'develop' (sha: 9f8a12b),
# but needs to be deployed immediately to 'main' without merging develop.

# 1. Switch to production branch
git checkout main

# 2. Pull latest
git pull origin main

# 3. Apply the specific commit diff
git cherry-pick 9f8a12b

# 4. Push the hotfix
git push origin main
```

---

## 3. Topic 6.3: Merge Conflict Resolution

### 3.1 Why Conflicts Happen
Git can automatically combine changes made in different files, or even different parts of the same file. A **merge conflict** occurs *only* when two branches have modified the **exact same lines of code** differently since their common ancestor, or when one branch deleted a file that the other branch modified.

### 3.2 Anatomy of Conflict Markers
When a conflict occurs, Git halts execution and injects special markers directly into the conflicting source file:

```python
<<<<<<< HEAD
# This block is from your active checked-out branch (e.g. main)
def get_embedding_model():
  return "BAAI/bge-base-en-v1.5"


=======
# This block is from the branch being merged/rebased (e.g. feature/new-model)
def get_embedding_model():
  return "text-embedding-3-small"


>>>>>>> feature/new-model
```

### 3.3 The 5-Step Deterministic Conflict Resolution Ritual

```
[Step 1: Discover] --------> [Step 2: Inspect] --------> [Step 3: Resolve & Edit] --------> [Step 4: Stage] --------> [Step 5: Finalize]
   git status                    git diff                      Remove <<<< ==== >>>>            git add <file>           git commit / rebase --continue
```

#### Complete Command Walkthrough:
```bash
# 1. Discover: Identify which files have conflicts
git status
# Output:
# Unmerged paths:
#   (use "git add <file>..." to mark resolution)
#	both modified:   askmynotes/embedder.py

# 2. Inspect: Review the conflicting blocks
git diff askmynotes/embedder.py

# 3. Resolve: Open the file in an editor, discuss with teammate, pick the correct code,
# and DELETE the markers (<<<<<<<, =======, >>>>>>>).
# Example resolution:
# def get_embedding_model():
#     return "BAAI/bge-base-en-v1.5"

# 4. Stage: Tell Git the conflict in this file is resolved
git add askmynotes/embedder.py

# 5. Finalize:
# If in a merge:
git commit -m "merge: resolve embedding model conflict between main and feature"

# If in a rebase:
git rebase --continue
```

#### Safe Escape Hatch:
If a merge or rebase becomes too confusing or tangled, you can always revert to the exact pre-merge state:
```bash
git merge --abort    # Restores working tree to before 'git merge' was invoked
git rebase --abort   # Restores branch to before 'git rebase' was invoked
```

---

## 4. Topic 6.4: Pull Request (PR) Etiquette & Code Review

### 4.1 The Industry Standard PR Rules
1. **The <400 Line Rule**: Pull requests over 400 lines of code have a 60% lower defect-detection rate because reviewers experience cognitive fatigue. Break large features into stacked PRs.
2. **One Logical Change Per PR**: Do not mix refactoring with business logic, and do not mix formatting changes with feature code.
3. **Include Automated Tests & Verification**: Every PR that introduces code must include unit/integration tests that prove the code works.

### 4.2 Production PR Description Template (`.github/pull_request_template.md`)

```markdown
## Context & Motivation
<!-- Why is this change necessary? Link to Jira ticket or GitHub Issue -->
Closes #84. Resolves memory spike during PDF chunking on large (>100 page) documents.

## What Changed
- Replaced eager in-memory text accumulation with a chunk generator in `askmynotes/chunker.py`.
- Added unit tests for streaming chunk generation in `tests/test_chunker.py`.
- Added memory benchmark test ensuring peak RSS remains < 350MB.

## How to Test
1. Checkout this branch: `git checkout fix/chunker-memory-leak`
2. Run test suite: `pytest tests/test_chunker.py -v`
3. Run memory benchmark: `pytest tests/test_chunker.py -k test_peak_memory_usage`

## Performance & Quality Impact
- Peak RAM reduced from 1.8GB to 240MB for a 250-page PDF document.
- Unit test branch coverage maintained at 88.4%.

## Checklist
- [x] Pre-commit hooks (`ruff`, `black`, `mypy`) pass locally.
- [x] Unit and integration tests pass.
- [x] No secrets or credentials committed.
- [x] Docs updated.
```

### 4.3 Branch Protection Rules on `main`
In enterprise repositories, developers cannot push directly to `main`. Protection rules configured in GitHub repository settings enforce:
- **Require a pull request before merging**.
- **Require approvals**: At least 1 (or 2) peer review sign-offs.
- **Require status checks to pass before merging**: CI workflow (`lint`, `typecheck`, `test`) must be green.
- **Require branches to be up to date before merging**: Ensures the branch was tested against the latest commit on `main`.

---

## 5. Topic 6.5: Git Internals & Disaster Recovery

### 5.1 The Four Fundamental Git Object Types
Inside `.git/objects/`, Git stores everything as compressed, content-addressable zlib objects identified by a 40-character SHA-1 hash.

```
       +-------------------------------------------------------------+
       |                         COMMIT OBJECT                       |
       |  tree: d8329f...                                            |
       |  parent: 7a1f4b...                                          |
       |  author: Abhiram <abhiram1.chittampally@gmail.com>          |
       |  committer: Abhiram <abhiram1.chittampally@gmail.com>       |
       |  message: feat: implement vector index                      |
       +-------------------------------------------------------------+
                                      |
                                      v
       +-------------------------------------------------------------+
       |                          TREE OBJECT                        |
       |  mode: 100644  blob 5e91ab...  chunker.py                   |
       |  mode: 100644  blob 8c23cd...  eval.py                      |
       |  mode: 040000  tree fa34ef...  tests/                       |
       +-------------------------------------------------------------+
               |                       |
               v                       v
      +-----------------+     +-----------------+
      |   BLOB OBJECT   |     |   BLOB OBJECT   |
      | (Raw File Data) |     | (Raw File Data) |
      +-----------------+     +-----------------+
```

1. **Blob (Binary Large Object)**: Stores raw file content only. It does not store filenames, directory paths, or file permissions.
2. **Tree**: Represents a directory. Maps human-readable filenames and file permissions to blob hashes or sub-tree hashes.
3. **Commit**: Points to a top-level root tree hash, parent commit hash(es), author info, timestamp, and the commit message.
4. **Annotated Tag**: A permanent pointer object pointing to a commit, containing tagger metadata, date, and a signed message.

#### Low-Level Plumbing Commands:
```bash
# Inspect the type of an object by hash
git cat-file -t a1b2c3d4e5...
# Output: commit (or tree, blob, tag)

# Pretty-print the content of an object by hash
git cat-file -p a1b2c3d4e5...
```

---

### 5.2 The 90-Day Safety Net: `git reflog` & Recovery
Many developers panic when they accidentally delete a branch, perform a bad rebase, or run a hard reset. In Git, **commits are virtually never lost immediately**.

Every time `HEAD` changes location (via commit, checkout, rebase, merge, or reset), Git records the previous position in a local log called the **Reference Log (`reflog`)**. These entries persist locally for 90 days before garbage collection (`git gc`).

#### Disaster Recovery Walkthrough:
```bash
# Disaster Scenario: Developer ran git reset --hard HEAD~3 by accident,
# deleting their last 3 commits!

# 1. View the reference log of HEAD movements
git reflog
# Output:
# 3b4c1a2 (HEAD -> main) HEAD@{0}: reset: moving to HEAD~3
# 9a8b7c6 HEAD@{1}: commit: feat(pipeline): add automated eval stage
# 8f7e6d5 HEAD@{2}: commit: feat(embedder): add batch vectorization
# 7d6c5b4 HEAD@{3}: commit: feat(loader): extract pdf text
# 1a2b3c4 HEAD@{4}: checkout: moving from feature to main

# 2. Identify the commit hash right BEFORE the mistake occurred (HEAD@{1} = 9a8b7c6)

# 3. Recover the repository state instantly:
# Option A: Reset main back to that commit
git reset --hard 9a8b7c6

# Option B: Create a brand new branch pointing to the lost commit
git branch recovered-work 9a8b7c6
```

---

### 5.3 The Three Modes of `git reset`

```bash
git reset [--soft | --mixed | --hard] <target-commit>
```

| Reset Mode | Moves `HEAD` & Branch Pointer? | Modifies Staging Area (Index)? | Modifies Working Tree (Disk)? | Real-World Use Case |
| :--- | :---: | :---: | :---: | :--- |
| `--soft` | **YES** | **NO** | **NO** | "I committed too early, or want to combine the last 3 commits into 1 before pushing." All changes remain staged. |
| `--mixed` *(default)* | **YES** | **YES** | **NO** | "I want to unstage files and rethink how to group them into commits." All file changes remain safe on disk. |
| `--hard` | **YES** | **YES** | **YES** | **DESTRUCTIVE**. "Completely throw away all work done since `<target-commit>` and match target state exactly." |

---

## 6. Comprehensive Command Reference for Day 32

```bash
# Branch Operations
git branch                          # List local branches
git branch -a                       # List local and remote tracking branches
git checkout -b feature/model-eval  # Create and switch to new branch
git switch -c feature/model-eval    # Modern syntax for creating & switching branches
git branch -d feature/my-branch     # Safe delete branch (only if merged)
git branch -D feature/my-branch     # Force delete branch (even if unmerged)

# Rebase & Cherry-Pick
git rebase main                     # Replay current branch commits onto main tip
git rebase -i HEAD~3                # Interactively squash/edit last 3 commits
git rebase --continue               # Continue rebase after resolving conflict
git rebase --abort                  # Cancel rebase and restore original state
git cherry-pick <commit-sha>        # Apply a specific commit from another branch

# Recovery & Internals
git reflog                          # Display history of all HEAD movements
git reset --soft HEAD~1             # Undo last commit, keep changes staged
git reset --mixed HEAD~1            # Undo last commit, unstage changes, keep files on disk
git reset --hard HEAD~1             # Destroy last commit and discard all file changes
git cat-file -p <hash>              # Inspect contents of a git object (commit/tree/blob)
git cat-file -t <hash>              # Inspect type of a git object
```
