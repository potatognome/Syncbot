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

    # Prefer nearest workspace-level config discovered from project ancestors.
    workspace_config_candidates = []
    for parent in [project_root, *project_root.parents]:
        workspace_config_candidates.append(
            parent / ".workspace" / ".projects_config" / "Syncbot_CONFIG.json"
        )
        workspace_config_candidates.append(
            parent / ".projects_config" / "Syncbot_CONFIG.json"
        )
        # Backward-compatible Prismata nesting fallback.
        workspace_config_candidates.append(
            parent / "Prismata" / ".workspace" / ".projects_config" / "Syncbot_CONFIG.json"
        )

    local_config = project_root / "config" / "Syncbot_CONFIG.json"

    for candidate in workspace_config_candidates:
        if candidate.exists():
            return candidate

    return local_config


def bootstrap_syncbot_config_loader(anchor_file=None):
    """Inject Syncbot ConfigLoader into tUilKit factory singleton."""
    config_path = resolve_syncbot_config_path(anchor_file)
    import tUilKit.factories as _factories_mod  # noqa: PLC0415
    _factories_mod._config_loader = ConfigLoader(config_path=str(config_path))
