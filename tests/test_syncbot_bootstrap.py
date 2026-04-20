"""Tests for Syncbot bootstrap config resolution helpers."""

from pathlib import Path
import sys


SRC_PATH = Path(__file__).resolve().parents[1] / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from Syncbot.bootstrap import resolve_syncbot_config_path


def test_resolve_prefers_projects_config(tmp_path):
    """Workspace-level .projects_config file should win when present."""
    workspace = tmp_path / "workspace"
    project = workspace / "Dev" / "Syncbot"
    src_syncbot = project / "src" / "Syncbot"
    src_syncbot.mkdir(parents=True)

    anchor = src_syncbot / "main.py"
    anchor.touch()

    local_config = project / "config" / "Syncbot_CONFIG.json"
    local_config.parent.mkdir(parents=True)
    local_config.write_text("{}", encoding="utf-8")

    projects_config = workspace / ".projects_config" / "Syncbot_CONFIG.json"
    projects_config.parent.mkdir(parents=True)
    projects_config.write_text("{}", encoding="utf-8")

    resolved = resolve_syncbot_config_path(anchor)
    assert resolved == projects_config


def test_resolve_falls_back_to_local_config(tmp_path):
    """Local project config should be used when override file is absent."""
    workspace = tmp_path / "workspace"
    project = workspace / "Dev" / "Syncbot"
    src_syncbot = project / "src" / "Syncbot"
    src_syncbot.mkdir(parents=True)

    anchor = src_syncbot / "main.py"
    anchor.touch()

    local_config = project / "config" / "Syncbot_CONFIG.json"
    local_config.parent.mkdir(parents=True)
    local_config.write_text("{}", encoding="utf-8")

    resolved = resolve_syncbot_config_path(anchor)
    assert resolved == local_config
