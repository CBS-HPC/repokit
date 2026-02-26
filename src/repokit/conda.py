"""Conda-specific environment helpers for repokit.env."""

from __future__ import annotations

import os
import pathlib
import platform
import subprocess

import yaml

from repokit_common import PROJECT_ROOT, is_installed


def set_conda_packages(
    version_control, python_env_manager, r_env_manager, conda_python_version, conda_r_version
):
    install_packages = []

    if python_env_manager.lower() == "conda":
        install_packages.extend([f"python={conda_python_version}"] if conda_python_version else ["python"])
    if r_env_manager.lower() == "conda":
        install_packages.extend([f"r-base={conda_r_version}"] if conda_r_version else ["r-base"])

    install_packages.extend(["uv"])

    if version_control.lower() in ["git", "dvc", "datalad"] and not is_installed("git", "Git"):
        install_packages.extend(["git"])

    os_type = platform.system().lower()
    if version_control.lower() == "datalad":
        if not is_installed("rclone", "Rclone", local_path="./bin"):
            install_packages.extend(["rclone"])
        if os_type in ["darwin", "linux"] and not is_installed("git-annex", "git-annex"):
            install_packages.extend(["git-annex"])

    return install_packages


def export_conda_env(env_path: str = None, output_file: str = "environment.yml"):
    """Export details of a conda environment by path to a YAML file."""
    if not env_path:
        env_path = str(PROJECT_ROOT / pathlib.Path("./.conda"))

    env_path = os.path.abspath(env_path)
    output_file = os.path.abspath(output_file)

    def update_conda_env_file(file_path: str):
        with open(file_path, encoding="utf-8") as f:
            env_data = yaml.safe_load(f)

        if env_data is None:
            print(f"Failed to parse environment YAML at {file_path}")
            return

        if "prefix" in env_data:
            prefix_path = env_data["prefix"]
            env_data["name"] = os.path.basename(prefix_path)
            del env_data["prefix"]
            with open(file_path, "w", encoding="utf-8") as f:
                yaml.dump(env_data, f, default_flow_style=False)

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            subprocess.run(["conda", "env", "export", "--prefix", env_path], stdout=f, check=True)
        update_conda_env_file(output_file)
        print(f"Environment exported to: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to export conda environment: {e}")
    except FileNotFoundError:
        print("Conda is not installed or not found in PATH.")

