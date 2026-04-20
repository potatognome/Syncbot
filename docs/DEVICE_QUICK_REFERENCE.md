# Syncbot Device Configuration - Quick Reference

**Last Updated:** 2026-03-11

## Device Status Summary

| Device | Hostname | Role | Status | Projects | Local Path |
|--------|----------|------|--------|----------|-----------|
| **Ghost** | GHOST | Primary | ✓ **ENABLED** | tUilKit, H3l3n, Syncbot, crUPto | `.` |
| **Falcon** | FALCON | Secondary | ✗ Disabled | tUilKit, H3l3n, Syncbot, crUPto, _PORTS | `D:/Core/dev_local` |
| **Pi** | johnnyfive | Secondary | ✗ Disabled | tUilKit, H3l3n, colour_lab | `/home/pi/dev_pi` |
| **NAS** | nas.local | **HUB** | ✓ **ENABLED** | All projects + _PORTS | `\\192.168.0.2\devsrc` |

## Key Changes Made

### Device Configuration Updates

**File:** `Applications/Syncbot/config/devices.d/*.yaml`

#### 1. Ghost Desktop
- ✓ Projects updated to reference correct umbrella structure
- ✓ Archive now includes `_PORTS/colour_lab_retrofit`

#### 2. Falcon Laptop
- ✓ Archive projects expanded to include all `_PORTS`
- ✓ Remains disabled until needed for multi-device development

#### 3. Raspberry Pi (**MAJOR UPDATE**)
- ✓ `local_path`: `/home/pi/dev` → `/home/pi/dev_pi`
- ✓ `hub_path`: `/mnt/onedrive/...` → `\\192.168.0.2\devsrc\dev_pi`
- ✓ Projects restructured for Pi-specific development:
  - Removed: Syncbot, crUPto (desktop-only)
  - Added: `hat_dev.colour_lab` (HAT testing & labs)
  - Kept: tUilKit, H3l3n
- ✓ Added excluded_folders for HAT development:
  - `.pytest_cache`, `.git`, `__pycache__`, `.vscode`, `*.egg-info`, `venv`

#### 4. NAS Storage Server (**MAJOR UPDATE**)
- ✓ `local_path`/`hub_path`: `\devsrc\dev_pi` → `\devsrc` (root level)
- ✓ Projects synchronized to new umbrella structure
- ✓ Archive updated to `_PORTS` only (active staging)
- ✓ excluded_repositories expanded:
  - Added: `*.whl`, `*.egg` (build artifacts)
- ✓ excluded_folders restructured:
  - Changed from prefix matching (`_0_`, `_1_`) to explicit folder names
  - Added: `logFiles`, `outputFiles`
  - Example:
    ```yaml
    # OLD:  - _0_  (matches _0_anything)
    # NEW:  - "_0_BACKUP_ARCHIVE"  (specific folder)
    ```

### Script Cleanup

**Location:** `Applications/Syncbot/` root directory

**Removed (Development Utilities):**
- ~~demo_help.py~~ — Use `python -m Syncbot --help` instead
- ~~organize_projects.py~~ — Manual organization tool
- ~~rename_version_folders.py~~ — Batch folder renaming utility
- ~~verify_multihub_system.py~~ — System verification tool

**Retained (Deployment):**
- `deploy.bat` — Windows deployment script
- `deploy_to_nas.py` — NAS deployment automation

## Network Configuration

### NAS Hub Setup

**Network:** Local network (192.168.0.x)
**IP:** 192.168.0.2
**Share Root:** `\\192.168.0.2\devsrc`

**Expected Directory Structure on NAS:**
```
\\192.168.0.2\devsrc\
├── Core/
│   ├── tUilKit/
│   ├── Syncbot/
│   └── H3l3n/
├── Applications/
│   └── crUPto/
├── Dev_Archive/
│   ├── _2_DEPORTED/
│   ├── _0_BACKUP_ARCHIVE/
│   └── ... (other archive folders)
└── dev_pi/            (Pi-specific sync folder)
    ├── hat_dev/
    │   └── colour_lab/
    └── Projects/
```

## Sync Flow Overview

```
Ghost (Primary) ←→ NAS Hub ←→ Pi (HAT Development)
     ↓
  Falcon (Secondary - when enabled)
```

**Hub Role:** NAS stores all projects and resolves conflicts (newest-wins)

**Sync Triggers:**
- Manual: `python -m Syncbot sync`
- Scheduled: (configure via device config if needed)
- On-demand: Per-project or per-device sync

## Configuration Validation

To verify device configurations are correct:

```bash
# List all configured devices
python -m Syncbot devices --list

# Validate device paths
python -m Syncbot devices --validate

# Show active device (auto-detected)
python -m Syncbot devices --current

# Test sync paths (dry-run)
python -m Syncbot sync --device nas --dry-run
```

## Common Reference Points

### Pi Projects Sync Path
- **Source (NAS):** `\\192.168.0.2\devsrc\dev_pi\hat_dev\colour_lab`
- **Destination (Pi):** `/home/pi/dev_pi/hat_dev/colour_lab`

### Archive Staging
- **NAS Path:** `\\192.168.0.2\devsrc\Archive\_PORTS`
- **Ghost Path:** `.\Archive\_PORTS`
- **Purpose:** Staging area for project porting and retrofitting

### Excluded Build/Cache Artifacts
- Across all devices: `.git`, `__pycache__`, `.vscode`
- Pi specific: `*.egg-info`, `venv`
- NAS wide: `build`, `dist`, `node_modules`

## Enabling Devices for Sync

### To Enable Falcon (Windows Secondary)
```yaml
# File: config/devices.d/falcon.yaml
enabled: true  # Change from: false
```

### To Enable Pi (HAT Development)
```yaml
# File: config/devices.d/pi.yaml
enabled: true  # Change from: false
```

Then on Pi:
```bash
# Verify config is correct
python -m Syncbot devices --current

# First sync from NAS to Pi
python -m Syncbot sync --from nas --to johnnyfive
```

## Troubleshooting Checklist

### NAS Connection Issues
- [ ] Test: `ping 192.168.0.2`
- [ ] Windows: verify SMB/CIFS credentials
- [ ] Pi: check NFS mount or Samba config
- [ ] Check firewall rules on NAS

### Path Not Found
- [ ] Verify folder exists: `\\192.168.0.2\devsrc`
- [ ] Check permissions: can read/write?
- [ ] On Pi: verify `/home/pi/dev_pi` exists or create with `mkdir -p`

### Missing Repositories in Sync
- [ ] Review `NODES` mappings in device config
- [ ] Repositories must exist on both source and destination
- [ ] Check `logFiles/SESSION.log` for sync details

### Sync Conflicts
- [ ] NAS uses `newest_wins` — newest file overwrites
- [ ] Check timestamps on conflicting files
- [ ] Review `logFiles/ERROR.log` for details

---

**Last Updated:** March 9, 2026  
**Syncbot Version:** 0.1.0  
**Project Structure:** Umbrella v2.0+
