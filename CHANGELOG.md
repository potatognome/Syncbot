## [0.5.0] - 2026-04-19
- Workspace migration to Core/SuiteTools/Applications layout.
- Path normalization for portable multi-device use (no machine-specific absolute roots).
- Consolidated Copilot instructions at project scope.

## [0.4.0] - 2026-04-19
- Workspace migration to Core/SuiteTools/Applications layout.
- Path normalization for portable multi-device use (no machine-specific absolute roots).
- Consolidated Copilot instructions at project scope.

# Changelog

All notable changes to Syncbot will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.1] - 2026-04-17

### Changed
- **Entrypoint Bootstrap Consistency**: Centralized deterministic config bootstrap helpers so `main.py`, package imports, and direct module execution paths resolve `Syncbot_CONFIG.json` consistently.
- **Setup Review Metadata**: Updated setup display to read version/author/name from canonical `INFO` block with legacy-key fallback.
- **Cross-Platform Editor Launch**: Replaced non-Windows hardcoded open command with platform-aware editor/file launch behavior.

### Added
- **Bootstrap Coverage Tests**: Added Syncbot tests validating `.projects_config` override precedence and project-local fallback behavior.

### Fixed
- **Legacy Config Naming in Menus/Docs**: Corrected remaining references to `GLOBAL_CONFIG.json` where runtime primary config is `Syncbot_CONFIG.json`.

## [0.3.0] - 2026-04-16

### Changed
- **Config System Standardization**: Migrated Syncbot to canonical `Syncbot_CONFIG.json` schema with `INFO`, `ROOTS`, `ROOT_MODES`, `PATHS`, `SHARED_CONFIG`, `ALT_CONFIG`, `LOG_FILES`, and `LOG_CATEGORIES`.
- **Single Primary Config Rule**: Removed legacy `config/GLOBAL_CONFIG.json` to eliminate dual-primary ambiguity and ensure deterministic config discovery.
- **Shared Config Resolution**: Standardized `SHARED_CONFIG.PATH` usage to local `config/GLOBAL_SHARED.d/` conventions and aligned workspace/project mode behavior.
- **Menu Config References**: Updated configuration editor/menu references to use `Syncbot_CONFIG.json` naming.

### Added
- **Project Shared Defaults**: Added project-local `config/GLOBAL_SHARED.d/` payload (`COLOURS.json`, `BORDER_PATTERNS.json`, `TESTS_OPTIONS.json`, `TIME_STAMP_OPTIONS.json`) for consistent local fallback behavior.

### Fixed
- **Demo Bootstrap Reliability**: Repaired `demo_menu.py` startup initialization order so `config_loader` is created before `LOG_FILES` access, resolving runtime `NameError`.

## [0.2.3] - 2026-03-13

### Changed
- **Config Folder Review**: Confirmed all config files reside in project root `config/` folder; removed src-level config duplication.

## [0.2.2] - 2026-03-13

### Changed
- **Config Folder Consolidation**: All configuration files now reside in the project root `config/` folder. Removed src-level config folder usage.

## [0.2.1] - 2026-03-13

### Changed
- **Log Rooting Refactor**: All logs now routed to workspace-level `.logs/Syncbot/`.
- **Config Update**: Updated `config/GLOBAL_CONFIG.json` to use new log file paths.


