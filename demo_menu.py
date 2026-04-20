#!/usr/bin/env python3
"""
demo_menu.py
Demonstration of Syncbot enhanced menu system.
Shows layout and features without requiring interaction.
"""
import sys
from pathlib import Path

src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from tUilKit import get_config_loader, get_logger

config_loader = get_config_loader()
LOG_FILES = config_loader.global_config.get("LOG_FILES", {})

if not LOG_FILES:
    LOG_FILES = {
        "SESSION": "logFiles/SESSION.log",
        "MASTER": "logFiles/MASTER.log",
        "ERROR": "logFiles/ERROR.log"
    }

def demo_main_menu():
    """Display demonstration of main menu"""
    logger = get_logger()
    
    print("\n" + "="*80)
    print("SYNCBOT ENHANCED MENU SYSTEM - DEMONSTRATION")
    print("="*80)
    print()
    
    print("Main Menu Display:")
    print("-" * 80)
    print()
    logger.apply_border(
        text="🔄 Syncbot - Device Backup & Sync Utility",
        pattern={"TOP": "═", "BOTTOM": "═", "LEFT": " ", "RIGHT": " "},
        total_length=70,
        border_rainbow=True,
        log_files=list(LOG_FILES.values())
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
    logger.colour_log("!list", "9", "!info", ". 🚪 Exit")
    
    print()
    print("-" * 80)
    print()
    print("Setup Review Output Example:")
    print("-" * 80)
    print()
    logger.apply_border(
        text="🔍 Setup Review & Configuration",
        pattern={"TOP": "═", "BOTTOM": "═", "LEFT": " ", "RIGHT": " "},
        total_length=70,
        border_rainbow=True,
        log_files=list(LOG_FILES.values())
    )
    print()
    logger.colour_log("!info", "📋 Project Information:")
    logger.colour_log("!list", "  Name:", "!thisfolder", "Syncbot Backup Utility")
    logger.colour_log("!list", "  Version:", "!thisfolder", "0.1.0")
    logger.colour_log("!list", "  Author:", "!thisfolder", "Daniel Austin")
    print()
    logger.colour_log("!info", "🖥️  Workspace Configuration:")
    logger.colour_log("!list", "  Base Path:", "!done", "✓ .")
    logger.colour_log("!list", "  Backup Destination:", "!done", "✓ ./_backup")
    logger.colour_log("!list", "  Description:", "!thisfolder", "Primary development workspace on Ghost desktop")
    print()
    logger.colour_log("!info", "💾 Backup Mode:")
    logger.colour_log("!list", "  Mode:", "!thisfolder", "project_folder")
    logger.colour_log("!list", "  Project Umbrellas:")
    logger.colour_log("!list", "    •", "!thisfolder", "Dev")
    logger.colour_log("!list", "    •", "!thisfolder", "Applications")
    logger.colour_log("!list", "    •", "!thisfolder", "Archive/_PORTS")
    
    print()
    print("-" * 80)
    print()
    print("HUB Review Output Example:")
    print("-" * 80)
    print()
    logger.apply_border(
        text="🗂️  Accessible HUBs Review",
        pattern={"TOP": "═", "BOTTOM": "═", "LEFT": " ", "RIGHT": " "},
        total_length=70,
        border_rainbow=True,
        log_files=list(LOG_FILES.values())
    )
    print()
    logger.colour_log("!info", "Current Device Hubs:")
    logger.colour_log("!done", "  ✓ Primary HUB")
    logger.colour_log("!list", "    Name:", "!thisfolder", "Primary Backup")
    logger.colour_log("!list", "    Path:", "!thisfolder", "./_backup")
    logger.colour_log("!list", "    Status:", "!done", "Accessible")
    logger.colour_log("!info", "    Contents (15 items):")
    logger.colour_log("!list", "      📁", "!thisfolder", "Dev")
    logger.colour_log("!list", "      📁", "!thisfolder", "Applications")
    logger.colour_log("!list", "      📁", "!thisfolder", "Archive")
    logger.colour_log("!list", "      📄", "!thisfolder", "README.md")
    logger.colour_log("!list", "      ... and 10 more items")
    
    print()
    print()
    print("="*80)
    print("KEY FEATURES")
    print("="*80)
    print()
    logger.colour_log("!done", "✓ Interactive menu system on startup")
    logger.colour_log("!done", "✓ Path validation with graceful error handling")
    logger.colour_log("!done", "✓ Configuration file editing")
    logger.colour_log("!done", "✓ HUB and project management")
    logger.colour_log("!done", "✓ Colour-coded output using tUilKit")
    logger.colour_log("!done", "✓ Backward compatible with command-line arguments")
    print()
    print()
    print("="*80)
    print("TO RUN SYNCBOT MENU")
    print("="*80)
    print()
    print("From Syncbot directory with venv activated:")
    print("  python .\\src\\Syncbot\\main.py")
    print()
    print("For more information, see docs/MENU_SYSTEM.md")
    print()

if __name__ == "__main__":
    demo_main_menu()
