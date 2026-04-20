"""
main.py
Main entry point for Syncbot.
Features interactive menu system for setup review, configuration, and backup management.
"""

import sys
import os
from pathlib import Path
import json
import yaml

if __name__ == "__main__" and __package__ is None:
    src_path = Path(__file__).resolve().parent.parent
    if src_path not in sys.path:
        sys.path.insert(0, str(src_path))
    from Syncbot.bootstrap import bootstrap_syncbot_config_loader
else:
    from .bootstrap import bootstrap_syncbot_config_loader


bootstrap_syncbot_config_loader(anchor_file=__file__)

# Handle both package and direct script execution
if __name__ == "__main__" and __package__ is None:
    # Direct script execution - add src/ to path so package can be imported
    src_path = Path(__file__).resolve().parent.parent
    if src_path not in sys.path:
        sys.path.insert(0, str(src_path))
    from Syncbot.proc.backup_projects import main as run_backup
    from Syncbot.proc.menu_operations import (
        review_setup, review_hubs, edit_config_files,
        add_hub, add_project, configure_hub_or_project,
        initialize_device_setup_wizard, run_startup_configuration_checks
    )
else:
    # Package execution - use relative import
    from .proc.backup_projects import main as run_backup
    from .proc.menu_operations import (
        review_setup, review_hubs, edit_config_files,
        add_hub, add_project, configure_hub_or_project,
        initialize_device_setup_wizard, run_startup_configuration_checks
    )

from tUilKit import get_logger, get_config_loader
config_loader = get_config_loader()

LOG_FILES = config_loader.global_config.get("LOG_FILES", {})
MENU_BORDER = {"TOP": "<>", "BOTTOM": "<>", "LEFT": "||", "RIGHT": "||"}


def apply_menu_header(logger, text, total_length=70, border_rainbow=True):
    """Render menu headers using V4l1d8r menu border style."""
    logger.apply_border(
        text=text,
        pattern=MENU_BORDER,
        total_length=total_length,
        border_rainbow=border_rainbow,
        log_files=list(LOG_FILES.values())
    )


def describe_visual_config_paths(global_config):
    """Describe active COLOURS/BORDER config location based on shared config."""
    paths = global_config.get("PATHS", {})
    shared = global_config.get("SHARED_CONFIG", {})
    config_root = str(paths.get("CONFIG", "config/")).replace("\\", "/")
    if not config_root.endswith("/"):
        config_root += "/"

    if shared.get("ENABLED"):
        shared_path = str(shared.get("PATH", "GLOBAL_SHARED.d/")).replace("\\", "/")
        if shared_path.startswith("./"):
            shared_path = shared_path[2:]
        shared_path = shared_path.strip("/") + "/"
        return f"{config_root}{shared_path}"

    return config_root

def main_menu():
    """Display main menu and handle user selection"""
    logger = get_logger()
    config_loader = get_config_loader()
    
    while True:
        print()
        apply_menu_header(
            logger,
            text="🔄 Syncbot - Device Backup & Sync Utility",
            border_rainbow=True,
        )
        
        print()
        logger.colour_log("!info", "📋 Main Menu:")
        logger.colour_log("!list", "1", "!info", ". 🔍 Review Setup & Configuration")
        logger.colour_log("!list", "2", "!info", ". 🗂️  Review Accessible HUBs")
        logger.colour_log("!list", "3", "!info", ". ⚙️  Edit Configuration Files")
        logger.colour_log("!list", "4", "!info", ". ➕ Add New HUB Repository")
        logger.colour_log("!list", "5", "!info", ". 📦 Add New Project/Folder Node")
        logger.colour_log("!list", "6", "!info", ". 🔧 Configure HUB or Project/Folder")
        logger.colour_log("!list", "7", "!info", ". 💾 Run Backup")
        logger.colour_log("!list", "8", "!info", ". ❓ Help")
        logger.colour_log("!list", "9", "!info", ". 🧭 First-Time Setup Wizard")
        logger.colour_log("!list", "0", "!info", ". 🚪 Exit")
        
        choice = input("\nSelect option (0-9): ").strip()
        
        if choice == '1':
            print()
            logger.colour_log("!info", "🔍 Loading Setup Review...")
            review_setup()
        elif choice == '2':
            print()
            logger.colour_log("!info", "🗂️  Loading HUB Review...")
            review_hubs()
        elif choice == '3':
            print()
            logger.colour_log("!info", "⚙️  Opening Configuration Editor...")
            edit_config_files()
        elif choice == '4':
            print()
            logger.colour_log("!info", "➕ Adding New HUB Repository...")
            add_hub()
        elif choice == '5':
            print()
            logger.colour_log("!info", "📦 Adding New Project/Folder Node...")
            add_project()
        elif choice == '6':
            print()
            logger.colour_log("!info", "🔧 Configuring HUB or Project...")
            configure_hub_or_project()
        elif choice == '7':
            print()
            logger.colour_log("!info", "💾 Starting Backup Process...")
            print()
            run_backup()
        elif choice == '8':
            print()
            show_help()
        elif choice == '9':
            print()
            logger.colour_log("!info", "🧭 Opening first-time setup wizard...")
            initialize_device_setup_wizard()
        elif choice == '0':
            print()
            logger.colour_log("!done", "👋 Goodbye!")
            break
        else:
            print()
            logger.colour_log("!error", "❌ Invalid choice. Please select 0-9.")

def show_help():
    """Display help information"""
    logger = get_logger()
    
    print()
    apply_menu_header(logger, text="❓ Help & Information", border_rainbow=False)
    print()
    
    logger.colour_log("!info", "📖 Syncbot Overview:")
    logger.colour_log("!info", "  Syncbot is a device-centric backup and synchronization utility.")
    logger.colour_log("!info", "  It manages repository nodes across multiple devices and HUBs.")
    
    print()
    logger.colour_log("!info", "🎯 Key Concepts:")
    logger.colour_log("!info", "  • HUB: Central repository location (local or network)")
    logger.colour_log("!info", "  • Device: Computer/device running Syncbot")
    logger.colour_log("!info", "  • Repository Node: Code repository or folder to sync")
    logger.colour_log("!info", "  • Config: YAML/JSON files defining devices, HUBS, and NODES")
    
    print()
    logger.colour_log("!info", "💡 Common Tasks:")
    logger.colour_log("!info", "  1. Review Setup to see current device & repository configuration")
    logger.colour_log("!info", "  2. Review HUBs to check accessible backup destinations")
    logger.colour_log("!info", "  3. Edit Configs to adjust colour, borders, or settings")
    logger.colour_log("!info", "  4. Add HUB to register a new backup destination")
    logger.colour_log("!info", "  5. Add Repository Node to register what to sync")
    logger.colour_log("!info", "  6. Run Backup to execute repository sync")
    
    print()
    global_config = config_loader.global_config
    visual_config_path = describe_visual_config_paths(global_config)
    logger.colour_log("!info", f"📁 Configuration Files Located in: {visual_config_path}")
    logger.colour_log("!info", "  • Syncbot_CONFIG.json: Main settings")
    logger.colour_log("!info", "  • COLOURS.json: Colour schemes for output")
    logger.colour_log("!info", "  • BORDER_PATTERNS.json: Border styles")
    logger.colour_log("!info", "  • devices.d/: Individual device configurations (YAML)")
    
    print()
    input("Press ENTER to return to main menu...")

def main():
    """Main entry point"""
    logger = get_logger()
    
    try:
        logger.colour_log("!info", "Syncbot", "!done", "initialized", log_files=list(LOG_FILES.values()))
        
        # Parse command line arguments
        if len(sys.argv) > 1:
            # If arguments provided, use original backup behavior
            logger.colour_log("!info", "Running with arguments (direct backup mode)...")
            print()
            run_backup()
        else:
            # No arguments - show interactive menu
            run_startup_configuration_checks()
            main_menu()
    except KeyboardInterrupt:
        print()
        logger.colour_log("!warn", "⚠️ Operation cancelled by user", log_files=list(LOG_FILES.values()))
    except Exception as e:
        logger.colour_log("!error", f"Fatal error: {e}", log_files=list(LOG_FILES.values()))
        sys.exit(1)

if __name__ == "__main__":
    main()
