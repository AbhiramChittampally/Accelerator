# Day 31: Git Fundamentals & Version Control

---

## Syllabus Alignment & Overview

| Topic Code | Module Title | Duration | Core Focus & Real-World Objective |
| :--- | :--- | :--- | :--- |
| **B1** | **What is Version Control?** | 30m | Why version control exists; disaster of `code_v2_final_FINAL.py`; Centralized vs Distributed VCS. |
| **B2** | **Git vs GitHub** | 30m | Local CLI tool vs hosted collaboration platform; cryptographic identities (SSH/GPG). |
| **B3** | **The Git Workflow** | 30m | The Three Trees: Working Tree $\rightarrow$ Staging Area (Index) $\rightarrow$ Commit History; inspection (`diff`, `status`). |
| **B4** | **Repositories & Remotes** | 30m | `init`, `clone`, `remote add`, `fetch`, `merge`, `pull`, `push`; upstream tracking. |
| **B5** | **.gitignore & Commit Hygiene** | 30m | Security & artifact hygiene; Conventional Commits specification; atomic commit discipline. |

---

## 1. Topic B1: What is Version Control?

### 1.1 The Problem It Solves: The Folder of Death
Before Version Control Systems (VCS), software versioning was handled by manual copies:
```
my_project/
├── main.py
├── main_v2.py
├── main_v2_fixed.py
├── main_v2_fixed_for_real.py
├── main_v2_fixed_for_real_FINAL.py
└── main_v2_fixed_for_real_FINAL_USE_THIS.py
```

#### Why This Fails in Real Engineering Teams:
1. **Zero Attribution (Who did what?)**: If a customer reports that payment processing stopped working yesterday, manual filenames cannot tell you who changed line 42 or why.
2. **Zero Concurrency (Collaborative Overwrite)**: If Engineer A edits `main_v2.py` while Engineer B is adding a database model to `main_v2.py`, whichever engineer saves last silently destroys the other engineer's work.
3. **No Reversibility**: If a bug crashes production at 2:00 AM, there is no single command to restore the exact state of the system from 1:59 AM.
4. **No Delta History (Diffs)**: You cannot see what lines changed between two releases without tedious external diff comparisons.

### 1.2 Centralized vs Distributed VCS
* **Centralized VCS (SVN, Perforce, CVS)**:
  * A single central server hosts the repository history.
  * Developers check out only a working snapshot.
  * *Single Point of Failure*: If the server is offline or network fails, you cannot commit, view diffs, or inspect logs.
* **Distributed VCS (Git, Mercurial)**:
  * Every developer who clones the repository gets a **complete mirror** of the entire project history, including all commits, branches, and tags.
  * All common operations (`git add`, `git commit`, `git log`, `git diff`, `git branch`) execute entirely locally in milliseconds without network access.
  * Network connection is required *only* to synchronize changes (`git push`, `git fetch`, `git pull`).

---

## 2. Topic B2: Git vs GitHub

| Dimension | Git | GitHub |
| :--- | :--- | :--- |
| **Nature** | Local CLI program and core content-tracking engine. | Cloud-hosted platform built on top of Git. |
| **Created By** | Linus Torvalds (2005) for Linux kernel development. | Chris Wanstrath, P. J. Hyett, Tom Preston-Werner (2008), acquired by Microsoft (2018). |
| **Location** | Runs on your local laptop, desktop, server, or container. | Runs on cloud infrastructure (`github.com` or GitHub Enterprise). |
| **Core Functions** | Tracking files, creating commits, branching, merging, rebasing. | Hosting remote repos, Pull Requests (PRs), code reviews, Issues, GitHub Actions (CI/CD), Discussions. |
| **Network** | Operates 100% offline for 95% of commands. | Requires network access to interact with the web interface and remote APIs. |

### Real-World Analogy:
- **Git** is the **filesystem audio recording software** (Audacity or GarageBand) installed on your computer. You record tracks, edit layers, and slice audio offline.
- **GitHub** is **Spotify or SoundCloud**. It is the cloud platform where you upload the mastered track for the world to review, listen to, fork, and comment on.

---

## 3. Topic B3: The Core Git Workflow (The Three Trees)

Git organizes files across three physical and logical stages:

```
+-------------------+        git add          +--------------------+        git commit       +--------------------+
|   Working Tree    | ----------------------> |    Staging Area    | ----------------------> |     Repository     |
| (Sandbox on disk) |                         |      (Index)       |                         |    (.git/ folder)  |
+-------------------+ <---------------------- +--------------------+ <---------------------- +--------------------+
                        git restore --staged                          git reset / checkout
```

1. **Working Tree (Working Directory)**:
   - The actual files and directories on your hard drive that you edit in VS Code, PyCharm, or Neovim.
2. **Staging Area (The Index)**:
   - A binary cache (`.git/index`) that prepares the next snapshot. Staging allows you to curate exactly what goes into the commit. If you edited 5 files, but only 2 belong to a single logical fix, you stage only those 2.
3. **Repository (Local Git Directory, `.git/`)**:
   - The permanent storage of compressed, immutable snapshot objects (`blobs`, `trees`, `commits`) identified by cryptographic SHA hashes.

### 3.1 Hands-on Workflow Walkthrough with Line-by-Line Code

#### Simple Example: First Commit from Scratch
```bash
# 1. Initialize a new git repository in the current directory
git init
# Output: Initialized empty Git repository in /home/user/project/.git/

# 2. Configure identity (stored in ~/.gitconfig or .git/config)
git config user.name "Abhiram Chittampally"
git config user.email "abhiram1.chittampally@gmail.com"

# 3. Create a python source file
echo "print('Hello, MLOps')" > app.py

# 4. Check the status of the working tree
git status
# Output:
# Untracked files:
#   (use "git add <file>..." to include in what will be committed)
#	app.py

# 5. Move app.py from Working Tree to Staging Area (Index)
git add app.py

# 6. Verify that app.py is staged
git status
# Output:
# Changes to be committed:
#   (use "git restore --staged <file>..." to unstage)
#	new file:   app.py

# 7. Commit the snapshot to the local repository (.git)
git commit -m "feat: initial commit with app entrypoint"
# Output:
# [main (root-commit) 7a1f4b2] feat: initial commit with app entrypoint
#  1 file changed, 1 insertion(+)
#  create mode 100644 app.py
```

#### Line-by-Line Code Breakdown:
- `git init`: Creates a hidden `.git` folder containing `objects/`, `refs/`, `HEAD`, `config`, and hooks. Without this, Git does not track anything.
- `git config user.name "..."`: Embeds author metadata into every subsequent commit. Crucial for blame and audit logs.
- `echo "..." > app.py`: Standard shell command creating a file in your working directory. Git does not track it until staged.
- `git add app.py`: Hashes the file contents using SHA-1, creates a compressed blob object in `.git/objects/`, and records the file mode and path in `.git/index`.
- `git commit -m "..."`: Creates a `tree` object pointing to the blobs, creates a `commit` object pointing to the tree, author, timestamp, commit message, and parent commit (none for root), and points `refs/heads/main` to this new commit hash.

---

## 4. Topic B4: Repositories & Remotes

A **remote** is a version of your project hosted on the internet or network (e.g., GitHub, GitLab, AWS CodeCommit).

### 4.1 Remote Management Commands
```bash
# Check existing remotes with verbose URLs
git remote -v

# Link your local repo to a remote GitHub repository
git remote add origin https://github.com/abhiram/askmynotes.git

# Rename branch to 'main' if defaulted to 'master'
git branch -M main

# Push and establish upstream tracking (-u sets upstream)
git push -u origin main
```

### 4.2 Fetch vs Pull vs Merge
* `git fetch origin`: Connects to GitHub, downloads all new commits, branches, and tags from remote into your `.git` folder, and updates remote tracking branches like `origin/main`. **It touches ZERO files in your working directory.**
* `git merge origin/main`: Merges the downloaded remote commits into your active local checked-out branch.
* `git pull origin main`: Convenience command that executes `git fetch` followed immediately by `git merge FETCH_HEAD`.

```
                    git fetch origin
Remote Repo (GitHub) ------------------> origin/main (Remote-Tracking Branch in .git)
                                                |
                                                | git merge origin/main
                                                v
                                         main (Your Local Checked-Out Working Branch)
```

> [!WARNING]
> Blindly running `git pull` can introduce unintended merge commits or surprise merge conflicts. Senior engineers frequently run `git fetch origin` first, inspect changes with `git log HEAD..origin/main --oneline`, and then merge or rebase cleanly.

---

## 5. Topic B5: .gitignore & Commit Hygiene

### 5.1 What Must NEVER Be Committed
1. **Secrets & Credentials**: API keys (`OPENAI_API_KEY`, `AWS_SECRET_ACCESS_KEY`), `.env` files, SSH private keys, TLS certs.
2. **Virtual Environments**: `.venv/`, `env/`, `venv/` (contains thousands of duplicate binary files specific to one OS).
3. **Build Artifacts & Caches**: `__pycache__/`, `*.pyc`, `dist/`, `build/`, `.eggs/`, `*.so`.
4. **OS Metadata**: `.DS_Store` (macOS), `Thumbs.db` (Windows).
5. **Large Datasets**: Multi-megabyte or gigabyte files (`data/*.csv`, `data/*.parquet`, `*.tar.gz`, `*.bin`). Use **DVC** for these instead.

### 5.2 Production Boilerplate `.gitignore` for Python & MLOps

```gitignore
# ==============================================================================
# PRODUCTION .gitignore for Python MLOps & Data Science
# ==============================================================================

# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class
*.so

# C extensions & build directories
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environments
.venv/
venv/
ENV/
env/
env.bak/
venv.bak/

# Environment Variables & Secrets (CRITICAL)
.env
.env.*
!.env.example
secrets.yaml
credentials.json
*.pem
*.key

# IDEs and Editors
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store
Thumbs.db

# Testing & Coverage
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
htmlcov/

# Jupyter Notebooks checkpoints
.ipynb_checkpoints
*/.ipynb_checkpoints/*

# DVC (Data Version Control) Local Cache
.dvc/cache
.dvc/tmp

# Large raw datasets and local model binaries
# (Track pointer files *.dvc in git, exclude actual blobs)
data/raw/*
data/processed/*
models/*.pkl
models/*.pt
models/*.onnx
models/*.bin
!data/raw/.gitkeep
!data/processed/.gitkeep
```

---

## 6. Commit Hygiene & The Conventional Commits Specification

### 6.1 The Anatomy of an Atomic Commit
An **atomic commit** does one single logical thing and leaves the repository in a working, passing state.
- **Anti-pattern**: A single commit named `"fixed bug and added model training and cleaned css and updated readme"`. If the model training has a memory leak, you cannot revert it without reverting your bug fix and docs!
- **Best Practice**: Split into 4 atomic commits:
  1. `fix(retrieval): prevent IndexError on empty candidate list`
  2. `feat(model): add BAAI/bge-base-en-v1.5 embedding support`
  3. `style(ui): align search bar container margin`
  4. `docs(readme): add environment setup instructions`

### 6.2 Conventional Commits Format
```
<type>(<optional scope>): <description>

[optional body]

[optional footer(s)]
```

#### Standard Commit Types:
- `feat`: A new user-facing or system feature.
- `fix`: A bug fix.
- `docs`: Documentation-only changes.
- `style`: Changes that do not affect code logic (whitespace, formatting, missing semicolons).
- `refactor`: Code change that neither fixes a bug nor adds a feature.
- `perf`: Code change that improves performance.
- `test`: Adding missing tests or correcting existing tests.
- `build`: Changes affecting build system or external dependencies (`pyproject.toml`, Docker).
- `ci`: Changes to CI configuration files and scripts (`.github/workflows/*.yml`).
- `chore`: Routine housekeeping tasks (`.gitignore` update, dependency bump).

#### Real-World High-Quality Commit Example:
```
feat(eval): add Mean Reciprocal Rank (MRR) metric calculation

Implement compute_mrr_at_k function inside askmynotes.eval to score
candidate chunks against golden question sets. Evaluated across k=[1, 5, 10].

Closes #142
```

---

## 7. Comprehensive Command Reference for Day 31

```bash
# Setup & Configuration
git config --global user.name "Your Name"
git config --global user.email "you@domain.com"
git config --global init.defaultBranch main

# Repo Creation
git init                           # Initialize current dir as git repository
git clone <url>                    # Download remote repo with full history

# Status & Staging
git status                         # View working tree and staging area state
git diff                           # View unstaged changes (working tree vs index)
git diff --staged                  # View staged changes (index vs HEAD commit)
git add <file>                     # Stage specific file
git add .                          # Stage all tracked & untracked changes
git restore <file>                 # Discard working tree changes (uncommitted edits)
git restore --staged <file>        # Unstage file (moves from index back to working tree)

# Committing & History
git commit -m "feat: message"      # Commit staged changes
git commit -am "fix: message"      # Stage tracked modified files and commit in 1 step
git log --oneline --graph --all    # Beautiful ASCII graph of all commits and branches
git log -n 5                       # View last 5 commits with full author and diff data

# Remotes
git remote add origin <url>        # Register remote URL under name 'origin'
git remote -v                      # Inspect configured remotes
git fetch origin                   # Download new objects and refs from remote
git pull origin main               # Fetch and merge origin/main into current branch
git push -u origin main            # Push commits and configure default upstream tracking
```
