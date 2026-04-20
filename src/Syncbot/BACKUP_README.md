# tUilKit Project Backup Script

A simple Python script to backup repositories from your local development folder to OneDrive.

## Location

This script is located in the `Core/BackupUtility/` folder, outside of the tUilKit repository.

## Features

- **Interactive Selection**: Choose individual repositories or backup all repositories
- **Smart Versioning**: Automatically creates versioned backups when repositories already exist
- **Dry Run Mode**: Preview what would be backed up without making changes
- **Force Versioned**: Create versioned backups even for new repositories

## Usage

### Interactive Mode
```bash
cd Core/BackupUtility
python backup_projects.py
```

Or from the Projects root:
```bash
python BackupUtility/backup_projects.py
```

### Command Line Options
```bash
# Backup specific repository
python backup_projects.py --repository tUilKit

# Dry run to see what would happen
python backup_projects.py --dry-run --repository tUilKit

# Force versioned backup for all repositories
python backup_projects.py --force-versioned

# Combine options
python backup_projects.py --dry-run --force-versioned --repository MyProject
```

Or from the Projects root:
```bash
python BackupUtility/backup_projects.py --repository tUilKit
```

## How It Works

1. **New Repositories**: If a repository doesn't exist in the backup folder, it's copied directly
2. **Existing Repositories**: If a repository exists, the script reads the version from `GLOBAL_CONFIG.json` and creates a versioned backup like `repo_name_v1.2.3`
3. **Duplicate Versions**: If a versioned backup already exists, it appends a counter: `project_name_1.2.3_1`, `project_name_1.2.3_2`, etc.

## Paths

- **Source**: `./Core/`
- **Destination**: `./_backup/Core/`

## Requirements

- Python 3.6+
- Projects must have a `src/tUilKit/config/GLOBAL_CONFIG.json` file with a `VERSION` field for proper versioning

