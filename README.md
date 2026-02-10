# repokit

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/CBS-HPC/repokit/actions/workflows/ci.yml/badge.svg)](https://github.com/CBS-HPC/repokit/actions/workflows/ci.yml)

Core utilities for the **Research Template** setup flow. `repokit` provides reusable setup helpers, CLI tools, and automation used by the cookiecutter template. It composes smaller, independent packages:

- **repokit-common**: shared utilities (env, prompts, paths, config helpers)
- **repokit-backup**: rclone-based backup tooling
- **repokit-dmp**: data management plan (DMP) tooling

## Highlights

- Setup automation for research projects
- CLI helpers for CI, dependencies, templates, repos, and README generation
- Integrates with `repokit-backup` and `repokit-dmp`

## Installation

From source:

```bash
git clone https://github.com/CBS-HPC/repokit.git
cd repokit
pip install -e .
```

If you cloned with submodules:

```bash
git submodule update --init --recursive
```

## CLI (selected)

```bash
ci-control --on
update-readme
update-dependencies
backup --help
set-dataset --help
dmp-update
```

## Development

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
pytest
ruff check .
```

## License

MIT

### <a id="online-installation"></a>
<details>
<summary><strong>📦 Online (with Git)</strong></summary><br>

Use this option if Git is installed and you want to fetch the template directly from GitHub:

```bash
cookiecutter gh:CBS-HPC/research-template
```

---
</details>

### <a id="offline-installation"></a>
<details>
<summary><strong>📁 Offline (Local Installation)</strong></summary><br>

If Git is **not installed**, you can still use the template by downloading it manually:

1. Go to [https://github.com/CBS-HPC/research-template](https://github.com/CBS-HPC/research-template)  
2. Click the green **“Code”** button, then choose **“Download ZIP”**  
3. Extract the ZIP file to a folder of your choice  
4. Run Cookiecutter locally:

```bash
cookiecutter path/to/research-template
```

> ⚠️ Do **not** use `git clone` if Git is not installed. Manual download is required in this case.

---
</details>

### 🧩 Interactive Project Configuration

This template guides you through a series of interactive prompts to configure your project:

### <a id="project-metadata"></a>
<details>
<summary><strong>📦 Project Metadata</strong></summary><br>

Provide essential project metadata to support clear documentation, proper attribution, and machine-readable citations.

These details help define your project's identity and improve visibility in collaborative and academic contexts.

```
├── project_name              → Human-readable name
├── repo_name                 → Folder and repository name
├── description               → Short summary of the project
├── author_name               → Your full name
├── email                     → Your email
├── orcid                     → Your ORCID researcher ID
├── version                   → Initial version number (e.g., 0.0.1)
```

This information is used to auto-generate:

- `README.md` – populated with title, description, and author info  
- `CITATION.cff` – for machine-readable academic citation
- `dmp.json` – for machine-actionable data management plan (maDMP).

---
</details>

### <a id="license"></a>
<details>
<summary><strong>🔑 License</strong></summary><br>

Clear licensing is essential for open and reproducible research. It defines how others can use, share, and build on your work—whether it's code, data, or documentation.

```
├── code_license              → [MIT | BSD-3-Clause | Apache-2.0 | None]
├── documentation_license     → [CC-BY-4.0 | CC0-1.0 | None]
├── data_license              → [CC-BY-4.0 | CC0-1.0 | None]
```

This information is used to auto-generate:

- `LICENSE.txt` – includes license sections for code, documentation, and data.
- `dmp.json` – sets the default licensing for dataset added to the for machine-actionable data management plan (maDMP).  

> ℹ️ If “None” is selected, the corresponding section will be omitted from the LICENSE file.

**Code Licenses:**

- [**MIT**](https://opensource.org/licenses/MIT) – Very permissive, short license. Allows reuse with attribution.  
- [**BSD-3-Clause**](https://opensource.org/license/bsd-3-clause/) – Permissive, but includes a non-endorsement clause.  
- [**Apache-2.0**](https://www.apache.org/licenses/LICENSE-2.0) – Like MIT, but includes explicit patent protection.  

**Documentation Licenses:**

- [**CC-BY-4.0**](https://creativecommons.org/licenses/by/4.0/) – Requires attribution, allows commercial and derivative use.  
- [**CC0-1.0**](https://creativecommons.org/publicdomain/zero/1.0/) – Places documentation in the public domain (no attribution required).

**Data Licenses:**

- [**CC-BY-4.0**](https://creativecommons.org/licenses/by/4.0/) – Allows reuse and redistribution with attribution.  
- [**CC0-1.0**](https://creativecommons.org/publicdomain/zero/1.0/) – Public domain dedication for unrestricted reuse.

---
</details>

### <a id="language-environment"></a>
<details>
<summary><strong>🧬 Language & Environment</strong></summary><br>

Define the core programming language and set up an isolated environment to ensure your analysis is reproducible across systems and collaborators.

#### ⚙️ Programming Language
Choose your primary scripting language. The template supports multi-language projects and automatically generates a modular codebase tailored to your selection.

```
├── programming_language      → [Python | R | Stata | Matlab | None]
│   └── If R/Stata/Matlab selected:
│       └── Prompt for executable path if not auto-detected
```

📝 Based on your selected language, the template will automatically generate example scripts and notebooks for each stage of the workflow — see [How it works](#-how-it-works) for details.

#### 🧪 Environment Configuration

To ensure reproducibility in computational research, it’s essential to isolate your project’s software dependencies.

Virtual environments allow you to lock in specific package versions and avoid conflicts with system-wide tools or other projects. This makes it possible for collaborators—and future you—to re-run analyses under the exact same conditions.

Set up isolated virtual environments using **Conda**, **UV (venv backend)**, or **system installation**.

```
├── Python environment
│   └── env_manager_python        → [Conda | UV]
│       ├── If Conda :             → Prompts for Python version
│       ├── If UV (venv backend): → Uses current Python kernel version
│                                 → Creates a `.venv` directory for the environment
│                                 → Initializes a UV project and generates `uv.lock` to capture dependencies
├── R environment (if R used)
│   └── env_manager_r             → [Conda | System R]
│       ├── If Conda:             → Prompts for R version
│       └── If System R:          → Searches system PATH for installed R
│                                 → Prompts for path if not found
│       → In all cases:           → Initializes an isolated R environment using `renv` in the `/R` directory
│                                 → Generates `renv.lock` to capture R package versions
├── Proprietary software (if selected)
│   └── [Stata | Matlab]
│       ├── Searches system PATH for installed application
│       └── Prompts user for executable path if not found
```

**Environment manager options:**
- [**Conda (Miniforge)**](https://github.com/conda-forge/miniforge) – A community-maintained minimal Conda distribution from conda-forge, preconfigured to use the conda-forge channel for consistent, reproducible, cross-platform environments (for both Python and R).
- [**UV**](https://github.com/astral-sh/uv) – A fast, modern Python package manager and `venv` backend. Provides isolated environments and accelerated dependency resolution. Ideal for Python-only workflows.  
- [**renv**](https://rstudio.github.io/renv/) – An R package for creating isolated, project-local environments. Captures exact package versions in a `renv.lock` file, enabling reproducibility similar to `requirements.txt` or `environment.yml`.

Regardless of your choice, the following files are generated to document your environment:

- `environment.yml` – Conda-compatible list of dependencies  
- `requirements.txt` – pip-compatible Python package list  
- `renv.lock` – (if R is selected) snapshot of R packages using the `renv` package
- `uv.lock` – (if Venv is selected) snapshot of python packages using the `uv` package manager  

⚠️ When using **UV** or **Pre-Installed R**, the `environment.yml` file is created **without Conda's native environment tracking**. As a result, it may be **less accurate or reproducible** than environments created with Conda.

⚠️ If proprietary software (e.g., Stata, Matlab) is selected, the system will first **search your PATH**. If not found, you’ll be prompted to manually enter the executable path.  

💡 Conda (miniforge) will be downloaded and installed automatically if it's not already available.

---
</details>

### <a id="version-control"></a>
<details>
<summary><strong>🗃️ Version Control</strong></summary><br>

Version control is a cornerstone of reproducible research.It enables you to track changes to your code, data, and analysis pipelines over time—ensuring transparency, accountability, and collaboration.

Choose a system to version your code (and optionally your data).

```
├── version_control           → [Git | Datalad | DVC | None]
│   ├── Git:
│   │   ├── Prompt for Git user.name and user.email
│   │   ├── Initializes Git repo in project root
│   │   └── Initializes separate Git repo in `data/`
│   ├── Datalad:
│   │   ├── Initializes Git repo (if not already)
│   │   └── Initializes a Datalad dataset in `data/` (nested Git repo)
│   └── DVC:
│       ├── Initializes Git repo (if not already)
│       ├── Runs `dvc init` to create a DVC project
│       └── Configures `data/` as a DVC-tracked directory
```

This template supports several version control systems to suit different workflows:

- [**Git**](https://git-scm.com/) – general-purpose version control for code and text files  
- [**Datalad**](https://www.datalad.org/) – for data-heavy, file-based versioning; designed to support **FAIR** principles and **Open Science** workflows  
- [**DVC**](https://dvc.org/) – for machine learning pipelines, dataset tracking, and model versioning

#### 🔧 How it works:

- **Git**: initializes the project root as a Git repository  
  - Also creates a separate Git repo in `data/` to track datasets independently  
- **Datalad**: builds on Git by creating a [Datalad dataset](https://handbook.datalad.org/en/latest/basics/101-137-datasets.html) in `data/`  
- **DVC**: runs `dvc init` and sets up `data/` as a [DVC-tracked directory](https://dvc.org/doc/start/data-management) using external storage and `.dvc` files

#### 📝 Auto-generated `.gitignore` includes:

```
├── data/                  → 00_raw, 01_interim and 02_processed data folders
├── bin/                   → local binaries (e.g., rclone)
├── env/, __pycache__/     → Python virtual environments and caches
├── .vscode/, .idea/       → IDE and editor configs
├── .DS_Store, *.swp       → OS/system-generated files
├── .ipynb_checkpoints/    → Jupyter notebook checkpoints
├── .coverage, *.log       → logs, test coverage reports
```

> 🧹 These defaults help keep your repository clean, portable, and reproducible.

> ⚙️ If **Git**, **Datalad**, or **DVC** (or their dependencies) are not detected, the template will automatically download and install them during setup.
> This ensures you can use advanced version control tools without manual pre-installation.

---
</details>

### <a id="remote-repo-setup"></a>
<details>
<summary><strong>📡 Remote Repository Setup</strong></summary><br>

Publishing your project to a remote Git hosting platform is a key step toward transparent, collaborative, and **reproducible** research.

A remote repository provides versioned backups, collaboration support, and integration with tools like CI pipelines—crucial for reproducible and FAIR research.

Automatically create and push to a Git repository on a remote hosting platform.

```
├── remote_repo               → [GitHub | GitLab | Codeberg | None]
│   └── If selected:
│       ├── Prompt for username
│       ├── Choose visibility: [private | public]
│       └── Provide personal access token (stored in `.env`)
```

Supported platforms include:

- [**GitHub**](https://github.com) – the most widely used platform for open source and academic collaboration. Supports seamless repo creation, authentication, and automation.
- [**GitLab**](https://gitlab.com) – a DevOps platform that supports both self-hosted and cloud-hosted repositories. Ideal for collaborative development with built-in CI/CD pipelines.
- [**Codeberg**](https://codeberg.org) – a privacy-focused Git hosting service powered by [Gitea](https://about.gitea.com). Community-driven and compliant with European data governance standards.

Repositories are created using the **HTTPS API**, and authenticated with [**personal access tokens**](#-personal-access-tokens-and-permissions).

> 🛡️ Your credentials and tokens are securely stored in the `.env` file and never exposed in plain text.

#### 🔐 Personal Access Tokens and Permissions

A Personal Access Token (PAT) is needed to:

- Create remote repositories
- Push CI configuration files
- Enable automated workflows (e.g. GitHub Actions, GitLab CI)

##### 🔎 Required Token Scopes by Platform

| Platform   | Purpose                              | Required Scopes           |
|------------|--------------------------------------|---------------------------|
| **GitHub** | Create repos, push code, configure CI workflows | `repo`, `workflow`       |
| **GitLab** | Create repos, push code, configure CI/CD        | `api`                    |
| **Codeberg** | Create repo (CI enabled manually)  | `repo` *(if using API)*   |

---
</details>

## 🧾 How It Works: Structure & Scripts

This template generates a standardized, reproducible project layout. It separates raw data, code, documentation, setup scripts, and outputs to support collaboration, transparency, and automation.

### <a id="project-activation"></a>
<details>
<summary><strong>🚀 Project Activation</strong></summary><br>

To configure the project's environment—including project paths, environment variables, and virtual environments—run the activation script for your operating system. These scripts read settings from the `.env` file.

#### 🪟 Windows (PowerShell)

```powershell
#Activate
./activate.ps1

#Deactivate
./deactivate.ps1
```

#### 🐧 macOS / Linux (bash)

```bash
#Activate
source activate.sh

#Deactivate
source deactivate.sh
```

---
</details>

### <a id="repokit-deps-update"></a>
<details>
<summary><strong>📦 <code>repokit deps-update</code></strong></summary>

The `repokit deps-update` command scans your project for imported packages and updates your dependency files (`requirements.txt`, `environment.yml`, and `uv.lock`) accordingly. It supports **Python**, **R**, **MATLAB**, and **Stata**, using language-specific tooling to track packages across `./src/` (or `./R/`, `./stata/do/`).

This command is useful for keeping your project environment reproducible and ensuring that all scripts and notebooks reference installable dependencies.

#### 🔧 Usage

```bash
repokit deps-update
```

#### ✅ What it does:

- 📄 Regenerates `requirements.txt` using `pip freeze`
- 📦 Ensures missing packages are added to `uv.lock` (if used)
- 🧪 Scans the `./src/` (or `./R/`, `./stata/do/`) directories for imports and writes dependency lists:
  - `./src/dependencies.txt` (or `R/`, `stata/`)
- 📑 Updates and tags `environment.yml` and `requirements.txt` with platform-specific selectors (via `platform_rules`)
- 🧠 Runs `renv` for R, or language-specific setup scripts for MATLAB and Stata

> 🛠 The command adapts to your selected programming language as defined in `.cookiecutter`  
> 🔍 Paths and rules are derived from the `pyproject.toml` and `platform_rules.json` config

#### Example output:

```bash
📄 requirements.txt has been created successfully.
✅ Conda environment file created: environment.yml
✅ requirements.txt updated with platform tags
✅ Updated environment.yml with Conda-style platform tags
```
---
</details>

### <a id="repokit-readme-update"></a>
<details>
<summary><strong>📝 <code>repokit readme-update</code></strong></summary>

The `repokit readme-update` command regenerates your `README.md` with up-to-date project information, including:

- ✅ Code metadata and environment details
- 📁 Project folder structure as a tree diagram
- 📦 Software dependencies (from `dependencies.txt`)
- 📑 Auto-generated descriptions for core files and scripts

This helps maintain a professional and standardized `README.md` that aligns with reproducibility and publication requirements (e.g., DCAS).

#### 🔧 Usage

```bash
repokit readme-update
```

#### ✅ What it does:

- Reads the selected programming language from `.cookiecutter`
- Parses existing files and structure to infer documentation
- Updates or inserts:
  - Code dependency section (`code_dependencies` fenced block)
  - File descriptions from `file_descriptions.json`
  - Directory structure (`tree` block in README)
- Regenerates the `README.md` with consistent formatting
- Automatically creates `README.md` if it doesn’t exist

> 🧠 File and folder annotations are pulled from `file_descriptions.json`  
> 🗂️ Files ignored by `.treeignore` or `pyproject.toml → treeignore.patterns` are excluded from the directory tree

---
</details>

### <a id="repokit-examples-code"></a>
<details>
<summary><strong>💡 <code>repokit examples-code</code></strong></summary>

The `repokit examples-code` command generates realistic starter scripts and notebooks for your selected programming language using predefined Jinja2 templates.

This is useful for quickly bootstrapping a project with well-structured, language-appropriate examples for each analysis stage.

#### 🔧 Usage

```bash
repokit examples-code
```

#### ✅ What it does:

- Detects your project language from `.cookiecutter`
- Renders realistic example scripts for:
  - `s00_main.*` – pipeline entry point
  - `s01_install_dependencies.*` – dependency setup
  - `s02_utils.*` – helper functions
  - `s03_data_collection.*` to `s06_visualization.*` – typical data workflow stages
- Saves outputs in the appropriate `./src/`, `R/`, `stata/do/`, etc.
- Calls:
  - `get_dependencies` to update `dependencies.txt`
  - `repokit readme-update` to regenerate project metadata

> 🧠 Uses templates from: `./setup/repokit/temples/j2/example`  
> 🗂️ Script locations depend on your selected programming language  
> ⚠️ Existing files will be **overwritten** if they share the same name

---
</details>

### <a id="repokit-templates-reset"></a>
<details>
<summary><strong>🧱 <code>repokit templates-reset</code></strong></summary>

The `repokit templates-reset` command regenerates all core analysis and test scripts using predefined Jinja2 templates. It ensures a consistent structure and coding pattern across different scripting languages.

This command is useful for initializing or resetting project scripts to their default structure.

#### 🔧 Usage

```bash
repokit templates-reset
```

#### ✅ What it does:

- Automatically detects your selected programming language from `.cookiecutter`
- Regenerates standard source scripts:
  - `s00_main.*` – orchestrates the pipeline
  - `s01_install_dependencies.*` – handles package installation
  - `s02_utils.*` – shared utilities
  - `s03_data_collection.*` to `s06_visualization.*` – core analysis stages
  - `get_dependencies.*` – collects project dependencies
- Generates:
  - `s00_workflow.*` – interactive notebook (.ipynb or .Rmd)
  - `test_*.*` – unit test scaffolds for each script

#### 📁 Output Paths

- Scripts are placed in:
  - `./src/`, `./R/`, `./stata/do/`, or equivalent source directory
- Test templates are placed in:
  - `./tests/`, `./tests/testthat/`, etc., depending on language

> 🧩 Uses Jinja2 templates stored in `./setup/repokit/temples/j2/code`  
> 🔄 Existing scripts with the same name may be overwritten!

---
</details>

### <a id="repokit-git-config"></a>
<details>
<summary><strong>🌐 <code>repokit git-config</code></strong></summary>

The `repokit git-config` command sets up your version control system and configures a remote Git repository on **GitHub**, **GitLab**, or **Codeberg** based on environment settings.

This command streamlines the process of remote repo creation, authentication, Git setup, and CI pipeline configuration.

#### 🔧 Usage

```bash
repokit git-config
```

#### ✅ What it does:

- Reads repository settings from `.cookiecutter` and environment variables:
  - `REPO_NAME`, `CODE_REPO`, `VERSION_CONTROL`, `PROJECT_DESCRIPTION`
- Configures Git remotes using platform APIs:
  - [GitHub REST API](https://docs.github.com/en/rest)
  - [GitLab API](https://docs.gitlab.com/ee/api/)
  - [Codeberg API](https://docs.gitea.io/en-us/)
- Authenticates using personal access tokens (`GITHUB_TOKEN`, `GITLAB_TOKEN`, etc.)
- Initializes remote repositories and sets the correct `origin` URL
- Pushes the local repo to the remote and sets the tracking branch
- Automatically sets up CI configuration via `ci_config()`

#### 🔐 Supports:

- `GitHub` (requires `gh` CLI or PAT)
- `GitLab` (installs and uses `glab` CLI or token)
- `Codeberg` (via Gitea API + token)

> 🧪 Remote login and repo creation are tested via platform-specific APIs  
> 📁 Pushes both root repo and data repo (if applicable)  
> 🧰 Can auto-install `gh` or `glab` if not found locally

---
</details>

### <a id="repokit-ci-control"></a>
<details>
<summary><strong>⚙️ <code>repokit ci-control</code></strong></summary>

The `repokit ci-control` command lets you enable or disable Continuous Integration (CI) for your project, and generates default CI configurations for your selected language and Git platform (GitHub, GitLab, or Codeberg).

This tool is helpful for bootstrapping or adjusting your CI setup without manually editing `.yml` files.

#### 🔧 Usage

```bash
repokit ci-control --on     # Enable CI
repokit ci-control --off    # Disable CI
```

> You must specify one flag: `--on` or `--off`.  
> This command is safe to run multiple times and won't overwrite existing CI files.

#### ✅ What it does:

- Automatically generates CI config based on:
  - Programming language (from `.cookiecutter`)
  - Git hosting service (`CODE_REPO`)
- Supports:
  - `.github/workflows/ci.yml` for GitHub
  - `.gitlab-ci.yml` for GitLab
  - `.woodpecker.yml` for Codeberg
- Adds a `git commit-skip` alias for bypassing CI on minor commits:
  ```bash
  git commit-skip "Update docs"
  ```
- Enables/disables CI by renaming files:
  - `ci.yml.disabled ↔ ci.yml`  
  - `.gitlab-ci.yml.disabled ↔ .gitlab-ci.yml`  
  - `.woodpecker.yml.disabled ↔ .woodpecker.yml`

#### 📁 Notes

- Will auto-install CI templates from `./repokit/temples/j2/ci/`  
- Only runs if a valid `CODE_REPO` is set  
- CI files can be removed manually using `remove_ci_configs()` in code

---
</details>

### <a id="repokit-lint"></a>
<details>
<summary><strong>🧹 <code>repokit lint</code></strong></summary><br>

`repokit lint` runs project linting in a **language-aware** way. It looks for scaffolded scripts and executes them **if present**:

- **Python** → `src/linting.py` → **Ruff** (formatter + linter) and **Mypy** (type checker)
- **R** → `R/linting.R` → **lintr::lint_dir()** (auto-activates `renv` if `R/renv/activate.R` exists)
- **MATLAB** → `src/linting.m` → **checkcode** (static analysis)

### Usage

```bash
# Run all present languages
repokit lint
```

### Requirements
- Python: `ruff`, `mypy`
- R: `lintr` in your project’s `renv` (if used)
- MATLAB: `matlab` CLI on `PATH`

> The Python and MATLAB scripts live under `src/`, the R script under `R/`.

> CI YAML: implement a dedicated lint job/stage

---
</details>

### <a id="config-files"></a>
<details>
<summary><strong>🗂️ Configuration Files (Root-Level)</strong></summary><br>

The following configuration files are intentionally placed at the root of the repository. These are used by various tools for environment setup, dependency management, templating, and reproducibility.

| File              | Purpose                                                                                          |
|-------------------|--------------------------------------------------------------------------------------------------|
| `pyproject.toml`  | Project metadata for packaging, CLI tools, sync rules, platform logic, and documentation         |
| `.env`            | Defines environment-specific variables (e.g., paths, secrets). Typically excluded from version control. |
| `dmp.json`            |for machine-actionable data management plan (maDMP). |
| `.gitignore`      | Excludes unnecessary files from Git version control                                              |
| `environment.yml` | Conda environment definition for Python/R, including packages and versions                       |
| `requirements.txt`| Pip-based Python dependencies for lightweight environments                                       |
| `renv.lock`       | Records the exact versions of R packages used in the project                                    |
| `uv.lock`         | Locked Python dependencies file for reproducible installs with `uv`                            |

#### 📄 `pyproject.toml` Sections Explained

| Section                   | Purpose                                                                                      |
|---------------------------|----------------------------------------------------------------------------------------------|
| `[project]`               | Declares the base project metadata for Python tooling (name, version, dependencies, etc.).   |
| `[tool.uv]`               | Placeholder for settings related to the uv package manager (currently unused).               |
| `[tool.cookiecutter]`     | Stores project template metadata (e.g., author, licenses, language) for reproducibility and scaffolding. |
| `[tool.rcloneignore]`     | Defines file patterns to ignore when syncing with remote tools like Rclone.                  |
| `[tool.treeignore]`       | Specifies which files and folders to exclude from directory tree visualizations.             |
| `[tool.platform_rules]`   | Maps Python packages to operating systems for conditional installations.                     |
| `[tool.file_descriptions]`| Contains descriptions of files and directories for automation, UI labels, and documentation. |

---
</details>

### <a id="script-templates"></a>
<details>
<summary><strong>🛠️ Script Templates</strong></summary><br>

This template helps you organize your scripts in a standardized way across programming languages—making it easier to rerun analyses, share with collaborators, and automate complex workflows over time.

Script generation is **language-agnostic**: based on your selected language, the template will create files with the appropriate extensions:

- `.py` (scripts) and `.ipynb` (notebooks) for Python
- `.R` (scripts) and `.Rmd` (notebooks) for R
- `.m`(scripts) and `.mlx` (notebooks) for Matlab 
- `.do` (scripts) and `.ipynb` (notebooks) for Stata


These starter scripts are placed in the `./src/` directory and include:

```
├── s00_main.*                  → orchestrates the full pipeline
├── s00_workflow.*              → notebook (.ipynb, .Rmd, .mlx) orchestrating the full pipeline
├── s01_install_dependencies.*  → installs any missing packages required for the project
├── s02_utils.*                 → shared helper functions (not directly executable)
├── s03_data_collection.*       → imports or generates raw data
├── s04_preprocessing.*         → cleans and transforms data
├── s05_modeling.*              → fits models and generates outputs
├── s06_visualization.*         → creates plots and summaries
├── get_dependencies.*          → retrieves and checks required dependencies for the project environment. (Utilised)

```

Each script is structured to:

- Define a `main()` function or logical entry point (where applicable)  
- Automatically resolve project folder paths (`data/00_raw/`, `results/figures/`, etc.)  
- Remain passive unless directly called or imported  
- Support reproducible workflows by default

> 🧩 Scripts are designed to be flexible and modular: you can run them individually, chain them in `main.*`, or explore them interactively using Jupyter or RMarkdown.

---
</details>

### <a id="unit-testing"></a>
<details>
<summary><strong>🧪 Unit Testing</strong></summary><br>

Unit tests play a critical role in **ensuring the reliability and reproducibility** of your research code. This template provides built-in testing support for **Python**, **R**, **MATLAB**, and **Stata** to help you catch errors early and build trust in your results.

It supports both:

- **Traditional unit testing** – write tests to validate existing code
- **Test-Driven Development (TDD)** – write tests before code to guide design

> 🧪 Test scaffolding is automatically generated for each core analysis script (e.g., `s00_main`, `s04_preprocessing`), making it easy to integrate testing from day one.

---

### 📁 File Structure & Test Execution

During setup, a dedicated `tests/` folder is created. Matching test files are generated for each language and script:

| Language | Test Framework     | Code Folder     | Test Folder         | File Format     | Run Command                                                   |
|----------|--------------------|------------------|----------------------|------------------|----------------------------------------------------------------|
| Python   | `pytest`           | `src/`           | `tests/`             | `test_*.py`      | `pytest`                                                       |
| R        | `testthat`         | `R/`             | `tests/testthat/`    | `test-*.R`       | `testthat::test_dir("tests/testthat")`<br>`Rscript -e '...'`   |
| MATLAB   | `matlab.unittest`  | `src/`           | `tests/`             | `test_*.m`       | `runtests('tests')`<br>`matlab -batch "..."`                   |
| Stata    | `.do` script-based | `stata/do/`      | `tests/`             | `test_*.do`      | `do tests/test_s00_main.do`<br>`stata -b do tests/...`         |

📄 Example (Python):

```
# Matching tests
src/s00_main.py
tests/test_s00_main.py

# Run Tests
pytest
```

💡 See the [CI section](#-continuous-integration-ci) for more on automated test execution.

---

### ✅ Best Practices

- **Test core logic and workflows** – e.g., cleaning, transformation, modeling functions  
- **Cover edge cases** – missing data, invalid inputs, unexpected file formats  
- **Write independent tests** – avoid shared state between tests  
- **Use language-specific assertions:**
  - Python: `assert`
  - R: `expect_equal()`, `expect_error()`
  - MATLAB: `verifyEqual()`, `verifyTrue()`
  - Stata: `assert`

🧩 Match test names to your scripts for clarity:  
Example: `s05_modeling.R` → `test-s05_modeling.R`

> ✅ Your tests don’t have to be exhaustive. Focus on **critical functions** and **key workflow branches**.

---
</details>

### <a id="ci"></a>
<details>
<summary><strong>⚙️ Continuous Integration (CI)</strong></summary><br>

Continuous Integration (CI) helps ensure your research project is **reproducible, portable, and robust** across different systems. This template includes built-in CI support for **Python**, **R**, and **MATLAB** using:

- **GitHub Actions**
- **GitLab CI/CD**
- **Codeberg CI** (Woodpecker)

✅ Even without writing **unit tests**, the default CI configuration will still verify that your project environment installs correctly across platforms (e.g., Linux, Windows, macOS).This provides early detection of broken dependencies, incompatible packages, or missing setup steps — critical for collaboration and long-term reproducibility.

#### 🔁 What the CI Pipeline Does

Each auto-generated CI pipeline:

1. Installs the appropriate language runtime (e.g., Python, R, MATLAB)
2. Installs project dependencies:
   - Python: via `requirements.txt`
   - R: via `renv::restore()` using `R/renv.lock`
3. Executes tests in the `tests/` directory (if present)
4. Outputs logs and results for debugging or documentation

#### ✅ Supported CI Platforms

| Platform     | Supported Languages     | OS Support              | Config File                |
|--------------|--------------------------|--------------------------|----------------------------|
| **GitHub**   | Python, R, MATLAB        | Linux, Windows, macOS    | `.github/workflows/ci.yml` |
| **GitLab**   | Python, R, MATLAB        | Linux only               | `.gitlab-ci.yml`           |
| **Codeberg** | Python, R *(no MATLAB)*  | Linux only               | `.woodpecker.yml`          |

> ⚠️ **Stata is not supported** on any CI platform due to licensing limitations and lack of headless automation.

#### ⚠️ MATLAB CI Caveats

MATLAB CI support is included as a **starter configuration**. It may require manual setup, including licensing and tokens.

- **GitHub Actions**: Uses [`setup-matlab`](https://github.com/matlab-actions/setup-matlab) and requires a `MATLAB_TOKEN`.
- **GitLab CI/CD**: Uses [MathWorks' CI template](https://github.com/mathworks/matlab-gitlab-ci-template) and requires a license server or `MLM_LICENSE_FILE`.

#### 📝 Codeberg CI Requires Activation

CI is **not enabled by default** on Codeberg. To enable:

- Submit a request via [Codeberg CI Activation Form](https://codeberg.org/Codeberg-e.V./requests/issues/new?template=ISSUE_TEMPLATE%2fWoodpecker-CI.yaml)
- Learn more in the [Codeberg CI documentation](https://docs.codeberg.org/ci/)

#### 🛠️ CI Control via CLI

You can toggle CI setup on or off at any time using the built-in CLI:

```bash
repokit ci-control --on
repokit ci-control --off
```

##### 🧷 Skip CI for a Commit

Use this Git alias to skip CI on minor commits:

```
git commit-skip "Updated documentation"
```

---
</details>

### <a id="directory-structure"></a>
<details>
<summary><strong>📁 Directory Structure</strong></summary><br>

This template uses a modular folder layout that promotes transparency, reproducibility, and clear separation of data, code, results, and documentation—making your project easy to navigate and maintain.

📝 File and folder descriptions are stored in `pyproject.toml` under `[tool.research_template.file_descriptions]`. See the [Configuration Files section](#-configuration-files-root-level) for details.

#### 🗂️ Top-Level Overview

```
├── .git/                     # Git repository metadata
├── .gitignore                # Files/folders excluded from Git tracking
├── .github/                  # GitHub Actions workflows for CI/CD
├── .venv/                    # Local Python virtual environment
├── .conda/                   # Local Conda environment (Python/R)
├── LICENSE.txt               # License for code, data, and documentation
├── CITATION.cff              # Citation metadata for scholarly reference
├── README.md                 # Main README with project usage and structure
├── pyproject.toml            # Project metadata and CLI configuration
├── activate.* / deactivate.* # Environment activation scripts (.ps1/.sh)
├── environment.yml           # Conda environment definition
├── requirements.txt          # pip-compatible Python dependency list
├── renv.lock                 # R package lock file created by renv
├── uv.lock                   # Python package lock file created by uv

```

> 🔁 `activate.*` and `deactivate.*` are either PowerShell (`.ps1`) or Bash (`.sh`) scripts, depending on your platform (Windows or macOS/Linux).

#### 📦 Project Subdirectories

```
├── bin/                     # Executables and helper tools (e.g., rclone)
├── data/
│   ├── .git/                # Git repo for tracking datasets
│   ├── .gitlog              # Git commit log specific to datasets
│   ├── 00_raw/              # Original, immutable input data
│   ├── 01_interim/          # Cleaned/transformed intermediate data
│   ├── 02_processed/        # Final, analysis-ready datasets
│   └── 03_external/         # Data from third-party sources
├── docs/                    # Documentation, reports, or rendered output
├── results/
│   └── figures/             # Visual outputs (charts, plots, etc.)
```

#### 🔧 Setup & Configuration

```
├── setup/
│   ├── pyproject.toml       # CLI tool registration and config
│   ├── dependencies.txt     # Setup-specific Python dependencies
│   └── repokit/               # Utility scripts for setup and automation
```

#### 🧬 Source Code

```
└── src (R/stata)/
    ├── dependencies.txt            # src-level dependency list
    ├── get_dependencies.*          # Dependency installation logic
    ├── s00_main.*                  # Full workflow orchestration
    ├── s00_workflow.*              # Notebook-based pipeline
    ├── s01_install_dependencies.*  # Project package installer
    ├── s02_utils.*                 # Shared helper functions
    ├── s03_data_collection.*       # Data import/generation logic
    ├── s04_preprocessing.*         # Data cleaning and transformation
    ├── s05_modeling.*              # Statistical modeling and ML
    └── s06_visualization.*         # Plotting and summaries
```

> ✳️ Script extensions (`.py`, `.R`, `.do`, `.m`) depend on the language selected during project setup.

#### 🧪 Unit Tests

```
├── tests/
│   ├── test_get_dependencies.*           # Tests dependency resolution
│   ├── test_s00_main.*                   # Tests pipeline orchestration
│   ├── test_s01_install_dependencies.*   # Tests installation logic
│   ├── test_s02_utils.*                  # Tests utility functions
│   ├── test_s03_data_collection.*        # Tests data handling
│   ├── test_s04_preprocessing.*          # Tests data cleaning
│   ├── test_s05_modeling.*               # Tests modeling logic
│   └── test_s06_visualization.*          # Tests plotting and outputs
```

> ✳️ Script extensions (`.py`, `.R`, `.do`, `.m`) depend on the language selected during project setup.

---
</details>

### <a id="dcas"></a>
<details>
<summary><strong>📚 DCAS Compatibility</strong></summary><br>

This template is designed to support the creation of replication packages that are fully compatible with the [Data and Code Availability Standard (DCAS)](https://datacodestandard.org/), a widely endorsed initiative to promote transparency and reproducibility in social science research.

By structuring code, data, metadata, and documentation into clear, well-separated folders—with standard naming conventions, licensing, and README scaffolds—the template helps you align with the expectations of journals that require or recommend DCAS compliance.

Key features that support DCAS alignment:

- 📂 Separation of raw, interim, and processed data
- 📜 Auto-generated licensing and citation metadata (`LICENSE.txt`, `CITATION.cff`)
- 🧪 Scripted environment setup and reproducibility utilities
- 📄 Optional DCAS template folder with journal-ready content

This format is consistent with the [AEA Data Editor’s guidance](https://aeadataeditor.github.io/aea-de-guidance/preparing-for-data-deposit.html) and the broader Social Science Data Editors' best practices.

**Examples of journals endorsing the DCAS standard:**

- [American Economic Journal: Applied Economics](https://www.aeaweb.org/journals/applied-economics)
- [Econometrica](https://www.econometricsociety.org/publications/econometrica)
- [Economic Inquiry](https://onlinelibrary.wiley.com/journal/14680299)
- [Journal of Economic Perspectives](https://www.aeaweb.org/journals/jep)

For a full list of supporting journals, visit the [DCAS website](https://datacodestandard.org/journals/).

> 📝 Journal-specific requirements may vary—always consult their latest submission guidelines to ensure full compliance.

---
</details>

---

## 🙏 Acknowledgements

This project was inspired by:

- [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/)

Maintained by the **CBS High-Performance Computing (HPC)** team.

---

## 📬 Support

For questions, suggestions, or bug reports:

- Open an [Issue on GitHub](https://github.com/CBS-HPC/replication_package/issues)
- Or contact: [kgp.lib@cbs.dk](mailto:kgp.lib@cbs.dk)

---
