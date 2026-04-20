## [0.5.0] - 2026-04-19
- Workspace migration to Core/SuiteTools/Applications layout.
- Path normalization for portable multi-device use (no machine-specific absolute roots).
- Consolidated Copilot instructions at project scope.

## [0.4.0] - 2026-04-19
- Workspace migration to Core/SuiteTools/Applications layout.
- Path normalization for portable multi-device use (no machine-specific absolute roots).
- Consolidated Copilot instructions at project scope.

# Changelog

All notable changes to this project will be documented in this file.

## [0.3.1] - 2026-04-17

### Changed
- Centralized deterministic config-loader bootstrap across main/package/direct module paths.
- Updated setup review metadata reads to use canonical `INFO` fields.
- Switched file-opening behavior to platform-aware commands (`os.startfile`, `open`, `xdg-open`).

### Added
- Syncbot bootstrap tests verifying workspace `.projects_config` precedence and local config fallback.

### Fixed
- Replaced remaining legacy `GLOBAL_CONFIG.json` references in Syncbot menu flows where primary runtime config is `Syncbot_CONFIG.json`.

## [0.3.0] - 2026-04-16

### Changed
- Standardized runtime configuration to canonical `Syncbot_CONFIG.json` structure and root-mode pathing.
- Removed legacy dual-primary config ambiguity by retiring `GLOBAL_CONFIG.json` as primary runtime source.
- Updated menu/config editor references to Syncbot-specific config naming.

### Added
- Project-local `GLOBAL_SHARED.d` support for colours, borders, test options, and timestamp options.

### Fixed
- `demo_menu.py` bootstrap ordering bug causing `NameError` when `config_loader` was referenced before initialization.

## [0.2.0] - 2026-03-11

### Added
- **Interactive Main Menu**: Full 9-option CLI menu (`main.py`) with rainbow header border, colour-coded option list, and graceful exit handling.
- **Backup Engine** (`proc/backup_projects.py`): Multi-mode backup execution supporting `repository_folder` and `single_folder` modes; version-stamped backup copies when destination already exists; reads workspace and backup config from `GLOBAL_CONFIG.json`.
- **Menu Operations** (`proc/menu_operations.py`): Complete set of menu handler functions — `review_setup`, `review_hubs`, `edit_config_files`, `add_hub`, `add_project`, `configure_hub_or_project`, `initialize_device_setup_wizard`, `run_startup_configuration_checks`.
- **GUI Path Browser**: `browse_for_path()` in menu_operations uses `tkinter.filedialog` on Windows with CLI fallback when tkinter is unavailable.
- **Help Screen**: `show_help()` with formatted overview of Syncbot functionality and key config locations.
- **First-Time Setup Wizard**: `initialize_device_setup_wizard()` guiding new users through device and HUB configuration.

### Changed
- **Startup Checks**: Application now runs `run_startup_configuration_checks()` on launch before displaying the main menu.
- **Description Update**: `pyproject.toml` description updated from scaffold placeholder to reflect full feature set.

### Technical Details
- All menu outputs use tUilKit colour-coded logging (`!info`, `!list`, `!warn`, `!error`, `!done` semantic keys).
- Backup destination and workspace paths driven by `GLOBAL_CONFIG.json` rather than hardcoded values.
- Module supports both package execution (`python -m Syncbot`) and direct script execution from `src/Syncbot/main.py`.

## [0.1.0] - 2026-01-14

### Added
- Initial project scaffold via M15tr355 retrofit
- Core project structure and packaging files


