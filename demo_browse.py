"""
demo_browse.py
Quick demo script to test the new BROWSE functionality in Syncbot.
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from Syncbot.proc.menu_operations import prompt_for_path, browse_for_path

def main():
    """Demo the BROWSE functionality."""
    print("\n" + "="*70)
    print("Syncbot BROWSE Functionality Demo")
    print("="*70 + "\n")
    
    print("This demo showcases the new PATH BROWSE feature.")
    print("You can now browse directories interactively when adding HUBs or projects.\n")
    
    # Demo 1: Direct browse
    print("Demo 1: Direct CLI Browser")
    print("-" * 70)
    result = browse_for_path("Demo: Select any directory", start_path=str(Path.cwd()))
    if result:
        print(f"\n✅ You selected: {result}\n")
    else:
        print("\n❌ Browse cancelled\n")
    
    # Demo 2: Prompt with browse option
    print("\nDemo 2: Integrated Prompt (Manual or Browse)")
    print("-" * 70)
    result = prompt_for_path("Demo: Enter or browse for a path", allow_browse=True)
    if result:
        print(f"\n✅ You entered/selected: {result}\n")
    else:
        print("\n❌ Cancelled\n")
    
    print("="*70)
    print("Demo complete! This functionality is now integrated into:")
    print("  - First-Time Setup Wizard (option 9 in main menu)")
    print("  - Add HUB (option 4 in main menu)")
    print("  - Add Project (option 5 in main menu)")
    print("="*70 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.\n")
        sys.exit(0)
