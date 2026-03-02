import fnmatch
import os
import pathlib
import platform
import shutil
import subprocess
from datetime import datetime
import cpuinfo
import psutil
import re
from typing import Iterable, List, Union, Optional
from repokit_common import PROJECT_ROOT, get_version, language_dirs, load_from_env, read_toml
from .ci import set_ci, set_unit_tests
from .runtime import has_ci, has_conda, has_tests

extension_map = {
    "r": (".R", ".Rmd"),
    "python": (".py", ".ipynb"),
    "stata": (".do", ".ipynb"),
    "matlab": (".m", [".ipynb", ".mlx"]),
    "sas": (".sas", ".ipynb"),
}


def main_text(json_file, code_path):
    programming_language = load_from_env("PROGRAMMING_LANGUAGE", ".cookiecutter")

    repo_name = load_from_env("REPO_NAME", ".cookiecutter")

    code_repo = load_from_env("CODE_REPO", ".cookiecutter")

    authors = load_from_env("AUTHORS", ".cookiecutter")

    orcids = load_from_env("ORCIDS", ".cookiecutter")

    emails = load_from_env("EMAIL", ".cookiecutter")

    project_name = load_from_env("PROJECT_NAME", ".cookiecutter")

    project_description = load_from_env("PROJECT_DESCRIPTION", ".cookiecutter")

    py_manager = load_from_env("PYTHON_ENV_MANAGER", ".cookiecutter")

    # Determine repo host and user

    if code_repo.lower() == "github":
        repo_user = load_from_env("GITHUB_USER")

        hostname = load_from_env("GITHUB_HOSTNAME") or "github.com"

    elif code_repo.lower() == "gitlab":
        repo_user = load_from_env("GITLAB_USER")

        hostname = load_from_env("GITLAB_HOSTNAME") or "gitlab.com"

    elif code_repo.lower() == "codeberg":
        repo_user = load_from_env("CODEBERG_USER")

        hostname = load_from_env("CODEBERG_HOSTNAME") or "codeberg.org"

    else:
        repo_user, hostname = None, None

    py_version = get_version("python")

    software_version = get_version(programming_language)

    conda_version = get_version("conda") if py_manager.lower() == "conda" else "conda"

    pip_version = get_version("pip")

    uv_version = get_version("uv")

    install = set_setup(
        programming_language,
        py_version,
        software_version,
        conda_version,
        pip_version,
        uv_version,
        repo_name,
        repo_user,
        hostname,
    )

    activate = set_activate()

    contact = set_contact(authors, orcids, emails)

    usage, run_command = set_scripts(programming_language, code_path, json_file)

    config = set_config_table()

    cli_section = _set_cli()

    dcas = set_dcas()

    code_path = language_dirs.get(programming_language.lower())

    system_spec = set_specs()

    ci_section = set_ci(programming_language, code_repo)

    unit_tests = set_unit_tests(programming_language)

    unit_tests_block = ""
    if has_tests(PROJECT_ROOT) and unit_tests.strip():
        unit_tests_block = (
            "<details>\n\n"
            "<summary><strong>Unit Testing</strong></summary><br>\n\n"
            f"{unit_tests}\n\n"
            "</details>\n"
        )


    ci_block = ""
    if has_ci(PROJECT_ROOT) and ci_section.strip():
        ci_block = (
            "<details>\n\n"
            "<summary><strong>Continuous Integration (CI)</strong></summary><br>\n\n"
            f"{ci_section}\n\n"
            "</details>\n"
        )


    dataset_section = set_dataset()

    if programming_language.lower() != "python":
        head = f"Instructions for installing {py_version}, {software_version}, and dependencies"

    else:
        head = f"Instructions for installing {software_version}, and dependencies"


    header = f"""# {project_name}

{project_description}

## Author & Contact

{contact}

<details>

<summary><strong>Initial Setup</strong></summary><br>

{head}

{install}

</details>

<details>

<summary><strong>Project Activation</strong></summary><br>

To configure the project's environment including project paths, environment variables, and virtual environments - run the activation script for your operating system. These scripts read settings from the `.env` file.

{activate}

</details>

<details>

<summary><strong>Code Scripts</strong></summary><br>

The project is written in **{software_version}** and includes modular scripts for standardized workflows, organized under `{code_path}`.

##### Run the Main Script

To execute the full workflow pipeline, run the main orchestration script from the terminal:

```

{run_command}

```

<details>

<summary><strong>Expand for showing detected Scripts:</strong></summary>

{usage}

</details>

</details>

{unit_tests_block}

{ci_block}

<details>

<summary><strong>Configuration Files (Root-Level)</strong></summary><br>

{config}

</details>

<details>

<summary><strong>CLI Utilities</strong></summary><br>

{cli_section}

</details>

<details>

<summary><strong>Dataset List</strong></summary><br>

{dataset_section}

</details>

<details>

<summary><strong>Project Directory Structure</strong></summary><br>

The current repository structure is shown below. Descriptions can be edited in `./pyproject.toml`.

```tree

```

</details>

"""

    return header


def set_activate():
    os_type = platform.system().lower()

    if os_type == "windows":
        usage = """**On Windows (PowerShell)**

```powershell

# Activate

./activate.ps1

# Deactivate

./deactivate.ps1

```"""

    elif os_type in ("darwin", "linux"):
        usage = """**On Linux/macOS (bash)**

```bash

# Activate

source activate.sh

# Deactivate

source deactivate.sh

```"""

    return usage


def set_setup(
    programming_language,
    py_version,
    software_version,
    conda_version,
    pip_version,
    uv_version,
    repo_name,
    repo_user,
    hostname,
):
    code_path = language_dirs.get(programming_language.lower())

    # setup_dependencies = read_dependencies(str(PROJECT_ROOT / "setup/dependencies.txt"))

    code_dependencies = read_dependencies(str(PROJECT_ROOT / f"{code_path}/dependencies.txt"))

    setup = ""

    if repo_name and repo_user:
        setup += "#### Clone the Project Repository\n"

        "This will donwload the repository to your local machine. '.env' file is not include in the online repository.\n"

        "Clone the repository using the following command:\n"

        setup += "```\n"

        if hostname:
            setup += f"git clone https://{hostname}/{repo_user}/{repo_name}.git\n```\n"

    setup += (
        "#### Navigate to the Project Directory\n"
        "Change into the project directory:\n"
        "```\n"
        f"cd {repo_name}\n"
        "```\n"
    )

    setup += f"#### {py_version}\n"

    if programming_language.lower() == "python":
        setup += f"Project environment using {software_version} can be setup using the options described below.\n\n"

    else:
        setup += f"Project `repokit` environment using **{py_version}** can be setup using the options described below.\n\n"

    if has_conda(PROJECT_ROOT):
        setup += f">Only the **Conda** will install **{py_version}** along with its dependencies. For pip and uv installation methods, **{py_version}** must already be installed on your system.\n\n"

    if programming_language.lower() in ["matlab", "stata", "sas"]:
        f"Project `code` environment using **{software_version}** can be installed using the options described below.\n\n"

        setup += f"These methods do **not** install external the proprietary software **{software_version}** which to be installed manually.\n\n"

    setup += f"""<details>

<summary><strong>Uv & Pip Installation (Recommended)</strong></summary><br>


To install using `requirements.txt`:

Alternatively, use **{pip_version}** directly (may be slower and less reproducible)

```
pip install -r requirements.txt
```

Recommended: Use **[{uv_version}](https://github.com/astral-sh/uv)** for faster and more reproducible installs

```
uv pip install -r requirements.txt
```

Or, if a `uv.lock` file is available and you want full reproducibility:

```
uv pip install --strict uv.lock

```

</details>

"""

    if has_conda(PROJECT_ROOT):
        if programming_language.lower() == "r":
            conda_title = f"Conda Installation (Installs **{py_version}** and **{software_version}**)"

        else:
            conda_title = f"Conda Installation (Installs **{py_version}**)"

        setup += f"""<details>

<summary><strong>{conda_title}</strong></summary><br>

Install the required dependencies using **{conda_version}** and the provided `environment.yml` file:

```
conda env create -f environment.yml
```

</details>

"""
    if programming_language.lower() == "python":
        setup += f"""#### {software_version}

The project code in `{code_path}` has the following {software_version} dependencies detected:

```code_dependencies 
{code_dependencies}
```

"""

    if programming_language.lower() == "r":
        setup += f"""#### {software_version}

The project code in `{code_path}` is written in **{software_version}** and can be set up using one of the option described below.

To use **{software_version}**, it must already be installed on your system.

The detected {software_version} dependencies are listed below:

```code_dependencies 
{code_dependencies}
```

##### Renv Installation

To install R packages required by this project, use the `renv` package within the `/R` directory and the provided lock file (`renv.lock`):

```

cd R

Rscript -e \"renv::restore()\"

```

> Warning: Ensure you are using **{software_version}** for full compatibility. If `renv` is not already installed, run:

```
install.packages("renv")
```

"""

    if programming_language.lower() in ["matlab", "stata"]:
        setup += f"""#### {software_version}

The project code in `{code_path}` is written in **{software_version}** and requires it to be pre-installed on your system. Once {software_version} is available, you can set up the environment using one of the options described below.

The following dependencies have been detected for **{software_version}**:

```code_dependencies 
{code_dependencies}
```

"""

    return setup


def _to_list(x: Optional[Union[str, Iterable[str]]]) -> List[str]:
    """Turn a string (split on , or ;) or an iterable into a clean list."""

    if x is None:
        return []

    if isinstance(x, str):
        return [p.strip() for p in re.split(r"[;,]", x) if p.strip()]

    return [str(p).strip() for p in x if str(p).strip()]


def set_contact(authors=None, orcids=None, emails=None):
    a = _to_list(authors)

    o = _to_list(orcids)

    e = _to_list(emails)

    n = max(len(a), len(o), len(e))

    if n == 0:
        return ""

    blocks = []

    for i in range(n):
        lines = []

        if i < len(a) and a[i]:
            lines.append(f"**Name:** {a[i]}\n")

        if i < len(o) and o[i]:
            lines.append(f"**ORCID:** {o[i]}\n")

        if i < len(e) and e[i]:
            lines.append(f"**Email:** {e[i]}\n")

        if lines:
            blocks.append("\n\n".join(lines))

    return "\n\n---\n\n".join(blocks) + ("\n\n---\n\n" if blocks else "")


def find_scripts(folder_path, source_ext, notebook_ext):
    if isinstance(notebook_ext, str):
        notebook_exts = [notebook_ext.lower()]

    else:
        notebook_exts = [ext.lower() for ext in notebook_ext]

    # prefix_pattern = re.compile(r'^s(\d{2})_', re.IGNORECASE)

    found = []

    for root, _, files in os.walk(folder_path):
        for fn in files:
            ext = os.path.splitext(fn)[1].lower()

            if ext == source_ext.lower():
                kind = "source"

            elif ext in notebook_exts:
                kind = "notebook"

            else:
                continue

            # m = prefix_pattern.match(fn)

            # if not m:

            #    continue

            # prefix = int(m.group(1))

            found.append((kind, os.path.join(root, fn)))

    # found.sort(key=lambda x: x[0])

    # return [(kind, path) for _, kind, path in found]

    return found


def get_run_command(orchestrator, programming_language):
    if not orchestrator:
        return None

    script_name = os.path.relpath(orchestrator).replace("\\", "/")

    base_name = os.path.splitext(os.path.basename(script_name))[0]

    command_map = {
        "python": lambda s: f"python {s}",
        "r": lambda s: f"Rscript {s}",
        "stata": lambda s: f"stata-mp -b do {s}",
        "matlab": lambda s: f'matlab -batch "{base_name}"',
        "sas": lambda s: f"sas {s}",
    }

    return command_map.get(programming_language.lower(), lambda s: f"<run {s}>")(script_name)


def set_scripts(programming_language, folder_path, json_file="./file_description.json"):
    """

    Generate the README section for Script Structure and Usage based on the programming language,

    and return the appropriate run command for the main orchestration script.

    Returns

    -------

        tuple[str, str]: (Formatted markdown for README, run command string)

    """

    programming_language = programming_language.lower()

    if programming_language not in ["r", "python", "stata", "matlab", "sas"]:
        raise ValueError("Supported programming languages are: r, python, stata, matlab, sas.")

    # Set extensions

    source_ext, notebook_ext = extension_map.get(programming_language.lower(), (".txt", ".txt"))

    scripts = find_scripts(folder_path, source_ext, notebook_ext)

    # Dectect Scripts

    file_descriptions = read_toml(
        json_filename=json_file, tool_name="file_descriptions", toml_path="pyproject.toml"
    )

    if not file_descriptions:
        file_descriptions = {}

    md = []

    for _, path in scripts:
        name = os.path.basename(path)

        display = os.path.splitext(name)[0].replace("_", " ").title()

        desc = file_descriptions.get(name)

        if desc:
            md.append(f"- **{display}** (`{name}`) <— {desc}")

        else:
            md.append(f"- **{display}** (`{name}`)")

    md.append("")

    if any("utils" in os.path.basename(p).lower() for _, p in scripts):
        md.append(
            "**Note**: `utils` does not define a `main()` function and should not be executed directly.\n"
        )

    orch_candidates = [
        path
        for kind, path in scripts
        if kind == "source" and os.path.basename(path).lower().startswith("s00_")
    ] or [
        path
        for kind, path in scripts
        if kind == "source" and os.path.basename(path).lower().startswith("main")
    ]

    orchestrator = orch_candidates[0] if orch_candidates else None

    if orchestrator:
        md.append(
            f"**The Content of the orchestration script `{os.path.basename(orchestrator)}` shown below:**\n"
        )

        try:
            code = open(orchestrator, encoding="utf-8").read().rstrip()

            md.append(f"```{programming_language.lower()}\n{code}\n```")

        except Exception as e:
            md.append(f"_Failed to read orchestrator script: {e}_")

    # Determine run command for README

    run_command = get_run_command(orchestrator, programming_language)

    return "\n".join(md), run_command


def set_config_table():
    files_to_check = [
        (
            "pyproject.toml",
            "Project metadata for packaging, CLI tools, sync rules, platform logic, and documentation",
        ),
        (
            ".env",
            "Defines environment-specific variables (e.g., paths, secrets). Typically excluded from version control.",
        ),
        (".gitignore", "Excludes unnecessary files from Git version control"),
        (
            "environment.yml",
            "Conda environment definition for Python/R, including packages and versions",
        ),
        ("requirements.txt", "Pip-based Python dependencies for lightweight environments"),
        ("renv.lock", "Records the exact versions of R packages used in the project"),
        ("uv.lock", "Locked Python dependencies file for reproducible installs with `uv`"),
    ]

    rows = []
    for filename, purpose in files_to_check:
        if (PROJECT_ROOT / filename).exists():
            rows.append(f"| `{filename}` | {purpose} |")

    if rows:
        base_config = (
            "The following configuration files are intentionally placed at the root of the repository. "
            "These are used by various tools for environment setup, dependency management, templating, and reproducibility.\n"
            "| File | Purpose |\n"
            "|------|---------|\n"
            + "\n".join(rows)
            + "\n\n"
        )
    else:
        base_config = (
            "No standard configuration files were detected at the repository root.\n\n"
        )

    if (PROJECT_ROOT / "pyproject.toml").exists():

        base_config += """

---
#### `pyproject.toml` Sections Explained
| Section                   | Purpose                                                                                      |
|---------------------------|----------------------------------------------------------------------------------------------|
| `[project]`               | Declares the base project metadata for Python tooling (name, version, dependencies, etc.).   |
| `[tool.uv]`               | Placeholder for settings related to the uv package manager (currently unused).               |
| `[tool.cookiecutter]`     | Stores project template metadata (e.g., author, licenses, language) for reproducibility and scaffolding. |
| `[tool.rcloneignore]`     | Defines file patterns to ignore when syncing with remote tools like Rclone.                  |
| `[tool.treeignore]`       | Specifies which files and folders to exclude from directory tree visualizations.             |
| `[tool.platform_rules]`   | Maps Python packages to operating systems for conditional installations.                     |
| `[tool.file_descriptions]`| Contains descriptions of files and directories for automation, UI labels, and documentation. |

"""

    return base_config








def _set_cli():
    cli_section = """

The Repokit toolchain is split into three command-line interfaces:

- [`repokit`](https://github.com/CBS-HPC/repokit) for core project automation

- [`repokit-backup`](https://github.com/CBS-HPC/repokit-backup) for backup/sync workflows

- [`repokit-dmp`]() for data management plan workflows

> **Note**: CLI tools are installed in the active environment.  

> Reinstall with: `uv pip install repokit` or `pip install repokit`

### `repokit` (core)
| Command | Description |
|---------|-------------|
| `repokit deps` | Updates dependency metadata for code environment. |
| `repokit readme` | Regenerates `README.md` from project metadata/structure. |
| `repokit templates` | Regenerates language script templates. |
| `repokit ex-code` | Generates code example scripts/notebooks. |
| `repokit tests` | Generates test examples. |
| `repokit git` | Applies Git configuration helpers. |
| `repokit ci` | Enables/disables CI configuration. |
| `repokit lint` | Runs language-aware linting workflows. |

### `repokit-backup`
| Command | Description |
|---------|-------------|
| `repokit-backup add` | Configure a backup remote and mapping. |
| `repokit-backup push` | Push/sync project data to remote storage. |
| `repokit-backup pull` | Restore/sync from remote to local project. |
| `repokit-backup diff` | Show remote/local diff report. |
| `repokit-backup list` | List configured remotes/mappings. |
| `repokit-backup delete` | Remove a configured remote mapping. |
| `repokit-backup transfer` | Transfer data between two remotes. |
| `repokit-backup types` | List supported remote types. |

### `repokit-dmp`
| Command | Description |
|---------|-------------|
| `repokit-dmp dataset` | Initialize/update dataset metadata and structure links. |
| `repokit-dmp update` | Create/update `dmp.json` from project metadata. |
| `repokit-dmp editor` | Launch Streamlit editor for DMP and publishing helpers. |
| `repokit-dmp dcas-migration` | Run DCAS migration/validation workflow. |

See [`repokit`](https://github.com/CBS-HPC/repokit), [`repokit-backup`](https://github.com/CBS-HPC/repokit-backup), and [`repokit-dmp`](https://github.com/CBS-HPC/repokit-dmp) READMEs for their CLI details

#### Usage

After activating your environment (see [Project Activation](#-project-activation)), run commands directly:

```bash

repokit-backup push --remote erda

repokit deps

repokit-dmp dataset

repokit templates

```

A full CLI walkthrough is maintained in the project README section for CLI tools.

"""

    return cli_section






def set_dcas():
    dcas = """To create a replication package that adheres to the [DCAS (Data and Code Sharing) standard](https://datacodestandard.org/), follow the guidelines ([AEA Data Editor's guidance](https://aeadataeditor.github.io/aea-de-guidance/preparing-for-data-deposit.html)) provided by the Social Science Data Editors. This ensures your research code and data are shared in a clear, reproducible format.

The following are examples of journals that endorse the Data and Code Availability Standard:

- [American Economic Journal: Applied Economics](https://www.aeaweb.org/journals/applied-economics)

- [Econometrica](https://www.econometricsociety.org/publications/econometrica)

- [Economic Inquiry](https://onlinelibrary.wiley.com/journal/14680299)

- [Journal of Economic Perspectives](https://www.aeaweb.org/journals/jep)

For a full list of journals, visit [here](https://datacodestandard.org/journals/).

Individual journal policies may differ slightly. To ensure full compliance, check the policies and submission guidelines of the journal."""

    return dcas


def set_dataset():
    return """ To set up or configure a dataset, run the following command:

```

repokit-dmp dataset

```

**The following datasets are included in the project:**
| Name             | Location        |Hash                       | Provided        | Run Command               | Number of Files | Total Size (MB) | File Formats         | Source          | DOI                | Citation               | License               | Notes                  |
|------------------|-----------------|---------------------------|-----------------|---------------------------|-----------------|-----------------|----------------------|-----------------|--------------------|------------------------|-----------------------|------------------------|

"""


def read_dependencies(dependencies_file):
    def collect_dependencies(content):
        current_software = None

        software_dependencies = {}

        # Parse the dependencies file

        for i, line in enumerate(content):
            line = line.strip()

            if line == "Software version:" and i + 1 < len(content):
                current_software = content[i + 1].strip()

                software_dependencies[current_software] = {"dependencies": []}

                continue

            if line == "Dependencies:":
                continue

            if current_software and "==" in line:
                package, version = line.split("==")

                software_dependencies[current_software]["dependencies"].append((package, version))

        return software_dependencies, package, version

    dependencies_section = ""

    # Check if the dependencies file exists

    if not os.path.exists(dependencies_file):
        return dependencies_section

    # Read the content from the dependencies file

    with open(dependencies_file) as f:
        content = f.readlines()

    software_dependencies, package, version = collect_dependencies(content)

    # Correctly loop through the dictionary

    for software, details in software_dependencies.items():
        for package, version in details["dependencies"]:
            dependencies_section += f"{package}: {version}\n"

    return dependencies_section


def set_specs():
    system_spec = get_system_specs()

    specs = f"""

The project was developed and tested on the following operating system:

{system_spec}

"""

    return specs


def get_system_specs():
    def detect_gpu():
        # Try NVIDIA

        if shutil.which("nvidia-smi"):
            try:
                output = (
                    subprocess.check_output(
                        ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
                        stderr=subprocess.DEVNULL,
                    )
                    .decode()
                    .strip()
                )

                gpus = output.splitlines()

                return ", ".join(gpus) if gpus else None

            except Exception:
                return None

        # Try PyTorch

        try:
            import torch

            if torch.cuda.is_available():
                gpus = [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())]

                return ", ".join(gpus)

        except ImportError:
            pass

        # Try AMD (Linux)

        if platform.system() == "Linux":
            try:
                lspci_output = subprocess.check_output(["lspci"], text=True)

                amd_gpus = [
                    line for line in lspci_output.splitlines() if "AMD" in line and "VGA" in line
                ]

                if amd_gpus:
                    return " / ".join(amd_gpus)

            except Exception:
                pass

            if shutil.which("rocm-smi"):
                try:
                    rocm_output = subprocess.check_output(
                        ["rocm-smi", "--showproductname"], text=True
                    )

                    rocm_lines = [
                        line.strip() for line in rocm_output.splitlines() if "GPU" in line
                    ]

                    return " / ".join(rocm_lines) if rocm_lines else None

                except Exception:
                    return None

        # Try Apple Silicon

        if platform.system() == "Darwin" and "Apple" in platform.processor():
            return platform.processor()

        return None  # GPU not detected

    def format_specs(info_dict):
        lines = []

        for k, v in info_dict.items():
            lines.append(f"- **{k}**: {v}")

        return "\n".join(lines) + "\n"

    info = {}

    # Basic OS and Python

    info["OS"] = f"{platform.system()} {platform.release()} ({platform.version()})"

    # CPU

    cpu = cpuinfo.get_cpu_info()

    info["CPU"] = cpu.get("brand_raw", platform.processor() or "Unknown")

    info["Cores (Physical)"] = psutil.cpu_count(logical=False)

    info["Cores (Logical)"] = psutil.cpu_count(logical=True)

    # RAM

    ram_gb = psutil.virtual_memory().total / (1024**3)

    info["RAM"] = f"{ram_gb:.2f} GB"

    # GPU detection

    gpu_info = detect_gpu()

    if gpu_info:
        info["GPU"] = gpu_info

    # Timestamp

    info["Collected On"] = datetime.now().isoformat()

    section_text = format_specs(info)

    return section_text


