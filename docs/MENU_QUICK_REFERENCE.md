# Syncbot Menu System - Quick Reference

**Last Updated:** 2026-04-17
**Version:** 0.3.1

## Launch Menu

```powershell
cd Dev\Syncbot
python .\src\Syncbot\main.py
```

No arguments = interactive menu mode  
With arguments = direct backup mode (backward compatible)

## Main Menu Options

| Option | Feature | Use Case |
|--------|---------|----------|
| **1** | 🔍 Review Setup | Verify workspace, paths, backup mode configuration |
| **2** | 🗂️ Review HUBs | Check accessible backup destinations, view HUB contents |
| **3** | ⚙️ Edit Config | Edit JSON/YAML configuration files, view settings |
| **4** | ➕ Add HUB | Register new backup repository (local or network) |
| **5** | 📦 Add Project | Add new project/folder node for backup |
| **6** | 🔧 Configure | Modify HUB or Project settings in config files |
| **7** | 💾 Backup | Execute backup process with current settings |
| **8** | ❓ Help | View help and documentation |
| **9** | 🧭 Setup Wizard | Run first-time setup wizard |
| **0** | 🚪 Exit | Gracefully exit Syncbot |

## Key Features

✅ **Interactive Menu** - User-friendly CLI interface  
✅ **Path Validation** - Checks path accessibility, shows ✓/✗ status  
✅ **Graceful Errors** - Handles invalid paths with warnings, allows override  
✅ **Config Management** - View and edit all configuration files  
✅ **HUB Operations** - Add, review, and manage backup destinations  
✅ **Project Nodes** - Add, configure project/folder backups  
✅ **Colour Support** - Semantic colour coding via tUilKit  
✅ **Logging** - All operations logged to SESSION/MASTER/ERROR logs  
✅ **Help System** - Built-in help with usage guides  
✅ **Backward Compatible** - Still works with command-line arguments

## Configuration Files

Located in `config/` directory:

| File | Purpose | Editing |
|------|---------|---------|
| `Syncbot_CONFIG.json` | Main settings, workspace, backup mode | View/Edit from menu option 3 |
| `COLOURS.json` | Colour schemes | Use tUilKit colour editor |
| `BORDER_PATTERNS.json` | Border styles | View/Edit from menu option 3 |
| `devices.d/*.yaml` | Device configurations | Edit from menu option 3.4 |

## Typical Workflows

### Verify Setup
```
1. Run main.py
2. Select option 1: Review Setup & Configuration
3. Verify paths show ✓ (accessible)
4. Review backup mode and umbrellas
5. Press ENTER to return
```

### Check Backup Destination
```
1. Run main.py
2. Select option 2: Review Accessible HUBs
3. View HUB path and contents
4. Verify status shows "Accessible"
5. Press ENTER to return
```

### Add New Backup Location
```
1. Run main.py
2. Select option 4: Add New HUB Repository
3. Enter HUB name (descriptive)
4. Enter HUB path (local or network)
5. Confirm path validation result
6. Review summary
7. Edit device config to enable it
```

### Add Repository/Folder
```
1. Run main.py
2. Select option 5: Add New Project/Folder Node
3. Enter repository name
4. Enter repository path (local)
5. Confirm path validation result
6. Edit device config to enable it in `NODES`
```

### Run Backup
```
1. Run main.py
2. Select option 7: Run Backup
3. Backup executes with current settings
4. Monitor progress
5. Return to menu when complete
```

## Path Validation Status

| Status | Meaning | Action |
|--------|---------|--------|
| ✓ Green | Path exists & accessible | Safe to use |
| ✗ Red | Path missing/inaccessible | Verify before backup |
| ⚠️ Yellow | Path doesn't exist but config created | Will fail at backup - fix path |

## Error Handling

**Invalid Menu Choice**
```
❌ Invalid choice. Please select 1-9.
```
→ Select valid option from 0-9

**Path Not Found**
```
❌ Path does not exist: C:/nonexistent/path
You can still add this node, but verify it exists before backing up.
Create anyway? (y/N):
```
→ Select 'y' to continue anyway, 'N' to cancel

**File Access Error**
```
❌ Could not open file: Permission denied
```
→ May need admin rights or file not accessible

## Tips

1. **Always review setup first** after making config changes
2. **Check HUB accessibility** before running backup operations
3. **Use path validation** to catch issues early
4. **Edit colours/borders** from menu for consistent theme
5. **Test with review options** before running backup
6. **Check log files** in `logFiles/` for detailed operation logs

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Menu doesn't appear | Ensure no arguments: `python .\src\Syncbot\main.py` |
| Path shows ✗ | Verify network connectivity, path permissions |
| Config won't open | Check file permissions, drive access |
| Menu freezes | Press Ctrl+C to interrupt (returns to menu) |
| tUilKit not found | Install: `pip install -e .\Dev\tUilKit` |

## Demo

View menu demonstration without interaction:
```powershell
python .\demo_menu.py
```

Shows colour layout and example output.

## Documentation

For detailed information:
- `docs/MENU_SYSTEM.md` - Complete menu documentation
- `docs/QUICK_START.md` - Getting started
- `docs/CONFIG_SETUP.md` - Configuration guide
- `docs/DEVICE_QUICK_REFERENCE.md` - Device config reference
