#!/usr/bin/env python3
"""
BackupUtility Script

Backs up repositories from a source workspace to a backup destination.
Supports two modes:
    - repository_folder: Backs up individual repositories within configured umbrella folders (Core/, Applications/, etc.)
  - single_folder: Backs up entire folder as one unit

- If repository doesn't exist in destination, copies directly
- If repository exists in destination, creates a versioned backup
"""

import os
import shutil
import sys
from pathlib import Path

if __package__:
    from ..bootstrap import bootstrap_syncbot_config_loader
else:
    src_path = Path(__file__).resolve().parents[2]
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))
    from Syncbot.bootstrap import bootstrap_syncbot_config_loader


bootstrap_syncbot_config_loader(anchor_file=__file__)

from tUilKit import get_logger, get_config_loader

# Initialize logger and config loader at module level
logger = get_logger()
config_loader = get_config_loader()
SKIP_LOG_DIRS = {"logFiles", "logs"}


def ignore_log_folders(_source, names):
    """Ignore Syncbot-style runtime log folders during repository backups."""
    return {name for name in names if name in SKIP_LOG_DIRS}

def get_workspace_config():
    """Load workspace configuration from Syncbot config."""
    global_config = config_loader.global_config
    workspace = global_config.get("WORKSPACE", {})
    backup_mode = global_config.get("BACKUP_MODE", {})
    
    return {
        "base_path": Path(workspace.get("base_path", Path("."))),
        "backup_destination": Path(workspace.get("backup_destination", "./_backup")),
        "mode": backup_mode.get("mode", "repository_folder"),
        "umbrellas": backup_mode.get("repository_folder_umbrellas", ["Core", "Applications"]),
        "single_target": backup_mode.get("single_folder_target", None)
    }

def get_repository_version(repository_path):
    """Extract version from a repository's pyproject.toml."""
    pyproject_file = repository_path / "pyproject.toml"
    if pyproject_file.exists():
        try:
            import tomllib
            with open(pyproject_file, 'rb') as f:
                data = tomllib.load(f)
                # Try poetry format
                version = data.get("tool", {}).get("poetry", {}).get("version")
                if version:
                    return version
                # Try PEP 621 project format
                version = data.get("project", {}).get("version")
                if version:
                    return version
        except Exception as e:
            logger.colour_log("!warn", f"Warning: Could not read version from {pyproject_file}: {e}")
    return "unknown"

def list_repositories_from_umbrellas(base_path, umbrellas):
    """List repositories organized by umbrella structure (Core/, Applications/, etc.)."""
    repositories = {}
    
    for umbrella in umbrellas:
        umbrella_path = base_path / umbrella
        if umbrella_path.exists():
            umbrella_repositories = []
            for item in umbrella_path.iterdir():
                is_repo = (item / "pyproject.toml").exists() or (item / "setup.py").exists()
                if item.is_dir() and is_repo and not item.name.startswith('.') and not item.name.startswith('_'):
                    umbrella_repositories.append(item.name)
            if umbrella_repositories:
                repositories[umbrella] = sorted(umbrella_repositories)
        else:
            logger.colour_log("!warn", f"Warning: Umbrella path {umbrella_path} does not exist")
    
    return repositories


def render_repository_backup_menu(repositories_by_umbrella, workspace_config):
    """Render an icon-rich repository backup menu and return indexed paths."""
    all_repositories = []
    repository_index = 1

    logger.colour_log("!info", "\n🗂️ Repository Backup Menu")
    logger.colour_log("!info", "Choose one repository or backup all listed repositories.")

    for umbrella, repositories in repositories_by_umbrella.items():
        logger.colour_log("!thisfolder", f"\n📁 {umbrella}/")
        for repository in repositories:
            repository_path = f"{umbrella}/{repository}"
            version = get_repository_version(workspace_config["base_path"] / repository_path)
            dest_path = workspace_config["backup_destination"] / repository_path
            exists_in_dest = dest_path.exists()

            logger.colour_log(
                "!list",
                f"  {repository_index}.",
                "!thisfolder",
                f"📦 {repository}",
                "!info",
                f"(v{version})",
            )
            if exists_in_dest:
                logger.colour_log("!done", "      ✅ Destination exists - versioned backup will be created")
            else:
                logger.colour_log("!warn", "      🆕 New in destination - direct backup will be created")

            all_repositories.append(repository_path)
            repository_index += 1

    logger.colour_log("!info", "\n🎯 Selection Options")
    logger.colour_log("!list", "  •", "!info", f"Enter a number (1-{len(all_repositories)}) to backup a single repository")
    logger.colour_log("!list", "  •", "!info", "Enter 'all' to backup every repository above")

    return all_repositories

def backup_repository(source_base, dest_base, repository_path, force_versioned=False, ignore_logs=False):
    """
    Backup a single repository with version checking.
    
    Args:
        source_base: Base path for source (e.g., Path("."))
        dest_base: Base path for destination (e.g., ./_backup)
        repository_path: Relative repository path (e.g., "Core/tUilKit" or "tUilKit")
        force_versioned: Force versioned backup even if destination does not exist
        ignore_logs: Skip runtime log folders (`logFiles`, `logs`) while copying
    """
    
    source_path = source_base / repository_path
    dest_path = dest_base / repository_path

    if not source_path.exists():
        logger.colour_log("!error", f"Error: Source repository {source_path} does not exist")
        return False

    # Ensure destination parent directory exists
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    # Get repository name (last part of path)
    repository_name = Path(repository_path).name
    dest_parent = dest_path.parent
    
    # Check if destination already exists
    if dest_path.exists() or force_versioned:
        version = get_repository_version(source_path)
        versioned_name = f"{repository_name}_v{version}"
        versioned_path = dest_parent / versioned_name

        logger.colour_log("!info", f"Repository {repository_path} exists in destination. Creating versioned backup: {versioned_name}")

        # Copy to versioned backup
        try:
            unique_name = versioned_name
            if versioned_path.exists():
                # Rename old backup instead of deleting (OneDrive sync compatibility)
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                old_backup_path = dest_parent / f"{versioned_name}_old_{timestamp}"
                logger.colour_log("!info", f"Versioned backup {versioned_name} exists, renaming old to {old_backup_path.name}...")
                os.rename(versioned_path, old_backup_path)

            copy_ignore = ignore_log_folders if ignore_logs else None
            shutil.copytree(source_path, versioned_path, ignore=copy_ignore)
            logger.colour_log("!done", f"✅ Created versioned backup: {unique_name}")
            return True

        except Exception as e:
            logger.colour_log("!error", f"❌ Error creating versioned backup: {e}")
            return False
    else:
        # Direct copy
        logger.colour_log("!info", f"Repository {repository_path} does not exist in destination. Creating direct backup.")

        try:
            copy_ignore = ignore_log_folders if ignore_logs else None
            shutil.copytree(source_path, dest_path, ignore=copy_ignore)
            logger.colour_log("!done", f"✅ Created direct backup: {repository_path}")
            return True

        except Exception as e:
            logger.colour_log("!error", f"❌ Error creating direct backup: {e}")
            return False

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Backup repositories with configurable workspace and backup modes")
    parser.add_argument('--dry-run', action='store_true', help='Show what would be backed up without actually copying')
    parser.add_argument('--force-versioned', action='store_true', help='Force versioned backup even for new repositories')
    parser.add_argument('--repository', help='Specific repository to backup (skip interactive selection)')
    parser.add_argument('--mode', choices=['repository_folder', 'single_folder'], 
                       help='Override backup mode from config')
    parser.add_argument('--folder', help='Specific folder to backup (for single_folder mode)')

    args = parser.parse_args()

    # Load workspace configuration
    workspace_config = get_workspace_config()
    backup_mode = args.mode if args.mode else workspace_config["mode"]
    
    logger.colour_log("!info", "🔄 Syncbot Backup Utility")
    logger.colour_log("!info", "=" * 40)
    logger.colour_log("!info", f"Mode: {backup_mode}")
    logger.colour_log("!info", f"Workspace: {workspace_config['base_path']}")
    logger.colour_log("!info", f"Destination: {workspace_config['backup_destination']}")

    if args.dry_run:
        logger.colour_log("!info", "🔍 DRY RUN MODE - No files will be copied")

    if backup_mode == "repository_folder":
        # Repository folder mode: scan umbrella structure for repositories.
        logger.colour_log("!info", "\n📂 Scanning umbrella structure for repositories...")
        
        repositories_by_umbrella = list_repositories_from_umbrellas(
            workspace_config['base_path'], 
            workspace_config['umbrellas']
        )

        if not repositories_by_umbrella:
            logger.colour_log("!error", "No repositories found in umbrella structure!")
            logger.colour_log("!info", f"Searched umbrellas: {', '.join(workspace_config['umbrellas'])}")
            logger.colour_log("!info", f"Base path: {workspace_config['base_path']}")
            return

        # Display repositories organized by umbrella.
        all_repositories = render_repository_backup_menu(
            repositories_by_umbrella,
            workspace_config,
        )

        # Get user choice or use command line argument.
        if args.repository:
            if args.repository.lower() == 'all':
                selected_repositories = all_repositories
            else:
            # Allow matching by repository name or full path
                selected_repositories = []
                for repository_path in all_repositories:
                    if args.repository in repository_path or args.repository == Path(repository_path).name:
                        selected_repositories.append(repository_path)
            
            if not selected_repositories:
                logger.colour_log("!error", f"Error: Repository '{args.repository}' not found")
                return
        else:
            while True:
                try:
                    print()
                    logger.colour_log("!info", "📌 Enter selection below")
                    choice = input("Your choice: ").strip().lower()

                    if choice == 'all':
                        selected_repositories = all_repositories
                        break
                    else:
                        choice_num = int(choice)
                        if 1 <= choice_num <= len(all_repositories):
                            selected_repositories = [all_repositories[choice_num - 1]]
                            break
                        else:
                            logger.colour_log("!warn", f"Please enter a number between 1 and {len(all_repositories)} or 'all'")

                except ValueError:
                    logger.colour_log("!warn", "Please enter a valid number or 'all'")

        # Process backups
        logger.colour_log("!info", "\n🔄 Starting backup process...")
        logger.colour_log("!info", f"Source: {workspace_config['base_path']}")
        logger.colour_log(
            "!info",
            f"Destination: {workspace_config['backup_destination']}"
        )
        if args.force_versioned:
            logger.colour_log("!warn", "⚙️ Mode: Force versioned backups")
        logger.colour_log("!info", "-" * 40)

        total_count = len(selected_repositories)
        success_count = 0
        for index, repository_path in enumerate(selected_repositories, start=1):
            logger.colour_log(
                "!list",
                f"\n[{index}/{total_count}]",
                "!thisfolder",
                f"📦 {repository_path}",
            )
            if args.dry_run:
                source_path = workspace_config['base_path'] / repository_path
                dest_path = workspace_config['backup_destination'] / repository_path
                version = get_repository_version(source_path)
                repository_name = Path(repository_path).name

                if dest_path.exists() or args.force_versioned:
                    versioned_name = f"{repository_name}_v{version}"
                    logger.colour_log(
                        "!warn",
                        f"🧪 Dry run: versioned backup -> {versioned_name}"
                    )
                else:
                    logger.colour_log(
                        "!warn",
                        f"🧪 Dry run: direct backup -> {repository_path}"
                    )
                logger.colour_log(
                    "!info",
                    "   ↳ log exclusions: logFiles/, logs/"
                )
                success_count += 1
            else:
                backup_ok = backup_repository(
                    workspace_config['base_path'],
                    workspace_config['backup_destination'],
                    repository_path,
                    args.force_versioned,
                    ignore_logs=True,
                )
                if backup_ok:
                    logger.colour_log("!done", "✅ Backup operation completed")
                    success_count += 1
                else:
                    logger.colour_log("!error", "❌ Backup operation failed")

        if args.dry_run:
            logger.colour_log(
                "!done",
                "\n🧪 Dry run complete! "
                f"Would backup {success_count}/{total_count} repositories"
            )
        else:
            logger.colour_log(
                "!done",
                "\n✅ Backup complete! "
                f"Successfully backed up {success_count}/{total_count} "
                "repositories"
            )

    elif backup_mode == "single_folder":
        # Single folder mode: backup entire folder as one unit
        folder_to_backup = (
            args.folder if args.folder else workspace_config.get('single_target')
        )

        if not folder_to_backup:
            logger.colour_log(
                "!error",
                "❌ No folder specified for single_folder mode"
            )
            logger.colour_log(
                "!info",
                "   ↳ Use --folder argument or set "
                "'single_folder_target' in config"
            )
            return

        source_path = workspace_config['base_path'] / folder_to_backup
        dest_path = workspace_config['backup_destination'] / folder_to_backup
        exists_in_dest = dest_path.exists()

        if not source_path.exists():
            logger.colour_log(
                "!error",
                f"❌ Source folder does not exist: {source_path}"
            )
            return

        logger.colour_log("!info", "\n📂 Single Folder Backup")
        logger.colour_log("!list", "  Target:", "!thisfolder", folder_to_backup)
        logger.colour_log("!list", "  Source:", "!thisfolder", str(source_path))
        logger.colour_log("!list", "  Destination:", "!thisfolder", str(dest_path))
        if exists_in_dest:
            logger.colour_log(
                "!done",
                "  ✅ Destination exists - versioned backup will be created"
            )
        else:
            logger.colour_log(
                "!warn",
                "  🆕 New in destination - direct backup will be created"
            )

        if args.dry_run:
            logger.colour_log(
                "!warn",
                f"\n🧪 Dry run: would backup entire folder -> {folder_to_backup}"
            )
            logger.colour_log("!done", "🧪 Dry run complete!")
        else:
            backup_ok = backup_repository(
                workspace_config['base_path'],
                workspace_config['backup_destination'],
                folder_to_backup,
                args.force_versioned,
                ignore_logs=False,
            )
            if backup_ok:
                logger.colour_log("!done", "\n✅ Backup complete!")
            else:
                logger.colour_log("!error", "\n❌ Backup failed!")

    else:
        logger.colour_log(
            "!error",
            f"❌ Unknown backup mode: {backup_mode}"
        )
        logger.colour_log(
            "!info",
            "   ↳ Valid modes: repository_folder, single_folder"
        )

if __name__ == "__main__":
    main()