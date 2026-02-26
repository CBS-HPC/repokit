"""CI and unit-test README section helpers."""

from __future__ import annotations

import fnmatch
import os
from pathlib import Path

from repokit_common import PROJECT_ROOT


def set_unit_tests(programming_language: str) -> str:
    lang_info = {
        "python": {
            "test_framework": "`pytest`",
            "code_folder": "`src/`",
            "test_folder": "`tests/`",
            "test_format": "`test_*.py`",
            "package_file": "`requirements.txt`",
        },
        "r": {
            "test_framework": "`testthat`",
            "code_folder": "`R/`",
            "test_folder": "`tests/testthat/`",
            "test_format": "`test-*.R`",
            "package_file": "`renv.lock`",
        },
        "matlab": {
            "test_framework": "`matlab.unittest`",
            "code_folder": "`src/`",
            "test_folder": "`tests/`",
            "test_format": "`test_*.m`",
            "package_file": "",
        },
        "stata": {
            "test_framework": "`.do` script-based",
            "code_folder": "`stata/do/`",
            "test_folder": "`tests/`",
            "test_format": "`test_*.do`",
            "package_file": "",
        },
    }

    if programming_language.lower() not in lang_info:
        return f"Unsupported language: {programming_language}"
    lang = lang_info[programming_language.lower()]
    folder_path = PROJECT_ROOT / Path(lang["test_folder"].replace("`", ""))
    md = (
        f"This template includes built-in support for **unit testing** in {programming_language.capitalize()} to promote research reliability and reproducibility.\n"
        f"| Language | Test Framework | Code Folder | Test Folder | Test File Format |\n"
        f"| --- | --- | --- | --- | --- |\n"
        f"| {programming_language.capitalize()} | {lang['test_framework']} | {lang['code_folder']} | {lang['test_folder']} | {lang['test_format']} |"
    )
    if not folder_path.exists():
        return md + f"\n\nTest folder not found: `{lang['test_folder']}`"

    test_pattern = lang["test_format"].replace("`", "")
    test_scripts = [f for f in os.listdir(str(folder_path)) if fnmatch.fnmatch(f, test_pattern)]
    if not test_scripts:
        return md + (
            f"\n\nNo valid test scripts were detected in `{lang['test_folder']}`.\n"
            f"Make sure test files follow the expected format: `{lang['test_format']}`"
        )
    listing = "\n".join(f"- **{name}**" for name in test_scripts)
    return md + f"\n\nThe following test scripts were detected in `{lang['test_folder']}`:\n{listing}"


def set_ci(programming_language: str, code_repo: str) -> str:
    ci_matrix = {
        "github": {
            "supports": ["python", "r", "matlab"],
            "config_file": ".github/workflows/ci.yml",
            "note": "",
        },
        "gitlab": {
            "supports": ["python", "r", "matlab"],
            "config_file": ".gitlab-ci.yml",
            "note": "",
        },
        "codeberg": {
            "supports": ["python", "r"],
            "config_file": ".woodpecker.yml",
            "note": (
                "No support for MATLAB or cross-platform testing.\n"
                "CI is not enabled by default on Codeberg and may require request/activation."
            ),
        },
    }
    lang_info = {
        "python": {"package_file": "`requirements.txt`"},
        "r": {"package_file": "`renv.lock`"},
        "matlab": {"package_file": ""},
        "stata": {"package_file": ""},
    }
    if programming_language.lower() not in lang_info:
        return f"Unsupported language: {programming_language}"
    if code_repo.lower() not in ci_matrix:
        return f"Unsupported code repository: {code_repo}"
    if programming_language.lower() not in ci_matrix[code_repo.lower()]["supports"]:
        return f"{programming_language.capitalize()} is not supported on {code_repo.capitalize()}."
    ci = ci_matrix[code_repo.lower()]
    return (
        f"CI is configured for **{code_repo.capitalize()}** (`{ci['config_file']}`) with "
        f"**{programming_language.capitalize()}** support.\n\n{ci['note']}"
    )
