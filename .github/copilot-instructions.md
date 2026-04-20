# Copilot Instructions: Syncbot Project

This instruction set governs key parameters and guidelines for Syncbot.

## Primary Project Parameters


## Centralized Log/Config Option

# Syncbot Project-Level Copilot Instructions

This file is minimal by design. All general rules, agent edit policies, and centralized log/config options are defined in the workspace and DEV umbrella copilot-instructions files.

Refer to:
- [Workspace copilot-instructions](../../.github/copilot-instructions.md)
- [DEV umbrella copilot-instructions](../.github/copilot-instructions.md)

Project-specific guidance:
- Device configs must be YAML and follow Syncbot schema.
- Document any new features or changes in the project changelog.
- All log/config paths must be config-driven (see parent instructions).

For any agent edits, follow workspace and umbrella rules unless a project-specific exception is documented here.

Syncbot must use config loader and the `LOG_ROOT_MODE` option in `GLOBAL_CONFIG.json` to determine log/config rooting (project or workspace). No hard-coded log/config paths; all paths must be config-driven. When `LOG_ROOT_MODE` is set to `workspace`, logs and configs are placed in workspace-level folders (e.g., `.logs/Syncbot/`, `config/`). When set to `project`, they are placed in project-specific folders. Agents must update tests, docs, and changelogs to reflect log/config rooting changes.

## User Variables & Configuration
- Devices: Configured in `config/devices.d/` with YAML files defining device properties, roles, and hub assignments
- HUBs: Configured in `config/devices.d/` with YAML files defining hub properties and network paths
- Repository NODEs: Configured in `config/devices.d/` with YAML files defining node properties and backup/sync settings
- User Permissions: Managed through device configs with role-based access control (e.g., admin, user, read-only)
- Global Settings: Configured in `GLOBAL_CONFIG.json` for overall system behavior (e.g., logging levels, default paths, centralized log/config rooting via `LOG_ROOT_MODE`)


### Syncbot
- **Purpose**: Device-centric backup/sync with multi-hub support
- **Architecture**: Menu-driven CLI, modular device configs in `config/devices.d/`
- **Current Version**: v2.0.0 (multi-hub architecture)
- **Key Modules**: 
  - `utils/device_detection.py` (device/hub discovery)
  - `utils/config_loader.py` (modular config loading)
  - `utils/path_resolver.py` (multi-hub routing)
- **Device Configs**: YAML schema v2.0.0 with hub assignment fields
- **Testing**: Use `verify_multihub_system.py` to validate configuration changes


## Startup / Initialization
- Check if device exists in /config/devices.d
- Check for at least one (primary) HUB and at least one (primary) NODE exist in framework
- Add devices and/or repositories to device YAML file under sections HUBS and NODES 
- OPTION: Configure Active user and group for ownership and permissions
- OPTION: Set up NEW repository
  - OPTION: Configure User:Group ownership (DEFAULT=CURRENT_USER:CURRENT_GROUP)
    - Link external permissions file to users.d folder for dynamic permission management
  - MANDATORY: Configure as either a HUB or a NODE
  - MANDATORY: Configure as either a PROJECT or a STANDARD folder
  - MANDATORY: Specify Drive Letter (Windows) or Mount Point (Linux)
  - MANDATORY: Specify Path (local or network) or BROWSE (Menu CLI) to select path
  - MANDATORY: Validate path accessibility and permissions

## Device Level Options

- DEFAULT_USER: (default=CURRENT_USER) The default user for file ownership and permissions when backing up to this device
- DEFAULT_GROUP: (default=CURRENT_GROUP) The default group for file ownership and permissions when backing up to this device
- IGNORE_FOLDERS: (default=[]) List of folder names to ignore during backup/sync operations on this device
- IGNORE_FILES: (default=[]) List of file names or patterns to ignore during backup/sync operations on this device
- HUB_ASSIGNMENTS: (default=[]) List of HUB names that this device is assigned to for backup/sync operations

## Repository Level Options
- Create_sub_folders: (default=True) Whether to create sub-folders for each project within the HUB
- Recursive: (default=True)Whether to automatically back up all sub-folders within a project
- remove_orphaned_files: (default=True) Whether to remove orphaned files during backup
- create_versioned_backups: (default=False) Whether to create versioned backups
- only_update_newer: (default=True) Whether to only update newer files
- is_project_folder: (default=True) Whether the folder is a project folder
- connected_hub_IDs: (default=[]) List of HUB IDs that this repository is connected to for backup/sync operations
- user_group_ownership: (default=CURRENT_USER:CURRENT_GROUP) User and group ownership


## Features to add
- Use ssh or alternative to sign in to remote device and configure a samba share to set up a new HUB 
- Ecosystem checks - Ensuring that every NODE has at least one accessible HUB and that every HUB has at least one connected NODE
- Backup/sync status monitoring with detailed logs and error reporting
