"""Syncbot bootstrap helpers for deterministic config loading."""

from pathlib import Path

from tUilKit.utils.config import ConfigLoader
import tUilKit.factories


def resolve_syncbot_config_path(anchor_file=None):
    """Resolve Syncbot config path with workspace override fallback."""
    anchor = Path(anchor_file).resolve() if anchor_file else Path(__file__).resolve()
    project_root = None
    for parent in [anchor.parent, *anchor.parents]:
        has_src = (parent / "src" / "Syncbot").exists()
        has_config = (parent / "config" / "Syncbot_CONFIG.json").exists()
        if has_src and has_config:
            project_root = parent
            break

    if project_root is None:
        if "src" in anchor.parts:
            src_index = anchor.parts.index("src")
            project_root = Path(*anchor.parts[:src_index])
        else:
            project_root = anchor.parent

    workspace_root = project_root.parent.parent
    workspace_config = workspace_root / ".projects_config" / "Syncbot_CONFIG.json"
    local_config = project_root / "config" / "Syncbot_CONFIG.json"

    if workspace_config.exists():
        return workspace_config
    return local_config


def bootstrap_syncbot_config_loader(anchor_file=None):
    """Inject Syncbot ConfigLoader into tUilKit factory singleton."""
    config_path = resolve_syncbot_config_path(anchor_file)
    tUilKit.factories._config_loader = ConfigLoader(config_path=str(config_path))
