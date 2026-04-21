# Copilot Instructions - Syncbot

## Purpose
Syncbot is a device-centric backup and synchronization application. Keep device discovery, hub/node configuration, and backup logic modular, schema-driven, and safe for multi-device use.
This file is minimal by design. All general rules, agent edit policies, and centralized log/config options are defined in the modular copilot-instructions files.

Refer to:
- [Modular copilot-instructions](./copilot-instructions.d/*.md) for extensions to the general rules in this file.

## Shared Policies Propagated from dev_local/.github
- Treat this repository as its own root. Do not depend on parent dev_local paths existing on another machine.
- Keep all config, logs, tests, and output locations config-driven. Respect ROOT_MODES, PATHS, LOG_FILES, and any `.d` override directories.
- Never hardcode machine-specific absolute paths.
- Use tUilKit config and logging patterns for production code; prefer factory-based access to shared services where available.
- Use semantic colour/log keys such as `!info`, `!proc`, `!done`, `!warn`, `!error`, `!path`, `!file`, `!data`, `!test`, `!pass`, `!fail`, and `!date`.
- Keep tests deterministic and update test bootstrap files such as `tests/test_paths.json` when path behavior changes.
- Update `README.md`, `CHANGELOG.md`, `pyproject.toml`, and config version fields together when behavior or releases change.
- Keep changelog dates in `YYYY-MM-DD` format and place substantive docs under `docs/`.

## Project-Specific Rules
- Device definitions under `config/devices.d/` should stay YAML-based and conform to the current Syncbot schema.
- All backup, sync, and routing paths must come from config or resolved device metadata, never from literal machine paths in source.
- Repository scanning should treat only real project repos as sync targets and avoid umbrella/container folders unless explicitly configured.
- Preserve dry-run safety, versioned-backup behavior, and clear logging for filesystem mutations.
- Tests and docs should be updated whenever hub/node schema, routing logic, or backup-mode behavior changes.
