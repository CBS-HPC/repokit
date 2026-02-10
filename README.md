# repokit

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/CBS-HPC/repokit/actions/workflows/ci.yml/badge.svg)](https://github.com/CBS-HPC/repokit/actions/workflows/ci.yml)

Core utilities for the Research Template setup flow. `repokit` provides reusable setup helpers, CLI tools, and automation used by the cookiecutter template. It composes smaller, independent packages:

- repokit-common: shared utilities (env, prompts, paths, config helpers)
- repokit-backup: rclone-based backup tooling
- repokit-dmp: data management plan (DMP) tooling

## Installation

```bash
pip install repokit
```

From source:

```bash
git clone https://github.com/CBS-HPC/repokit.git
cd repokit
pip install -e .
```

## CLI overview

`repokit` provides a core CLI plus two companion CLIs that ship via dependencies:

- `repokit` (core)
- `repokit-backup` (backup/sync)
- `repokit-dmp` (DMP tooling)

### `repokit` commands

| Command | Description |
|---------|-------------|
| `repokit copy` | Copy/sync files based on project rules. |
| `repokit deps` | Update dependency metadata and lockfiles. |
| `repokit readme` | Regenerate `README.md`. |
| `repokit templates` | Regenerate script templates. |
| `repokit ex-code` | Generate code example scripts. |
| `repokit tests` | Generate test examples. |
| `repokit git` | Apply Git configuration helpers. |
| `repokit ci` | Enable/disable CI configuration. |
| `repokit lint` | Run language-aware linting. |
| `repokit agent` | Scaffold agent files/skills. |

Below is a detailed description of each CLI command available in the project, including usage, behavior, and example output.

### <a id="repokit-deps"></a>
<details>
<summary><strong>📦 <code>repokit deps</code></strong></summary>

The `repokit deps` command scans your project for imported packages and updates your dependency files (`requirements.txt`, `environment.yml`, and `uv.lock`) accordingly. It supports Python, R, MATLAB, and Stata, using language-specific tooling to track packages across `./src/` (or `./R/`, `./stata/do/`).

This command is useful for keeping your project environment reproducible and ensuring that all scripts and notebooks reference installable dependencies.

#### Usage

```bash
repokit deps
```

#### What it does

- Regenerates `requirements.txt` using `pip freeze`
- Ensures missing packages are added to `uv.lock` (if used)
- Scans the `./src/` (or `./R/`, `./stata/do/`) directories for imports and writes dependency lists:
  - `./src/dependencies.txt` (or `R/`, `stata/`)
- Updates and tags `environment.yml` and `requirements.txt` with platform-specific selectors (via `platform_rules`)
- Runs `renv` for R, or language-specific setup scripts for MATLAB and Stata

> Paths and rules are derived from the `pyproject.toml` and `platform_rules.json` config.

#### Example output

```bash
📄 requirements.txt has been created successfully.
✅ Conda environment file created: environment.yml
✅ requirements.txt updated with platform tags
✅ Updated environment.yml with Conda-style platform tags
```

---
</details>

### <a id="repokit-readme"></a>
<details>
<summary><strong>📝 <code>repokit readme</code></strong></summary>

The `repokit readme` command regenerates your `README.md` with up-to-date project information, including:

- Code metadata and environment details
- Project folder structure as a tree diagram
- Software dependencies (from `dependencies.txt`)
- Auto-generated descriptions for core files and scripts

This helps maintain a professional and standardized `README.md` that aligns with reproducibility and publication requirements (e.g., DCAS).

#### Usage

```bash
repokit readme-update
```

#### What it does

- Reads the selected programming language from `.cookiecutter`
- Parses existing files and structure to infer documentation
- Updates or inserts:
  - Code dependency section (`code_dependencies` fenced block)
  - File descriptions from `file_descriptions.json`
  - Directory structure (`tree` block in README)
- Regenerates the `README.md` with consistent formatting
- Automatically creates `README.md` if it doesn’t exist

> File and folder annotations are pulled from `file_descriptions.json`.
> Files ignored by `.treeignore` or `pyproject.toml -> treeignore.patterns` are excluded from the directory tree.

---
</details>

### <a id="repokit-ex-code"></a>
<details>
<summary><strong>💡 <code>repokit ex-code</code></strong></summary>

The `repokit ex-code` command generates realistic starter scripts and notebooks for your selected programming language using predefined Jinja2 templates.

This is useful for quickly bootstrapping a project with well-structured, language-appropriate examples for each analysis stage.

#### Usage

```bash
repokit ex-code
```

#### What it does

- Detects your project language from `.cookiecutter`
- Renders example scripts for:
  - `s00_main.*` (pipeline entry point)
  - `s01_install_dependencies.*` (dependency setup)
  - `s02_utils.*` (helper functions)
  - `s03_data_collection.*` to `s06_visualization.*` (workflow stages)
- Saves outputs in the appropriate `./src/`, `R/`, `stata/do/`, etc.
- Calls:
  - `get_dependencies` to update `dependencies.txt`
  - `repokit readme-update` to regenerate project metadata

> Uses templates from `repokit/templates/j2/example` inside the package.
> Script locations depend on your selected programming language.
> Existing files will be overwritten if they share the same name.

---
</details>

### <a id="repokit-templates"></a>
<details>
<summary><strong>🧱 <code>repokit templates</code></strong></summary>

The `repokit templates` command regenerates all core analysis and test scripts using predefined Jinja2 templates. It ensures a consistent structure and coding pattern across different scripting languages.

This command is useful for initializing or resetting project scripts to their default structure.

#### Usage

```bash
repokit templates
```

#### What it does

- Automatically detects your selected programming language from `.cookiecutter`
- Regenerates standard source scripts:
  - `s00_main.*` (pipeline orchestration)
  - `s01_install_dependencies.*` (package installation)
  - `s02_utils.*` (shared utilities)
  - `s03_data_collection.*` to `s06_visualization.*` (analysis stages)
  - `get_dependencies.*` (collects project dependencies)
- Generates:
  - `s00_workflow.*` (interactive notebook)
  - `test_*.*` (unit test scaffolds)

#### Output paths

- Scripts are placed in:
  - `./src/`, `./R/`, `./stata/do/`, or equivalent source directory
- Test templates are placed in:
  - `./tests/`, `./tests/testthat/`, etc., depending on language

> Uses Jinja2 templates stored in `repokit/templates/j2/code` inside the package.
> Existing scripts with the same name may be overwritten.

---
</details>

### <a id="repokit-git"></a>
<details>
<summary><strong>🌐 <code>repokit git</code></strong></summary>

The `repokit git` command sets up your version control system and configures a remote Git repository on GitHub, GitLab, or Codeberg based on environment settings.

This command streamlines the process of remote repo creation, authentication, Git setup, and CI pipeline configuration.

#### Usage

```bash
repokit git
```

#### What it does

- Reads repository settings from `.cookiecutter` and environment variables:
  - `REPO_NAME`, `CODE_REPO`, `VERSION_CONTROL`, `PROJECT_DESCRIPTION`
- Configures Git remotes using platform APIs:
  - GitHub REST API
  - GitLab API
  - Codeberg API
- Authenticates using personal access tokens (`GITHUB_TOKEN`, `GITLAB_TOKEN`, etc.)
- Initializes remote repositories and sets the correct `origin` URL
- Pushes the local repo to the remote and sets the tracking branch
- Automatically sets up CI configuration via `ci_config()`

#### Supports

- GitHub (requires `gh` CLI or PAT)
- GitLab (installs and uses `glab` CLI or token)
- Codeberg (via Gitea API + token)

> Remote login and repo creation are tested via platform-specific APIs.
> Pushes both root repo and data repo (if applicable).
> Can auto-install `gh` or `glab` if not found locally.

---
</details>

### <a id="repokit-ci"></a>
<details>
<summary><strong>⚙️ <code>repokit ci</code></strong></summary>

The `repokit ci` command lets you enable or disable Continuous Integration (CI) for your project, and generates default CI configurations for your selected language and Git platform (GitHub, GitLab, or Codeberg).

This tool is helpful for bootstrapping or adjusting your CI setup without manually editing `.yml` files.

#### Usage

```bash
repokit ci --on     # Enable CI
repokit ci --off    # Disable CI
```

> You must specify one flag: `--on` or `--off`.
> This command is safe to run multiple times and won't overwrite existing CI files.

#### What it does

- Automatically generates CI config based on:
  - Programming language (from `.cookiecutter`)
  - Git hosting service (`CODE_REPO`)
- Supports:
  - `.github/workflows/ci.yml` for GitHub
  - `.gitlab-ci.yml` for GitLab
  - `.woodpecker.yml` for Codeberg
- Adds a `git commit-skip` alias for bypassing CI on minor commits
- Enables/disables CI by renaming files:
  - `ci.yml.disabled` ↔ `ci.yml`
  - `.gitlab-ci.yml.disabled` ↔ `.gitlab-ci.yml`
  - `.woodpecker.yml.disabled` ↔ `.woodpecker.yml`

##### <a id="unit-testing"></a>
<details>
<summary><strong> Unit Testing</strong></summary><br>

Unit tests play a critical role in **ensuring the reliability and reproducibility** of your research code. This template provides built-in testing support for **Python**, **R**, **MATLAB**, and **Stata** to help you catch errors early and build trust in your results.

It supports both:

- **Traditional unit testing** â€“ write tests to validate existing code
- **Test-Driven Development (TDD)** â€“ write tests before code to guide design

> Test scaffolding is automatically generated for each core analysis script (e.g., `s00_main`, `s04_preprocessing`), making it easy to integrate testing from day one.

---

### File Structure & Test Execution

During setup, a dedicated `tests/` folder is created. Matching test files are generated for each language and script:

| Language | Test Framework     | Code Folder     | Test Folder         | File Format     | Run Command                                                   |
|----------|--------------------|------------------|----------------------|------------------|----------------------------------------------------------------|
| Python   | `pytest`           | `src/`           | `tests/`             | `test_*.py`      | `pytest`                                                       |
| R        | `testthat`         | `R/`             | `tests/testthat/`    | `test-*.R`       | `testthat::test_dir("tests/testthat")`<br>`Rscript -e '...'`   |
| MATLAB   | `matlab.unittest`  | `src/`           | `tests/`             | `test_*.m`       | `runtests('tests')`<br>`matlab -batch "..."`                   |
| Stata    | `.do` script-based | `stata/do/`      | `tests/`             | `test_*.do`      | `do tests/test_s00_main.do`<br>`stata -b do tests/...`         |

Example (Python):

```
# Matching tests
src/s00_main.py
tests/test_s00_main.py

# Run Tests
pytest
```

See the [CI section](#-continuous-integration-ci) for more on automated test execution.

---

### Best Practices

- **Test core logic and workflows** â€“ e.g., cleaning, transformation, modeling functions  
- **Cover edge cases** â€“ missing data, invalid inputs, unexpected file formats  
- **Write independent tests** â€“ avoid shared state between tests  
- **Use language-specific assertions:**
  - Python: `assert`
  - R: `expect_equal()`, `expect_error()`
  - MATLAB: `verifyEqual()`, `verifyTrue()`
  - Stata: `assert`

Match test names to your scripts for clarity:  
Example: `s05_modeling.R` â†’ `test-s05_modeling.R`

> âœ… Your tests donâ€™t have to be exhaustive. Focus on **critical functions** and **key workflow branches**.

---
</details>

### <a id="ci"></a>
<details>
<summary><strong>âš™ï¸ Continuous Integration (CI)</strong></summary><br>

Continuous Integration (CI) helps ensure your research project is **reproducible, portable, and robust** across different systems. This template includes built-in CI support for **Python**, **R**, and **MATLAB** using:

- **GitHub Actions**
- **GitLab CI/CD**
- **Codeberg CI** (Woodpecker)

âœ… Even without writing **unit tests**, the default CI configuration will still verify that your project environment installs correctly across platforms (e.g., Linux, Windows, macOS).This provides early detection of broken dependencies, incompatible packages, or missing setup steps â€” critical for collaboration and long-term reproducibility.

#### What the CI Pipeline Does

Each auto-generated CI pipeline:

1. Installs the appropriate language runtime (e.g., Python, R, MATLAB)
2. Installs project dependencies:
   - Python: via `requirements.txt`
   - R: via `renv::restore()` using `R/renv.lock`
3. Executes tests in the `tests/` directory (if present)
4. Outputs logs and results for debugging or documentation

#### Supported CI Platforms

| Platform     | Supported Languages     | OS Support              | Config File                |
|--------------|--------------------------|--------------------------|----------------------------|
| **GitHub**   | Python, R, MATLAB        | Linux, Windows, macOS    | `.github/workflows/ci.yml` |
| **GitLab**   | Python, R, MATLAB        | Linux only               | `.gitlab-ci.yml`           |
| **Codeberg** | Python, R *(no MATLAB)*  | Linux only               | `.woodpecker.yml`          |

> âš ï¸ **Stata is not supported** on any CI platform due to licensing limitations and lack of headless automation.

#### MATLAB CI Caveats

MATLAB CI support is included as a **starter configuration**. It may require manual setup, including licensing and tokens.

- **GitHub Actions**: Uses [`setup-matlab`](https://github.com/matlab-actions/setup-matlab) and requires a `MATLAB_TOKEN`.
- **GitLab CI/CD**: Uses [MathWorks' CI template](https://github.com/mathworks/matlab-gitlab-ci-template) and requires a license server or `MLM_LICENSE_FILE`.

#### Codeberg CI Requires Activation

CI is **not enabled by default** on Codeberg. To enable:

- Submit a request via [Codeberg CI Activation Form](https://codeberg.org/Codeberg-e.V./requests/issues/newtemplate=ISSUE_TEMPLATE%2fWoodpecker-CI.yaml)
- Learn more in the [Codeberg CI documentation](https://docs.codeberg.org/ci/)

#### CI Control via CLI

You can toggle CI setup on or off at any time using the built-in CLI:

```bash
repokit ci --on
repokit ci --off
```

##### Skip CI for a Commit

Use this Git alias to skip CI on minor commits:

```
git commit-skip "Updated documentation"
```

---
</details>

## Notes

- Installs CI templates from `repokit/templates/j2/ci` inside the package
- Only runs if a valid `CODE_REPO` is set
- CI files can be removed manually using `remove_ci_configs()` in code

---
</details>

### <a id="repokit-lint"></a>
<details>
<summary><strong>🧹 <code>repokit lint</code></strong></summary>

`repokit lint` runs project linting in a language-aware way. It looks for scaffolded scripts and executes them if present:

- Python → `src/linting.py` → Ruff (formatter + linter) and Mypy (type checker)
- R → `R/linting.R` → lintr::lint_dir() (auto-activates `renv` if `R/renv/activate.R` exists)
- MATLAB → `src/linting.m` → checkcode (static analysis)

#### Usage

```bash
repokit lint
```

#### Requirements

- Python: `ruff`, `mypy`
- R: `lintr` in your project’s `renv` (if used)
- MATLAB: `matlab` CLI on `PATH`

> The Python and MATLAB scripts live under `src/`, the R script under `R/`.
> CI YAML: implement a dedicated lint job/stage.

---
</details>

## Notes

- See `repokit-backup` and `repokit-dmp` READMEs for their CLI details.

## License

MIT


