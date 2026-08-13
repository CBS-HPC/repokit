import subprocess
import sys


def test_import():
    import repokit  # noqa: F401


def test_common_v1_integration_imports(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import repokit.env; import repokit.vcs.datalad_w; import repokit.vcs.dvc_w",
        ],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
