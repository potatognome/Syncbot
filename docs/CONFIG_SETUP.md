# Syncbot Configuration Setup - Updated Structure

**Last Updated**: April 17, 2026  
**Version**: 0.3.1  
**Project Structure Version**: Umbrella v2.0+

---

## Overview

Syncbot has been updated to support the new multi-umbrella project structure across Windows development machines, Raspberry Pi, and Network Attached Storage (NAS). This document describes the current device configuration, paths, and sync policies.

---

## Project Umbrella Structure

Projects are now organized into three main umbrellas:

### 1. **Core/** (Core Packages)
- **tUilKit** — Utility library for CLI applications
- **Syncbot** — Device sync and backup utility
- **H3l3n** — Project scaffolding framework

### 2. **Applications/** (tUilKit-Enabled Apps)
- **crUPto** — Cryptocurrency/portfolio management application

### 3. **Dev_Archive/** (Archived & Staging)
- **_PORTS/** — Staging directory for project porting/retrofitting
- **_0_BACKUP_ARCHIVE** — Automated backup snapshots
- **_0_LOG_ARCHIVE** — Historical log snapshots
- **_0_TESTS_ARCHIVE** — Test result archives
- **_1_DEPRECATED** — Deprecated projects (read-only reference)
- **_2_DEPORTED** — Deported projects (read-only reference)
- **_3_REFACTOR** — Projects under refactoring

---

## Configured Devices

### 1. **Ghost Desktop** (Primary - Windows 11)

**Role:** Primary development hub
**Hostname:** GHOST  
**Machine:** GIGABYTE G6X9KG

**Paths:**
- **Local:** `.`
- **Hub:** `./_backup`

**Sync Configuration:**
- **Can Be Hub:** ✓ Yes
- **Preferred Hubs:** NAS (primary), OneDrive (fallback)
- **Config Source:** NAS
- **Peer Sync:** Disabled
- **Status:** ✓ Enabled

**Projects Synced:**
```
Dev:              tUilKit, Syncbot, H3l3n
Dev_Applications: crUPto
Dev_Archive:      _2_DEPORTED/BackupUtility
```

**Sync Options:**
- Remove orphaned files: ✓ Yes
- Create versioned backups: ✗ No
- Only update newer: ✓ Yes

---

### 2. **Falcon Laptop** (Secondary - Windows 11)

**Role:** Secondary development device  
**Hostname:** FALCON  
**Status:** Currently disabled

**Paths:**
- **Local:** `D:/Core/dev_local`
- **Hub:** `./_backup`

**Sync Configuration:**
- **Can Be Hub:** ✗ No
- **Preferred Hubs:** NAS, OneDrive
- **Config Source:** NAS
- **Peer Sync:** Disabled

**Projects Synced:**
```
Dev:              tUilKit, Syncbot, H3l3n
Dev_Applications: crUPto
Dev_Archive:      _2_DEPORTED
```

**Sync Options:**
- Remove orphaned files: ✗ No
- Create versioned backups: ✓ Yes
- Only update newer: ✓ Yes

---

### 3. **Raspberry Pi (johnnyfive)** (Secondary - ARM Linux)

**Role:** Secondary device for HAT development  
**Hostname:** johnnyfive  
**Model:** Raspberry Pi 3 Model B+  
**OS:** Raspberry Pi OS (Debian 11 Bullseye)  
**Status:** Currently disabled

**Paths:**
- **Local:** `/home/pi/dev_pi`
- **Hub:** `\\192.168.0.2\devsrc\dev_pi`

**Sync Configuration:**
- **Can Be Hub:** ✗ No
- **Preferred Hubs:** NAS, OneDrive
- **Config Source:** NAS
- **Peer Sync:** Disabled

**Projects Synced:**
```
Dev:              tUilKit, H3l3n
hat_dev:          colour_lab (HAT development & testing)
Projects:         (utilities)
```

**Sync Options:**
- Remove orphaned files: ✗ No
- Create versioned backups: ✓ Yes
- Only update newer: ✓ Yes
- **Excluded Folders:** `.pytest_cache`, `.git`, `__pycache__`, `.vscode`, `*.egg-info`, `venv`

---

### 4. **NAS Storage Server** (Hub - Network)

**Role:** Central backup and sync hub  
**Hostname:** nas.local  
**IP Address:** 192.168.0.2  
**Network Path Root:** `\\192.168.0.2\devsrc`

**Paths:**
- **Local/Hub:** `\\192.168.0.2\devsrc`
- All devices sync through this hub

**Sync Configuration:**
- **Can Be Hub:** ✓ Yes (primary hub)
- **Preferred Hubs:** (none - it is the hub)
- **Peer Sync:** Disabled

**Projects Stored:**
```
Dev:              tUilKit, Syncbot, H3l3n
Dev_Applications: crUPto
Dev_Archive:      _2_DEPORTED
```

**Excluded Repositories:**
- `git_forks/` — External third-party forks
- `pi/` — Raspberry Pi system files
- `venv/` — Virtual environments
- `*.whl` — Python wheel files
- `*.egg` — Python egg files

**Hub Sync Options:**
- Remove orphaned files: ✗ No
- Create versioned backups: ✗ No
- Only update newer: ✓ Yes
- Conflict resolution: `newest_wins`
- Dry run default: ✗ No

**Excluded Folders:**
- `_0_BACKUP_ARCHIVE`, `_0_LOG_ARCHIVE`, `_0_TESTS_ARCHIVE` — Snapshot archives
- `_1_DEPRECATED`, `_2_DEPORTED`, `_3_REFACTOR` — Old project archives
- `.pytest_cache`, `.git`, `__pycache__`, `.vscode` — Development artifacts
- `node_modules`, `venv`, `build`, `dist`, `*.egg-info` — Build & dependency artifacts
- `logFiles`, `outputFiles` — Generated files

---

## Multi-Hub Architecture (v2.0+)

Syncbot implements a **hub-and-spoke** sync model:

```
        ┌─────────────────┐
        │   NAS (Hub)     │
        │  192.168.0.2    │
        │ Central Backup  │
        └────────┬────────┘
                 │
        ┌────────┼────────┐
        │        │        │
   ┌────▼───┐ ┌─▼──────┐ ┌▼─────────────┐
   │ Ghost  │ │Falcon  │ │ Raspberry Pi │
   │  (PC)  │ │ (PC)   │ │   (ARM)      │
   │Enabled │ │Disabled│ │ Disabled     │
   └────────┘ └────────┘ └──────────────┘
```

**Sync Flow:**
1. All devices sync to/from NAS hub  
2. Devices do not sync directly with each other (peer sync disabled)
3. Config updates sourced from NAS hub
4. Conflict resolution: newest file wins

---

## Path Mapping Summary

| Device | Local Path | Hub Path |
|--------|-----------|----------|
| Ghost | `.` | `./_backup` |
| Falcon | `D:/Core/dev_local` | `<onedrive_root>/...` |
| Pi | `/home/pi/dev_pi` | `\\192.168.0.2\devsrc\dev_pi` |
| NAS | `\\192.168.0.2\devsrc` | (hub = local) |

---

## Common Sync Scenarios

### Enable Falcon for Development
```yaml
# In devices.d/falcon.yaml
enabled: true
```
Falcon will then sync with NAS hub on next run.

### Add New Repository to Sync
```yaml
# In any device config
NODES:
   new_project:
      name: NewProject
      path: ./Core/NewProject
      repository_role: NODE
      connected_hub_IDs: [nas_primary]
```

### Enable Pi Hardware Development
```yaml
# In devices.d/pi.yaml
enabled: true
```
Pi will sync `colour_lab` from NAS hub for HAT development.

### Exclude Additional Folders
```yaml
# In NAS config SYNC_OPTION_OVERRIDES
excluded_folders:
- "mytemp"
- "cache"
```

---

## Configuration Files

All device configurations located in:
```
Applications/Syncbot/config/devices.d/
├── ghost.yaml      # Primary Windows desktop
├── falcon.yaml     # Secondary Windows laptop
├── pi.yaml         # Raspberry Pi HAT development
└── nas.yaml        # NAS central hub
```

Global Syncbot configuration:
```
Applications/Syncbot/config/
├── Syncbot_CONFIG.json     # Project metadata
├── COLOURS.json            # Colour codes for output
└── BORDER_PATTERNS.json    # CLI border styles
```

---

## Deployment Scripts

**Current state after cleanup:**
- `deploy.bat` — Windows batch deployment script
- `deploy_to_nas.py` — Python script for NAS deployment

**Removed (development utilities):**
- ~~demo_help.py~~ — Help system demo (use `python -m Syncbot --help`)
- ~~organize_projects.py~~ — Project folder organization utility
- ~~rename_version_folders.py~~ — Version folder naming utility
- ~~verify_multihub_system.py~~ — System verification utility

---

## Next Steps

1. **Verify Paths on Each Device:**
   - Ensure local paths exist on each machine
   - Test NAS connectivity from Ghost and Pi

2. **Enable Devices as Needed:**
   - Keep Ghost enabled (primary)
   - Enable Falcon when ready for multi-device sync
   - Enable Pi for HAT development sync

3. **Create Initial NAS Backup:**
   ```bash
   python -m Syncbot backup --device nas --dry-run
   ```

4. **Monitor Sync Operations:**
   - Check `logFiles/` for sync details
   - Review `logFiles/SESSION.log` for current session info

5. **Test Multi-Device Sync:**
   Once both Ghost and Pi are enabled, perform test sync:
   ```bash
   python -m Syncbot sync --from ghost --to nas
   ```

---

## Troubleshooting

### Path Not Found Errors
- Verify network paths are accessible
- For NAS: test with `ping 192.168.0.2`
- For Pi: ensure SSH/NFS mounts are configured

### Missing Repositories
- Check `NODES` mappings in device config
- Verify repository folders exist at expected paths
- Run with `--verbose` for debugging

### Sync Conflicts
- NAS is hub and uses `newest_wins` conflict resolution
- Check `logFiles/ERROR.log` for details

---

## Related Documentation

- [Syncbot README.md](https://github.com/your-repo/blob/main/Applications/Syncbot/README.md)
- [Canonical Workspace Instructions](.github/copilot-instructions.md)
- [Pi Workspace Setup](/home/pi/.github/copilot-instructions.md)
- [tUilKit Utilities](../tUilKit/README.md)
