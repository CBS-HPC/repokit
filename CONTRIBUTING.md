# Contributing

## Development setup

Use Python 3.10 or later. Install the compatible internal wheels, then install this project without resolving internal dependencies from PyPI:

```bash
python -m pip install https://github.com/CBS-HPC/repokit-common/releases/download/v1.0.0/repokit_common-1.0.0-py3-none-any.whl
python -m pip install https://github.com/CBS-HPC/repokit-backup/releases/download/v0.1.0/repokit_backup-0.1-py3-none-any.whl
python -m pip install https://github.com/CBS-HPC/repokit-dmp/releases/download/v1.0.0/repokit_dmp-1.0.0-py3-none-any.whl
python -m pip install -e ".[dev]" --no-deps
```

Install the public dependencies declared in `pyproject.toml`, then run:

```bash
python -m pip check
python -m compileall -q src
pytest --cov=repokit --cov-report=term-missing
python -m build
twine check dist/*
```

Release tags must match `project.version`. The tag workflow creates the GitHub Release and uploads the wheel, source archive, and `SHA256SUMS` file.
