# Syncbot Device YAML Schema

**Last Updated:** 2026-03-11

This folder contains device-level YAML configuration files. The schema is repository-to-repository focused using `HUBS` and `NODES` mappings.

## Required Device Fields

- `name`: Human-readable device label
- `role`: `primary`, `secondary`, or `hub`
- `hostname`: Hostname used for auto-detection
- `enabled`: Enable or disable this device

## Device Defaults

- `DEFAULT_USER`
- `DEFAULT_GROUP`
- `IGNORE_FOLDERS`
- `IGNORE_FILES`
- `HUB_ASSIGNMENTS`

Recommended baseline:
- Add `logFiles` and `logs` to `IGNORE_FOLDERS` to avoid syncing runtime log output between devices.

## Repository Mappings

### `HUBS`
Dictionary keyed by hub repository ID. Each entry defines a repository that receives sync data.

Common fields:
- `repository_role`: `HUB`
- `repository_type`: `STANDARD` or `PROJECT`
- `path`: Absolute path or network path
- `is_primary`: Whether this is the primary hub route
- `enabled`: Enable or disable this mapping

Optional fields:
- `hub_device`: Logical hub device ID
- `Create_sub_folders`
- `Recursive`
- `remove_orphaned_files`
- `create_versioned_backups`
- `only_update_newer`
- `user_group_ownership`

### `NODES`
Dictionary keyed by node repository ID. Each entry defines a local repository that syncs to one or more hubs.

Common fields:
- `repository_role`: `NODE`
- `repository_type`: `STANDARD` or `PROJECT`
- `path`: Absolute local repository path
- `connected_hub_IDs`: Hub IDs from `HUBS` to sync with
- `is_primary`: Whether this is the primary node
- `enabled`: Enable or disable this mapping

Optional fields:
- `source_device`: Source device ID
- `Recursive`
- `remove_orphaned_files`
- `create_versioned_backups`
- `only_update_newer`
- `is_project_folder`
- `user_group_ownership`

## Sync Overrides

Use `SYNC_OPTION_OVERRIDES.excluded_folders` for sync-level exclusion rules.

Recommended baseline:
- Include `logFiles` and `logs` so repository-oriented sync jobs avoid copying runtime logs.

## Simplified Migration Policy

- `HUBS` and `NODES` are the single source of truth.
- Do not use legacy keys like `selected_projects`, `local_path`, `hub_path`, or `preferred_hubs`.

## Minimal Example

```yaml
name: Ghost Desktop
role: primary
hostname: GHOST
enabled: true

HUBS:
  nas_primary:
    repository_role: HUB
    repository_type: STANDARD
    path: "\\\\192.168.0.2\\devsrc"
    is_primary: true
    enabled: true

NODES:
  dev_local_main:
    repository_role: NODE
    repository_type: STANDARD
    path: "."
    connected_hub_IDs: [nas_primary]
    is_primary: true
    enabled: true
```


