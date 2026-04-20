# Syncbot Backup Mode Configuration

**Last Updated:** April 17, 2026  
**Version:** 0.3.1

---

## Overview

Syncbot now supports configurable workspace paths and two distinct backup modes:

1. **Repository Folder Mode** — Scans umbrella structure for individual repositories
2. **Single Folder Mode** — Backs up entire folder as one unit

---

## Configuration (Syncbot_CONFIG.json)

### New Configuration Sections

#### WORKSPACE Settings

```json
"WORKSPACE": {
    "base_path": ".",
    "backup_destination": "./_backup",
    "description": "Primary development workspace on Ghost desktop"
}
```

**Fields:**
- `base_path` — Root directory of your local workspace
- `backup_destination` — Target directory for backups
- `description` — Human-readable description of this workspace

#### BACKUP_MODE Settings

```json
"BACKUP_MODE": {
    "mode": "repository_folder",
    "description": "Backup mode: 'repository_folder' scans configured umbrella folders; 'single_folder' backs up one explicit folder target",
    "repository_folder_umbrellas": [
        "Dev",
        "Dev_Applications"
    ],
    "single_folder_target": null
}
```

**Fields:**
- `mode` — Active backup mode: `"repository_folder"` or `"single_folder"`
- `repository_folder_umbrellas` — List of umbrella directories to scan for repositories
- `single_folder_target` — Target folder for single_folder mode (null = requires --folder argument)

---

## Backup Modes Explained

### 1. Repository Folder Mode (Default)

**Use Case:** When you have multiple repositories organized in umbrella folders (Core/, Applications/, etc.)

**Behavior:**
- Scans specified umbrella directories for repositories
- Lists all repositories grouped by umbrella
- Allows selection of individual repositories or all repositories
- Each repository backed up independently

**Example Structure:**
```
dev_local/
├── Core/
│   ├── tUilKit/          ← Discovered as repository
│   ├── Syncbot/          ← Discovered as repository
│   └── H3l3n/            ← Discovered as repository
├── Applications/
│   └── crUPto/           ← Discovered as repository
└── Dev_Archive/
    └── _2_DEPORTED/
        └── BackupUtility/ ← Optional legacy discovery target
```

**Configuration:**
```json
{
    "mode": "repository_folder",
    "repository_folder_umbrellas": [
        "Dev",
        "Dev_Applications"
    ]
}
```

**Usage:**
```bash
# List all repositories and choose interactively
python src/Syncbot/main.py

# Backup a specific repository
python src/Syncbot/main.py --repository tUilKit

# Backup all repositories
python src/Syncbot/main.py --repository all

# Dry run (see what would happen)
python src/Syncbot/main.py --dry-run
```

---

### 2. Single Folder Mode

**Use Case:** When you want to backup an entire folder as one unit (not scanning for sub-projects)

**Behavior:**
- Backs up entire specified folder
- No sub-project scanning
- Treats folder as single backup unit

**Configuration:**
```json
{
    "mode": "single_folder",
    "single_folder_target": "git_forks"
}
```

**Usage:**
```bash
# Backup configured folder
python src/Syncbot/main.py

# Backup specific folder (override config)
python src/Syncbot/main.py --folder git_forks

# Force mode override
python src/Syncbot/main.py --mode single_folder --folder MyFolder
```

---

## Command-Line Arguments

### Global Arguments

| Argument | Description |
|----------|-------------|
| `--dry-run` | Show what would be backed up without copying |
| `--force-versioned` | Force versioned backup even for new repositories |
| `--mode {repository_folder,single_folder}` | Override backup mode from config |

### Repository Folder Mode Arguments

| Argument | Description |
|----------|-------------|
| `--repository NAME` | Specific repository to backup (by name or path) |

**Examples:**
```bash
# By repository name (searches all umbrellas)
python src/Syncbot/main.py --repository tUilKit

# By full path
python src/Syncbot/main.py --repository Core/tUilKit

# All repositories
python src/Syncbot/main.py --repository all
```

### Single Folder Mode Arguments

| Argument | Description |
|----------|-------------|
| `--folder PATH` | Specific folder to backup (relative to base_path) |

**Examples:**
```bash
# Backup specific folder
python src/Syncbot/main.py --mode single_folder --folder git_forks

# With versioning
python src/Syncbot/main.py --mode single_folder --folder MyData --force-versioned
```

---

## Versioned Backups

### When Destination Repository Already Exists

If a repository already exists at the destination, Syncbot creates a **versioned backup** instead of overwriting:

**Naming Format:** `{RepositoryName}_v{Version}`

**Example:**
- Source: `Core/tUilKit/` (version 0.7.1)
- Destination already has: `Core/tUilKit/`
- Creates: `Core/tUilKit_v0.7.1/`

### Handling Existing Versioned Backups

If versioned backup already exists, Syncbot renames the old one with timestamp:

**Format:** `{RepositoryName}_v{Version}_old_{YYYYMMDD_HHMMSS}`

**Example:**
- Existing: `Core/tUilKit_v0.7.1/`
- Renames to: `Core/tUilKit_v0.7.1_old_20260309_122630/`
- Creates new: `Core/tUilKit_v0.7.1/`

### Force Versioned Mode

Use `--force-versioned` to always create versioned backups, even for new repositories:

```bash
python src/Syncbot/main.py --force-versioned --repository tUilKit
```

**Result:** Even if `tUilKit` doesn't exist at destination, creates `tUilKit_v0.7.1/` instead of `tUilKit/`

---

## Version Detection

Syncbot extracts version numbers from `pyproject.toml`:

**Supported Formats:**

1. **PEP 621 (setuptools):**
   ```toml
   [project]
   version = "0.7.1"
   ```

2. **Poetry:**
   ```toml
   [tool.poetry]
   version = "0.7.1"
   ```

If no version found, uses `"unknown"` as version identifier.

---

## Example Workflows

### Workflow 1: Daily Repository Backup

**Goal:** Back up all Dev repositories to OneDrive

```bash
# 1. Review what will be backed up
python src/Syncbot/main.py --dry-run

# 2. Select "all" when prompted or use:
python src/Syncbot/main.py --repository all

# 3. Check backup destination
# ./_backup/
```

### Workflow 2: Before Major Refactor

**Goal:** Create versioned repository snapshot before risky changes

```bash
# Force versioned backup for current repository
python src/Syncbot/main.py --force-versioned --repository tUilKit

# Result: Creates tUilKit_v0.7.1 even if tUilKit doesn't exist yet
```

### Workflow 3: Archive Old Projects

**Goal:** Back up git_forks folder as single unit

```bash
# Switch to single folder mode
python src/Syncbot/main.py --mode single_folder --folder git_forks

# Or configure in Syncbot_CONFIG.json:
# "mode": "single_folder",
# "single_folder_target": "git_forks"
```

### Workflow 4: Backup Specific Repository

**Goal:** Quick backup of one repository after significant work

```bash
# Interactive selection
python src/Syncbot/main.py
# Then choose repository number from list

# Or direct:
python src/Syncbot/main.py --repository crUPto
```

---

## Troubleshooting

### "No repositories found in umbrella structure!"

**Cause:** Umbrella directories don't exist or are empty

**Solutions:**
1. Check `base_path` in Syncbot_CONFIG.json
2. Verify umbrella directories exist:
   ```
   .\Dev\
    .\Dev_Applications\
   ```
3. Ensure repositories are subdirectories of umbrellas (not hidden with `.` prefix)

### "Error: Path {path} does not exist"

**Cause:** Configured workspace path is incorrect

**Solutions:**
1. Update `WORKSPACE.base_path` in Syncbot_CONFIG.json
2. Ensure path uses forward slashes: `C:/Repository/...`
3. Check drive letter and folder spelling

### "Error: Source repository {path} does not exist"

**Cause:** Selected repository not found at expected location

**Solutions:**
1. Verify repository exists in umbrella folder
2. Check for typos in repository name
3. Use `--dry-run` to see what Syncbot detects

### Repositories Not Discovered

**Cause:** Repositories filtered out by naming rules

**Solutions:**
- Syncbot ignores directories starting with `.` (hidden) or `_` (archives)
- Include additional archive folders explicitly via `repository_folder_umbrellas` when needed
- Rename repository folders to not start with special characters

---

## Multi-Device Configuration

Each device can have different workspace paths configured in Syncbot_CONFIG.json:

### Ghost Desktop (Primary)
```json
"WORKSPACE": {
    "base_path": ".",
    "backup_destination": "./_backup"
}
```

### Falcon Laptop (Secondary)
```json
"WORKSPACE": {
    "base_path": "D:/Core/dev_local",
    "backup_destination": "./_backup"
}
```

### Raspberry Pi
```json
"WORKSPACE": {
    "base_path": "/home/pi/dev_pi",
    "backup_destination": "\\\\192.168.0.2\\devsrc\\dev_pi"
}
```

**Note:** Each device's Syncbot_CONFIG.json should be customized for local paths.

---

## Migration from Old Configuration

### Old Behavior (Hardcoded)
- Always looked in `./Projects`
- Single flat folder structure
- No umbrella support

### New Behavior (Configurable)
- Reads from Syncbot_CONFIG.json
- Supports umbrella structure (Core/, Applications/)
- Dual-mode: repository_folder or single_folder

### Migration Steps

1. **Update Syncbot_CONFIG.json** with workspace and backup_mode sections
2. **Test with dry-run:**
   ```bash
   python src/Syncbot/main.py --dry-run
   ```
3. **Verify repositories detected correctly**
4. **Run actual backup after confirmation**

---

## Related Documentation

- [Syncbot Configuration Setup](CONFIG_SETUP.md)
- [Device Quick Reference](DEVICE_QUICK_REFERENCE.md)
- [Workspace Instructions](../../.github/copilot-instructions.md)

---

## Change Log

### March 9, 2026 - Configuration Enhancement

**Added:**
- ✓ Configurable workspace paths in Syncbot_CONFIG.json
- ✓ Two backup modes: repository_folder and single_folder
- ✓ Umbrella structure support (Core/, Applications/)
- ✓ Command-line mode override (--mode, --folder)
- ✓ Improved repository discovery and listing

**Changed:**
- ✗ Removed hardcoded workspace paths
- ✗ Removed flat Projects/ folder assumption

**Migration Required:** Update Syncbot_CONFIG.json before next use
