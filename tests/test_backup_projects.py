"""Tests for Syncbot backup project helpers and backup flow."""

from pathlib import Path
import sys


SRC_PATH = Path(__file__).resolve().parents[1] / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from Syncbot.proc import backup_projects as bp


class _ConfigLoaderStub:
    def __init__(self, data):
        self.global_config = data


class _LoggerStub:
    def colour_log(self, *args, **kwargs):
        return None


def test_get_workspace_config_uses_core_and_applications_defaults(monkeypatch):
    """Default umbrellas should match migrated workspace layout."""
    monkeypatch.setattr(bp, "config_loader", _ConfigLoaderStub({}))
    cfg = bp.get_workspace_config()
    assert cfg["umbrellas"] == ["Core", "Applications"]


def test_list_repositories_from_umbrellas_filters_only_real_repos(tmp_path):
    """Only folders with pyproject.toml or setup.py should be considered repos."""
    base = tmp_path

    core = base / "Core"
    core.mkdir()

    valid_pyproject = core / "Alpha"
    valid_pyproject.mkdir()
    (valid_pyproject / "pyproject.toml").write_text("[project]\nname='alpha'\n", encoding="utf-8")

    valid_setup = core / "Beta"
    valid_setup.mkdir()
    (valid_setup / "setup.py").write_text("from setuptools import setup\n", encoding="utf-8")

    invalid_plain = core / "NotARepo"
    invalid_plain.mkdir()

    hidden_repo = core / ".HiddenRepo"
    hidden_repo.mkdir()
    (hidden_repo / "pyproject.toml").write_text("[project]\nname='hidden'\n", encoding="utf-8")

    underscore_repo = core / "_TempRepo"
    underscore_repo.mkdir()
    (underscore_repo / "pyproject.toml").write_text("[project]\nname='temp'\n", encoding="utf-8")

    result = bp.list_repositories_from_umbrellas(base, ["Core", "MissingUmbrella"])

    assert "Core" in result
    assert result["Core"] == ["Alpha", "Beta"]
    assert "MissingUmbrella" not in result


def test_backup_repository_direct_copy_ignores_log_folders(tmp_path, monkeypatch):
    """Direct backup should copy files and skip logFiles/logs when requested."""
    monkeypatch.setattr(bp, "logger", _LoggerStub())

    source_base = tmp_path / "source"
    dest_base = tmp_path / "dest"
    repo_rel = Path("Core") / "Gamma"

    src_repo = source_base / repo_rel
    src_repo.mkdir(parents=True)
    (src_repo / "pyproject.toml").write_text("[project]\nname='gamma'\nversion='0.1.0'\n", encoding="utf-8")
    (src_repo / "README.md").write_text("hello\n", encoding="utf-8")

    (src_repo / "logFiles").mkdir()
    (src_repo / "logFiles" / "runtime.log").write_text("ignore me\n", encoding="utf-8")
    (src_repo / "logs").mkdir()
    (src_repo / "logs" / "debug.log").write_text("ignore me\n", encoding="utf-8")

    ok = bp.backup_repository(source_base, dest_base, str(repo_rel), force_versioned=False, ignore_logs=True)

    assert ok is True
    copied = dest_base / repo_rel
    assert (copied / "README.md").exists()
    assert not (copied / "logFiles").exists()
    assert not (copied / "logs").exists()


def test_backup_repository_creates_versioned_folder_when_destination_exists(tmp_path, monkeypatch):
    """Existing destination should trigger versioned backup naming."""
    monkeypatch.setattr(bp, "logger", _LoggerStub())

    source_base = tmp_path / "source"
    dest_base = tmp_path / "dest"
    repo_rel = Path("Core") / "Delta"

    src_repo = source_base / repo_rel
    src_repo.mkdir(parents=True)
    (src_repo / "pyproject.toml").write_text(
        "[project]\nname='delta'\nversion='1.2.3'\n",
        encoding="utf-8",
    )
    (src_repo / "file.txt").write_text("payload\n", encoding="utf-8")

    existing_dest = dest_base / repo_rel
    existing_dest.mkdir(parents=True)

    ok = bp.backup_repository(source_base, dest_base, str(repo_rel), force_versioned=False)

    assert ok is True
    versioned_dest = dest_base / "Core" / "Delta_v1.2.3"
    assert (versioned_dest / "file.txt").exists()
