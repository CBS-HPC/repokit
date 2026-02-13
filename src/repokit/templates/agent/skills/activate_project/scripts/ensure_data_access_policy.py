#!/usr/bin/env python3
import datetime as dt
import re
from pathlib import Path

try:
    import tomllib
except Exception as exc:  # pragma: no cover
    raise SystemExit(f"tomllib is required: {exc}")


SECTION_HEADER = "[tool.data_access]"
BEGIN_MARKER = "# BEGIN tool.data_access (auto-managed)"
END_MARKER = "# END tool.data_access (auto-managed)"


def yes_no(prompt: str, default: bool = True) -> bool:
    suffix = " [Y/n]: " if default else " [y/N]: "
    raw = input(prompt + suffix).strip().lower()
    if not raw:
        return default
    return raw in {"y", "yes"}


def top_level_dirs(root: Path) -> list[str]:
    skip = {
        ".git",
        ".venv",
        ".conda",
        "__pycache__",
        "bin",
        "setup",
    }
    dirs: list[str] = []
    for item in sorted(root.iterdir(), key=lambda p: p.name.lower()):
        if not item.is_dir():
            continue
        if item.name.startswith("."):
            continue
        if item.name in skip:
            continue
        dirs.append(item.name)
    return dirs


def parse_index_selection(raw: str, n: int) -> list[int]:
    if not raw.strip():
        return []
    out: list[int] = []
    for part in raw.split(","):
        p = part.strip()
        if not p:
            continue
        idx = int(p)
        if idx < 1 or idx > n:
            raise ValueError(f"Index out of range: {idx}")
        if idx not in out:
            out.append(idx)
    return out


def prompt_sensitive_paths(root: Path) -> list[str]:
    dirs = top_level_dirs(root)
    if not dirs:
        return []
    print("\nSelect top-level directories containing sensitive/proprietary data or documents.")
    print("Enter comma-separated numbers (example: 1,3). Leave empty for none.")
    for i, d in enumerate(dirs, start=1):
        print(f"{i:2d}. {d}/")
    while True:
        raw = input("Selection: ")
        try:
            picks = parse_index_selection(raw, len(dirs))
            break
        except Exception as exc:
            print(f"Invalid selection: {exc}")
    return [f"{dirs[i - 1]}/**" for i in picks]


def load_pyproject(pyproject_path: Path) -> tuple[dict, str]:
    text = pyproject_path.read_text(encoding="utf-8")
    data = tomllib.loads(text)
    return data, text


def get_existing_data_access(data: dict) -> dict | None:
    tool = data.get("tool")
    if not isinstance(tool, dict):
        return None
    access = tool.get("data_access")
    return access if isinstance(access, dict) else None


def render_data_access_section(
    sensitive_paths: list[str],
    agent_mode: str = "metadata-only",
) -> str:
    contains = "true" if bool(sensitive_paths) else "false"
    today = dt.date.today().isoformat()
    lines = [
        SECTION_HEADER,
        'tool-description = "Agent access policy for sensitive/proprietary data and documents."',
        f"contains_sensitive_data = {contains}",
        f'agent_data_access = "{agent_mode}"',
        "sensitive_paths = [",
    ]
    for p in sensitive_paths:
        lines.append(f'  "{p}",')
    lines.append("]")
    lines.extend(
        [
            "allowed_metadata_paths = [",
            '  "README.md",',
            '  "pyproject.toml",',
            '  "dmp.json",',
            '  "TASKS.md",',
            "]",
            f'last_confirmed = "{today}"',
            "",
        ]
    )
    return "\n".join(lines)


def upsert_data_access_section(pyproject_text: str, section_text: str) -> str:
    pattern = re.compile(
        r"(?ms)^\[tool\.data_access\]\n.*?(?=^\[.*\]|\Z)"
    )
    if pattern.search(pyproject_text):
        updated = pattern.sub(section_text, pyproject_text).rstrip() + "\n"
        return updated
    return pyproject_text.rstrip() + "\n\n" + section_text


def extract_sensitive_paths(data: dict) -> list[str]:
    access = get_existing_data_access(data)
    if not access:
        return []
    raw = access.get("sensitive_paths")
    if not isinstance(raw, list):
        return []
    out: list[str] = []
    for item in raw:
        if isinstance(item, str) and item.strip():
            out.append(item.strip())
    return out


def update_ignore_file(path: Path, sensitive_paths: list[str]) -> None:
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    block_lines = [BEGIN_MARKER]
    block_lines.extend(sensitive_paths)
    block_lines.append(END_MARKER)
    block = "\n".join(block_lines) + "\n"

    pattern = re.compile(
        re.escape(BEGIN_MARKER) + r".*?" + re.escape(END_MARKER) + r"\n?",
        flags=re.S,
    )
    if pattern.search(existing):
        new_text = pattern.sub(block, existing)
    else:
        sep = "" if not existing or existing.endswith("\n") else "\n"
        new_text = existing + sep + ("\n" if existing.strip() else "") + block
    path.write_text(new_text, encoding="utf-8")


def main() -> None:
    root = Path.cwd().resolve()
    pyproject = root / "pyproject.toml"
    if not pyproject.exists():
        raise SystemExit("pyproject.toml not found in current directory.")

    data, text = load_pyproject(pyproject)
    existing = get_existing_data_access(data)

    if existing is None:
        print("[tool.data_access] is not defined.")
        sensitive = prompt_sensitive_paths(root)
    else:
        print("Existing [tool.data_access] detected.")
        current = extract_sensitive_paths(data)
        print("Current sensitive paths:", current if current else "[]")
        if yes_no("Is this data access policy still correct?", default=True):
            sensitive = current
        else:
            sensitive = prompt_sensitive_paths(root)

    if sensitive:
        print("\nDefaulting agent_data_access to 'metadata-only' for sensitive content.")
    section = render_data_access_section(sensitive_paths=sensitive, agent_mode="metadata-only")
    updated = upsert_data_access_section(text, section)
    pyproject.write_text(updated, encoding="utf-8")

    update_ignore_file(root / ".codexignore", sensitive)
    update_ignore_file(root / ".claudeignore", sensitive)
    update_ignore_file(root / ".cursorignore", sensitive)

    print("Updated pyproject.toml [tool.data_access].")
    print("Synced sensitive paths to .codexignore, .claudeignore, and .cursorignore.")


if __name__ == "__main__":
    main()
