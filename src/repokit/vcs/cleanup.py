"""DataLad/Git cleanup helpers."""

from __future__ import annotations

import os
import pathlib
import re
import shutil
import subprocess

from repokit_common import is_installed

GLOB_META = set("*?[")


def _run(cmd, cwd=None, check=True, capture=False):
    if capture:
        return subprocess.run(
            cmd,
            cwd=cwd,
            check=check,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    return subprocess.run(cmd, cwd=cwd, check=check)


def _first_token(line: str) -> str | None:
    s = line.strip()
    if not s or s.startswith("#"):
        return None
    m = re.match(r"(\S+)", s)
    return m.group(1) if m else None


def _non_wildcard_prefix(pathspec: str) -> str:
    ps = re.sub(r"/\*\*$", "/", pathspec)
    buf = []
    for ch in ps:
        if ch in GLOB_META:
            break
        buf.append(ch)
    return "".join(buf)


def _pathspec_exists(root: pathlib.Path, pathspec: str) -> bool:
    if pathspec == "*":
        return True
    local = pathspec.replace("/", os.sep)
    if not any(ch in GLOB_META for ch in pathspec):
        return (root / local).exists()
    prefix = _non_wildcard_prefix(pathspec)
    if not prefix:
        return True
    return (root / prefix.replace("/", os.sep)).exists()


def clean_gitattributes(project_root: pathlib.Path) -> int:
    ga = project_root / ".gitattributes"
    if not ga.exists():
        return 0
    original = ga.read_text(encoding="utf-8").splitlines(True)
    if not original:
        return 0

    backup = ga.with_suffix(ga.suffix + ".bak")
    shutil.copy2(ga, backup)

    kept, removed = [], []
    for line in original:
        tok = _first_token(line)
        if tok is None:
            kept.append(line)
            continue
        if _pathspec_exists(project_root, tok):
            kept.append(line)
        else:
            removed.append(line)

    if removed:
        ga.write_text("".join(kept), encoding="utf-8")
    backup.unlink()
    return len(removed)


def _list_absent_submodules_via_gitmodules(project_root: pathlib.Path) -> list[str]:
    gm = project_root / ".gitmodules"
    if not gm.exists():
        return []
    out = _run(
        ["git", "config", "-f", ".gitmodules", "--get-regexp", r"^submodule\..*\.path$"],
        cwd=project_root,
        check=False,
        capture=True,
    )
    absent = []
    for line in (out.stdout or "").splitlines():
        try:
            _key, path = line.split(None, 1)
        except ValueError:
            continue
        if not (project_root / path).exists():
            absent.append(path)
    return absent


def _git_unregister_submodule(project_root: pathlib.Path, rel_path: str) -> None:
    _run(["git", "rm", "--cached", "-r", "--ignore-unmatch", rel_path], cwd=project_root, check=False)
    _run(
        ["git", "config", "-f", ".gitmodules", "--remove-section", f"submodule.{rel_path}"],
        cwd=project_root,
        check=False,
    )
    if (project_root / ".gitmodules").exists():
        _run(["git", "add", ".gitmodules"], cwd=project_root, check=False)


def clean_subdatasets(project_root: pathlib.Path) -> list[str]:
    cleaned: list[str] = []
    if is_installed("datalad"):
        res = _run(
            ["datalad", "subdatasets", "--state", "absent", "--recursive", "--result-renderer", "json"],
            cwd=project_root,
            check=False,
            capture=True,
        )
        missing: list[str] = []
        for line in (res.stdout or "").splitlines():
            m = re.search(r'"path"\s*:\s*"([^"]+)"', line)
            if m:
                abs_path = pathlib.Path(m.group(1))
                try:
                    rel = abs_path.relative_to(project_root)
                    missing.append(rel.as_posix())
                except Exception:
                    pass

        for rel in missing:
            try:
                _run(["datalad", "remove", "-d", ".", "-r", "--nocheck", rel], cwd=project_root, check=True)
                _run(["datalad", "save", "-m", f"Unregister removed subdataset {rel}", rel], cwd=project_root, check=False)
                cleaned.append(rel)
            except subprocess.CalledProcessError:
                _git_unregister_submodule(project_root, rel)
                cleaned.append(rel)
    else:
        for rel in _list_absent_submodules_via_gitmodules(project_root):
            _git_unregister_submodule(project_root, rel)
            cleaned.append(rel)

    if cleaned:
        _run(["git", "commit", "-m", f"Unregister {len(cleaned)} removed subdataset(s)"], cwd=project_root, check=False)
    return cleaned


def datalad_cleaning(project_root: str | pathlib.Path = ".") -> None:
    root = pathlib.Path(project_root).resolve()
    if not (root / ".git").is_dir():
        raise SystemExit(f"Not a Git repo: {root}")
    clean_gitattributes(root)
    clean_subdatasets(root)

