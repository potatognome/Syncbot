# Syncbot Enhanced Menu System

**Last Updated:** 2026-03-11

## Overview

Syncbot now features an interactive CLI menu system that launches when running `main.py` with no arguments. This menu provides easy access to setup review, configuration management, and HUB/repository management features.

## Quick Start

### Launch the Menu
```powershell
# From Syncbot root with venv activated
python .\src\Syncbot\main.py

# Or run directly
cd .\src
python Syncbot/main.py
```

### Menu Structure

When you run `main.py` with no arguments, you'll see:

```
🔄 Syncbot - Device Backup & Sync Utility
════════════════════════════════════════════════

📋 Main Menu:
1. 🔍 Review Setup & Configuration
2. 🗂️  Review Accessible HUBs
3. ⚙️  Edit Configuration Files
4. ➕ Add New HUB Repository
5. 📦 Add New Project/Folder Node
6. 🔧 Configure HUB or Project/Folder
7. 💾 Run Backup
8. ❓ Help
9. 🚪 Exit
```

## Features

### 1. 🔍 Review Setup & Configuration

Displays your current device and workspace configuration including:
- **Project Information** - Name, version, author
- **Workspace Configuration** - Base path and backup destination with validation
- **Backup Mode** - Current mode (repository_folder or single_folder)
- **Log Files Location** - All configured log file paths

Path validation shows:
- ✓ Green if path is accessible
- ✗ Red if path is invalid or inaccessible

### 2. 🗂️ Review Accessible HUBs

Shows all accessible backup destinations (HUBs) including:
- Primary HUB path and status
- HUB contents preview (first 10 items)
- Multi-HUB configuration from device configs
- Device-specific preferred HUBs

### 3. ⚙️ Edit Configuration Files

Manage all Syncbot configuration files:

**Available Config Files:**
- `Syncbot_CONFIG.json` - Main settings
- `COLOURS.json` - Colour schemes (integrates with tUilKit colour editor)
- `BORDER_PATTERNS.json` - Border styles
- Device configurations (YAML files in `config/devices.d/`)

**Options for Each File:**
- View content in terminal
- Open in text editor (notepad on Windows)
- Return to menu

### 4. ➕ Add New HUB Repository

Add a new backup destination:
1. Enter HUB name (e.g., "NAS Storage")
2. Enter HUB path (local or network)
3. Path is validated; warnings shown if inaccessible
4. Can force creation even if path doesn't exist yet
5. Configuration summary displayed

**Notes:**
- New HUBs must be configured in device config
- Configure which projects sync to this HUB

### 5. 📦 Add New Project/Folder Node

Add a new repository or folder to backup:
1. Enter repository name
2. Enter repository path (local path)
3. Path is validated; warnings shown if inaccessible
4. Can force creation even if path doesn't exist yet
5. Configuration summary displayed

**Next Steps:**
- Review device configuration to enable this repository
- Configure backup destination HUB
- Run backup to sync

### 6. 🔧 Configure HUB or Project/Folder

Manage existing configurations:

**For HUB Configuration:**
- Edit `Syncbot_CONFIG.json`
- Key settings:
  - `WORKSPACE.backup_destination` - HUB location path
  - `BACKUP_MODE.mode` - 'repository_folder' or 'single_folder'

**For Project/Folder Configuration:**
- Edit device configuration file in `config/devices.d/`
- Modify `NODES`/`HUBS` mappings
- Choose which repositories to backup from each umbrella

### 7. 💾 Run Backup

Execute the backup process with current settings.
Delegates to the original `backup_projects.py` function.

### 8. ❓ Help

Display help information covering:
- Syncbot overview
- Key concepts (HUB, Device, Repository, Config)
- Common tasks with step-by-step guidance
- Configuration file locations

### 9. 🚪 Exit

Gracefully exit Syncbot.

## Error Handling

### Path Validation

All file path operations include graceful error handling:

```
⚠️  Warning: Path validation failed
  Error message displayed
  You can still add this HUB/Repository, but verify it exists before backing up.
```

Users can choose to:
- Proceed anyway (creates config even if path doesn't exist)
- Cancel and return to menu

### Invalid Input

- Invalid menu choices show error message with valid options
- Invalid path selections close and return to submenu
- Keyboard interrupt (Ctrl+C) handled gracefully

### File Access

If configuration files can't be read:
- Error message displayed with reason
- Menu continues functioning
- Other config files remain accessible

## Running with Arguments (Backward Compatibility)

If you run `main.py` with arguments, it delegates to the original backup function:

```powershell
python .\src\Syncbot\main.py backup  # Runs backup directly
python .\src\Syncbot\main.py --help  # Shows help
```

This ensures backward compatibility with existing scripts and automation.

## Configuration Examples

### Viewing Device Configuration

From menu, select:
1. Option 3: Edit Configuration Files
2. Option 4: Edit Device Configuration
3. Select device (e.g., "ghost")
4. Option 1: View content

Sample device config (`ghost.yaml`):
```yaml
name: Ghost Desktop
role: primary
hostname: GHOST
enabled: true
HUBS:
  nas_primary:
    name: NAS Primary
    path: \\192.168.0.2\devsrc
    repository_role: HUB
NODES:
  syncbot_repo:
    name: Syncbot
    path: ./Applications/Syncbot
    repository_role: NODE
    connected_hub_IDs: [nas_primary]
```

### Adding a Repository

From menu, select:
1. Option 5: Add New Project/Folder Node
2. Enter repository name: "My Project"
3. Enter path: "C:/Repository/my_project"
4. Confirm creation

Then configure `NODES`/`HUBS` mappings in device YAML to enable backup.

## Colour Support

Syncbot uses semantic colour codes from tUilKit:
- `!info` - Blue (informational)
- `!done` - Green (success)
- `!error` - Red (errors)
- `!warn` - Yellow (warnings)
- `!list` - Cyan (list items)
- `!thisfolder` - Magenta (file/folder names)

All output files support colour logging with the ability to disable colours for piping or CI/CD.

## Log Files

All menu operations are logged to:
- `logFiles/SESSION.log` - Current session log
- `logFiles/MASTER.log` - Master log archive
- `logFiles/ERROR.log` - Error log

View logs from the file system or use the status indicators in the menu output.

## Tips & Tricks

1. **Review Setup First**: Always start with "Review Setup & Configuration" after major changes
2. **Check HUBs**: Use "Review Accessible HUBs" to verify network paths before backup
3. **Validate Paths**: The menu shows validation status (✓/✗) for all configured paths
4. **Edit Colours**: Use tUilKit's colour editor for `COLOURS.json` from the Config Files menu
5. **Backup Regularly**: Use option 7 to test configuration before running automated backups

## Troubleshooting

### "Path is not valid"
- Verify the path exists and is accessible
- Check network connectivity for network paths
- Retry with a valid local path

### "File not found"
- Configuration file may have been deleted
- Restore from backup if available
- Recreate missing configuration

### "Module not found"
- Ensure tUilKit is installed: `pip install -e ./Core/tUilKit`
- Verify Python path includes Syncbot/src

### Menu Freezes
- Press Ctrl+C to interrupt
- Returns to main menu cleanly

## Development Notes

- Menu system implemented in `src/Syncbot/main.py`
- Menu operations in `src/Syncbot/proc/menu_operations.py`
- Integrates with tUilKit for logging and colour management
- All menu functions include path validation and error handling
- Backward compatible with existing backup functionality

## See Also

- [QUICK_START.md](./QUICK_START.md) - Getting started with Syncbot
- [CONFIG_SETUP.md](./CONFIG_SETUP.md) - Configuration setup guide
- [DEVICE_QUICK_REFERENCE.md](./DEVICE_QUICK_REFERENCE.md) - Device configuration reference
