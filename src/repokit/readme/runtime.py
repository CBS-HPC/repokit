"""Runtime/environment detection helpers for README generation."""

from __future__ import annotations

from pathlib import Path


def has_conda(root: str | Path) -> bool:
    root_p = Path(root)
    return (root_p / ".conda").exists() or (root_p / "environment.yml").exists()


def has_tests(root: str | Path) -> bool:
    root_p = Path(root)
    return (root_p / "tests").exists() or (root_p / "test").exists()


def has_ci(root: str | Path) -> bool:
    root_p = Path(root)
    return (
        (root_p / ".github" / "workflows").exists()
        or (root_p / ".gitlab-ci.yml").exists()
        or (root_p / ".woodpecker.yml").exists()
        or (root_p / ".woodpecker").exists()
    )

