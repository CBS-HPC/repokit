"""CLI entrypoint for repokit-only commands."""
from __future__ import annotations

import argparse
import sys

ALIASES = {
    "deps-update": "deps",
    "readme-update": "readme",
    "templates-reset": "templates",
    "examples-code": "ex-code",
    "examples-test": "tests",
    "ex-test": "tests",
    "ex-tests": "tests",
    "git-config": "git",
    "ci-control": "ci",
}

COMMAND_HELP = {
    "copy": "Copy/sync files based on project rules.",
    "deps": "Update dependency metadata and lockfiles.",
    "readme": "Regenerate README.md.",
    "templates": "Regenerate script templates.",
    "ex-code": "Generate code example scripts.",
    "tests": "Generate test examples.",
    "git": "Apply Git configuration helpers.",
    "ci": "Enable/disable CI configuration.",
    "lint": "Run language-aware linting.",
    "agent": "Scaffold agent files/skills.",
}


def _dispatch(func, argv: list[str], prog: str) -> None:
    old_argv = sys.argv
    try:
        sys.argv = [prog, *argv]
        func()
    finally:
        sys.argv = old_argv


def main(argv: list[str] | None = None) -> None:
    if argv is None:
        argv = sys.argv[1:]
    if argv:
        argv = [ALIASES.get(argv[0], argv[0]), *argv[1:]]

    parser = argparse.ArgumentParser(
        prog="repokit", description="repokit core commands"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    for name, help_text in COMMAND_HELP.items():
        sub.add_parser(name, help=help_text, description=help_text)

    ns, passthrough = parser.parse_known_args(argv)
    cmd = ns.command

    if cmd == "copy":
        from . import scp

        _dispatch(scp.main, passthrough, "repokit copy")
    elif cmd == "deps":
        from . import deps

        _dispatch(deps.main, passthrough, "repokit deps")
    elif cmd == "readme":
        from .readme import template as readme_template

        _dispatch(readme_template.main, passthrough, "repokit readme")
    elif cmd == "templates":
        from .templates import code as templates_code

        _dispatch(templates_code.main, passthrough, "repokit templates")
    elif cmd == "ex-code":
        from .templates import example as templates_example

        _dispatch(templates_example.main, passthrough, "repokit ex-code")
    elif cmd == "tests":
        from .templates import tests as templates_tests

        _dispatch(templates_tests.main, passthrough, "repokit tests")
    elif cmd == "git":
        from . import repos

        _dispatch(repos.main, passthrough, "repokit git")
    elif cmd == "ci":
        from . import ci

        _dispatch(ci.ci_control, passthrough, "repokit ci")
    elif cmd == "lint":
        from . import linting

        _dispatch(linting.main, passthrough, "repokit lint")
    elif cmd == "agent":
        from . import agent

        _dispatch(agent.main, passthrough, "repokit agent")


if __name__ == "__main__":
    main()
