"""
menu_operations.py
Menu operation handlers for Syncbot interactive CLI.
Provides functions for setup review, HUB management, config editing, and project configuration.
"""

import sys
import os
import yaml
import subprocess
from pathlib import Path
from datetime import datetime
import socket

if __package__:
    from ..bootstrap import bootstrap_syncbot_config_loader
else:
    src_path = Path(__file__).resolve().parents[2]
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))
    from Syncbot.bootstrap import bootstrap_syncbot_config_loader

bootstrap_syncbot_config_loader(anchor_file=__file__)

from tUilKit import get_logger, get_config_loader, get_colour_manager

logger = get_logger()
config_loader = get_config_loader()
colour_manager = get_colour_manager()

LOG_FILES = config_loader.global_config.get("LOG_FILES", {})
MENU_BORDER = {"TOP": "<>", "BOTTOM": "<>", "LEFT": "||", "RIGHT": "||"}

def apply_menu_header(text, total_length=70, border_rainbow=True):
    """Render menu headers using the V4l1d8r border style."""
    logger.apply_border(
        text=text,
        pattern=MENU_BORDER,
        total_length=total_length,
        border_rainbow=border_rainbow,
        log_files=list(LOG_FILES.values())
    )

def _clean_rel_path(path_value):
    """Normalize a configured relative path for safe path joining."""
    if path_value is None:
        return ""
    cleaned = str(path_value).replace("\\", "/").strip()
    while cleaned.startswith("./"):
        cleaned = cleaned[2:]
    return cleaned.strip("/")

def resolve_menu_config_paths(global_config):
    """Resolve menu config file paths from PATHS.CONFIG and SHARED_CONFIG."""
    project_root = get_project_root()
    paths_config = global_config.get("PATHS", {})
    config_base = _clean_rel_path(paths_config.get("CONFIG", "config/"))
    config_dir = project_root / (config_base or "config")

    shared_config = global_config.get("SHARED_CONFIG", {})
    shared_enabled = bool(shared_config.get("ENABLED"))
    shared_path = _clean_rel_path(shared_config.get("PATH", ""))
    shared_files = shared_config.get("FILES", {})

    syncbot_config_path = config_dir / "Syncbot_CONFIG.json"
    colours_path = config_dir / "COLOURS.json"
    border_patterns_path = config_dir / "BORDER_PATTERNS.json"

    if shared_enabled:
        colours_name = shared_files.get("COLOURS", "COLOURS.json")
        border_name = shared_files.get("BORDER_PATTERNS", "BORDER_PATTERNS.json")
        if colours_name:
            colours_path = config_dir / shared_path / colours_name
        if border_name:
            border_patterns_path = config_dir / shared_path / border_name

    return {
        "Syncbot_CONFIG.json": syncbot_config_path,
        "COLOURS.json": colours_path,
        "BORDER_PATTERNS.json": border_patterns_path,
        "shared_enabled": shared_enabled,
        "shared_path": shared_path,
    }

def open_in_system_editor(target_path):
    """Open a path in the OS default editor/file browser."""
    if sys.platform == "win32":
        os.startfile(str(target_path))
        return

    if sys.platform == "darwin":
        command = ["open", str(target_path)]
    else:
        command = ["xdg-open", str(target_path)]

    subprocess.Popen(command)

def browse_for_path(prompt="Select path", start_path=None, allow_files=False):
    """
    Interactive CLI directory browser with optional GUI fallback.
    
    Args:
        prompt: Prompt text to display
        start_path: Starting directory (default: current directory or home)
        allow_files: If True, allow file selection; if False, directories only
        
    Returns:
        Path string if selected, None if cancelled
    """
    try:
        # Try GUI browser first on Windows if tkinter is available
        if sys.platform == 'win32':
            try:
                import tkinter as tk
                from tkinter import filedialog
                
                root = tk.Tk()
                root.withdraw()  # Hide the main window
                root.attributes('-topmost', True)  # Bring dialog to front
                
                if allow_files:
                    result = filedialog.askopenfilename(title=prompt, initialdir=start_path)
                else:
                    result = filedialog.askdirectory(title=prompt, initialdir=start_path)
                
                root.destroy()
                
                if result:
                    return result
                else:
                    logger.colour_log("!warn", "GUI browser cancelled, falling back to CLI browser")
            except ImportError:
                logger.colour_log("!warn", "tkinter not available, using CLI browser")
            except Exception as e:
                logger.colour_log("!warn", f"GUI browser error: {e}, using CLI browser")
    except Exception:
        pass  # Fall through to CLI browser
    
    # CLI-based browser
    print()
    logger.colour_log("!info", f"📂 {prompt}")
    logger.colour_log("!info", "Navigate: Enter number to open folder, '..' for parent, 'q' to cancel")
    print()
    
    # Determine starting path
    if start_path and Path(start_path).exists():
        current_path = Path(start_path).resolve()
    elif Path.home().exists():
        current_path = Path.home()
    else:
        current_path = Path.cwd()
    
    while True:
        try:
            logger.colour_log("!info", f"Current: {current_path}")
            print()
            
            # List contents
            try:
                items = []
                for item in sorted(current_path.iterdir()):
                    if allow_files or item.is_dir():
                        items.append(item)
            except PermissionError:
                logger.colour_log("!error", "Permission denied")
                items = []
            
            # Display items
            if not items:
                logger.colour_log("!warn", "No accessible items in this directory")
            else:
                for idx, item in enumerate(items[:50], 1):  # Limit to 50 items
                    icon = "📁" if item.is_dir() else "📄"
                    logger.colour_log("!list", f"{idx:2d}.", "!thisfolder", f"{icon} {item.name}")
                
                if len(items) > 50:
                    logger.colour_log("!warn", f"... and {len(items)-50} more items (not shown)")
            
            print()
            logger.colour_log("!list", "s", "!info", ". Select current directory")
            logger.colour_log("!list", "..", "!info", " Go to parent directory")
            logger.colour_log("!list", "m", "!info", ". Manual path entry")
            logger.colour_log("!list", "q", "!info", ". Cancel")
            print()
            
            choice = input("Enter choice: ").strip().lower()
            
            if choice == 'q':
                return None
            elif choice == 's':
                return str(current_path)
            elif choice == 'm':
                manual_path = input("Enter path manually: ").strip()
                if manual_path:
                    return manual_path
                continue
            elif choice == '..':
                if current_path.parent != current_path:  # Not at root
                    current_path = current_path.parent
                else:
                    logger.colour_log("!warn", "Already at root directory")
            else:
                try:
                    idx = int(choice)
                    if 1 <= idx <= min(len(items), 50):
                        selected = items[idx - 1]
                        if selected.is_dir():
                            current_path = selected
                        elif allow_files:
                            return str(selected)
                        else:
                            logger.colour_log("!warn", "Files not selectable, choose a directory")
                    else:
                        logger.colour_log("!error", "Invalid selection")
                except ValueError:
                    logger.colour_log("!error", "Invalid input")
            
            print()
            
        except KeyboardInterrupt:
            print()
            logger.colour_log("!warn", "Browser cancelled")
            return None
        except Exception as e:
            logger.colour_log("!error", f"Browser error: {e}")
            return None

def load_device_yaml(device_file):
    """Load a device YAML file safely."""
    try:
        with open(device_file, "r", encoding="utf-8") as file_handle:
            data = yaml.safe_load(file_handle) or {}
        return data
    except Exception as exc:
        logger.colour_log("!error", f"Could not load {device_file.name}: {exc}", log_files=list(LOG_FILES.values()))
        return {}

def save_device_yaml(device_file, data):
    """Persist a device YAML file safely."""
    with open(device_file, "w", encoding="utf-8") as file_handle:
        yaml.safe_dump(data, file_handle, sort_keys=False, allow_unicode=True)

def get_device_files():
    """Return sorted device YAML files."""
    device_config_dir = get_device_config_dir()
    if not device_config_dir.exists():
        return []
    return sorted(device_config_dir.glob("*.yaml"))

def get_current_hostname():
    """Return normalized current hostname."""
    return socket.gethostname().strip().upper()

def select_device_file(device_files=None):
    """Select the current device file based on hostname or user selection."""
    if device_files is None:
        device_files = get_device_files()

    if not device_files:
        return None

    current_hostname = get_current_hostname()
    for device_file in device_files:
        data = load_device_yaml(device_file)
        configured_hostname = str(data.get("hostname", "")).strip().upper()
        if configured_hostname and configured_hostname == current_hostname:
            return device_file

    if len(device_files) == 1:
        return device_files[0]

    print()
    logger.colour_log("!warn", "Current host not matched to a device config.")
    logger.colour_log("!info", "Select a device config to update:")
    for index, device_file in enumerate(device_files, 1):
        logger.colour_log("!list", str(index), "!info", f". {device_file.stem}")
    logger.colour_log("!list", str(len(device_files) + 1), "!info", ". Cancel")

    choice = input(f"\nSelect device (1-{len(device_files) + 1}): ").strip()
    try:
        choice_number = int(choice)
        if choice_number == len(device_files) + 1:
            return None
        if 1 <= choice_number <= len(device_files):
            return device_files[choice_number - 1]
    except ValueError:
        pass

    logger.colour_log("!error", "Invalid selection", log_files=list(LOG_FILES.values()))
    return None

def count_primary_hubs_and_nodes(device_files=None):
    """Return counts for device configs and primary HUB/NODE declarations."""
    if device_files is None:
        device_files = get_device_files()

    hub_primary_count = 0
    node_primary_count = 0

    for device_file in device_files:
        data = load_device_yaml(device_file)
        hubs = data.get("HUBS", {}) or {}
        nodes = data.get("NODES", {}) or {}

        for _, hub_data in hubs.items():
            if isinstance(hub_data, dict) and hub_data.get("is_primary"):
                hub_primary_count += 1

        for _, node_data in nodes.items():
            if isinstance(node_data, dict) and node_data.get("is_primary"):
                node_primary_count += 1

    return {
        "device_count": len(device_files),
        "primary_hub_count": hub_primary_count,
        "primary_node_count": node_primary_count,
    }

def build_default_device_config(device_label=None):
    """Build default device config skeleton for first-time setup."""
    current_hostname = get_current_hostname()
    name = device_label if device_label else f"{current_hostname} Device"
    return {
        "name": name,
        "role": "primary",
        "hostname": current_hostname,
        "manufacturer": "Unknown",
        "model": "Unknown",
        "os": os.name,
        "os_version": sys.platform,
        "enabled": True,
        "description": "Auto-generated device configuration",
        "DEFAULT_USER": "CURRENT_USER",
        "DEFAULT_GROUP": "CURRENT_GROUP",
        "IGNORE_FOLDERS": [],
        "IGNORE_FILES": [],
        "HUB_ASSIGNMENTS": [],
        "HUBS": {},
        "NODES": {},
        "SYNC_OPTION_OVERRIDES": {
            "remove_orphaned_files": True,
            "create_versioned_backups": False,
            "only_update_newer": True,
        },
    }

def ensure_hubs_nodes_sections(device_data):
    """Ensure HUBS and NODES sections exist in a device config."""
    if "HUBS" not in device_data or not isinstance(device_data.get("HUBS"), dict):
        device_data["HUBS"] = {}
    if "NODES" not in device_data or not isinstance(device_data.get("NODES"), dict):
        device_data["NODES"] = {}

def prompt_for_path(prompt_text, allow_browse=True, allow_files=False, start_path=None):
    """
    Prompt user for a path with optional BROWSE support.
    
    Args:
        prompt_text: Prompt to display
        allow_browse: If True, offer BROWSE option
        allow_files: If True, allow file selection (not just directories)
        start_path: Starting directory for browser
        
    Returns:
        Path string or None if cancelled
    """
    if allow_browse:
        logger.colour_log("!info", f"{prompt_text}")
        logger.colour_log("!list", "1", "!info", ". Enter path manually")
        logger.colour_log("!list", "2", "!info", ". Browse for path")
        logger.colour_log("!list", "q", "!info", ". Cancel")
        print()
        
        choice = input("Select option (1/2/q): ").strip().lower()
        
        if choice == 'q':
            return None
        elif choice == '2':
            browsed_path = browse_for_path(prompt_text, start_path=start_path, allow_files=allow_files)
            if browsed_path:
                return browsed_path
            logger.colour_log("!warn", "Browse cancelled, enter path manually")
        
        # Fall through to manual entry for choice '1' or if browse was cancelled
    
    path = input(f"{prompt_text}: ").strip()
    return path if path else None

def initialize_device_setup_wizard():
    """Interactive first-run wizard to initialize device + primary HUB/NODE."""
    print()
    apply_menu_header(text="🧭 First-Time Setup Wizard")
    print()

    device_config_dir = get_device_config_dir()
    device_config_dir.mkdir(parents=True, exist_ok=True)

    device_files = get_device_files()
    device_file = select_device_file(device_files)

    if device_file is None and not device_files:
        default_name = get_current_hostname().lower()
        suggested_file = device_config_dir / f"{default_name}.yaml"
        custom_name = input(f"Device config file name [{default_name}]: ").strip().lower()
        if custom_name:
            suggested_file = device_config_dir / f"{custom_name}.yaml"

        friendly_name = input("Device display name (optional): ").strip()
        device_data = build_default_device_config(friendly_name or None)
        save_device_yaml(suggested_file, device_data)
        device_file = suggested_file
        logger.colour_log("!done", f"✓ Created device config: {device_file.name}")
    elif device_file is None:
        logger.colour_log("!warn", "Setup cancelled")
        return

    device_data = load_device_yaml(device_file)
    ensure_hubs_nodes_sections(device_data)

    if not any(isinstance(item, dict) and item.get("is_primary") for item in device_data.get("HUBS", {}).values()):
        print()
        logger.colour_log("!info", "Primary HUB is required.")
        hub_key = input("Primary HUB key [primary]: ").strip().lower() or "primary"
        hub_name = input("Primary HUB display name: ").strip() or "Primary HUB"
        print()
        hub_path = prompt_for_path("Primary HUB path", allow_browse=True)
        if not hub_path:
            logger.colour_log("!warn", "HUB path required, wizard incomplete")
            return
        is_valid, resolved_path, error_message = validate_path(hub_path, "Primary HUB path")
        if not is_valid:
            logger.colour_log("!warn", error_message)

        device_data["HUBS"][hub_key] = {
            "name": hub_name,
            "path": hub_path,
            "is_primary": True,
            "enabled": True,
            "repository_role": "HUB",
            "description": "Primary hub configured via setup wizard",
            "user_group": "",
            "last_validated": datetime.now().isoformat(timespec="seconds"),
        }

    if not any(isinstance(item, dict) and item.get("is_primary") for item in device_data.get("NODES", {}).values()):
        print()
        logger.colour_log("!info", "Primary NODE is required.")
        node_key = input("Primary NODE key [primary_node]: ").strip().lower() or "primary_node"
        node_name = input("Primary NODE display name: ").strip() or "Primary Node"
        print()
        node_path = prompt_for_path("Primary NODE path", allow_browse=True)
        if not node_path:
            logger.colour_log("!warn", "NODE path required, wizard incomplete")
            return
        node_type = input("Node type [STANDARD/PROJECT]: ").strip().upper() or "STANDARD"
        if node_type not in {"STANDARD", "PROJECT"}:
            node_type = "STANDARD"
        is_valid, _, error_message = validate_path(node_path, "Primary NODE path")
        if not is_valid:
            logger.colour_log("!warn", error_message)

        device_data["NODES"][node_key] = {
            "name": node_name,
            "path": node_path,
            "is_primary": True,
            "enabled": True,
            "repository_role": "NODE",
            "node_type": node_type,
            "ownership": "",
            "description": "Primary node configured via setup wizard",
        }

    save_device_yaml(device_file, device_data)

    counts = count_primary_hubs_and_nodes()
    print()
    logger.colour_log("!done", "✅ Device setup wizard completed")
    logger.colour_log("!list", "  Device configs:", "!thisfolder", str(counts["device_count"]))
    logger.colour_log("!list", "  Primary HUBs:", "!thisfolder", str(counts["primary_hub_count"]))
    logger.colour_log("!list", "  Primary NODEs:", "!thisfolder", str(counts["primary_node_count"]))
    input("\nPress ENTER to continue...")

def run_startup_configuration_checks():
    """Run startup checks and offer first-time setup when needed."""
    device_files = get_device_files()
    counts = count_primary_hubs_and_nodes(device_files)

    if counts["device_count"] == 0:
        print()
        logger.colour_log("!warn", "No device configs found in config/devices.d")
        choice = input("Run first-time setup wizard now? (Y/n): ").strip().lower()
        if choice in {"", "y", "yes"}:
            initialize_device_setup_wizard()
        return

    if counts["primary_hub_count"] == 0 or counts["primary_node_count"] == 0:
        print()
        logger.colour_log("!warn", "Device config check found missing required primary entries.")
        logger.colour_log("!list", "  Primary HUB count:", "!thisfolder", str(counts["primary_hub_count"]))
        logger.colour_log("!list", "  Primary NODE count:", "!thisfolder", str(counts["primary_node_count"]))
        choice = input("Open first-time setup wizard to fix this? (Y/n): ").strip().lower()
        if choice in {"", "y", "yes"}:
            initialize_device_setup_wizard()

def get_project_root():
    """Get the Syncbot project root directory"""
    return Path(__file__).resolve().parent.parent.parent.parent

def get_config_dir():
    """Get the config directory"""
    return get_project_root() / "config"

def get_device_config_dir():
    """Get the devices.d directory"""
    return get_config_dir() / "devices.d"

def validate_path(path_str, description="Path"):
    """
    Validate if a path exists and is accessible.
    Returns (is_valid, resolved_path, error_message)
    """
    try:
        path = Path(path_str).expanduser().resolve()
        if not path.exists():
            return False, path, f"{description} does not exist: {path}"
        return True, path, None
    except Exception as e:
        return False, None, f"Invalid {description.lower()}: {e}"

def review_setup():
    """Display current device and configuration setup details."""
    print()
    apply_menu_header(text="🔍 Setup Review & Configuration")
    print()
    
    try:
        global_config = config_loader.global_config
        info_display = str(global_config.get("INFO_DISPLAY", "VERBOSE")).strip().upper()
        is_verbose = info_display != "BASIC"

        roots = global_config.get("ROOTS", {})
        root_modes = global_config.get("ROOT_MODES", {})
        paths = global_config.get("PATHS", {})

        def resolve_mode_path(path_key):
            mode = str(root_modes.get(path_key, "project")).strip().lower()
            root_key = "WORKSPACE" if mode == "workspace" else "PROJECT"
            root_value = roots.get(root_key, "")
            rel_path = str(paths.get(path_key, "")).replace("\\", "/").lstrip("./")
            if root_value:
                return Path(root_value) / Path(rel_path) if rel_path else Path(root_value)
            return Path(rel_path) if rel_path else Path(".")

        device_files = get_device_files()
        current_device_file = None
        current_hostname = get_current_hostname()
        for device_file in device_files:
            device_data = load_device_yaml(device_file)
            configured_hostname = str(device_data.get("hostname", "")).strip().upper()
            if configured_hostname and configured_hostname == current_hostname:
                current_device_file = device_file
                break

        if current_device_file is None and len(device_files) == 1:
            current_device_file = device_files[0]

        current_device_data = (
            load_device_yaml(current_device_file) if current_device_file else {}
        )
        hubs = current_device_data.get("HUBS", {}) if isinstance(current_device_data, dict) else {}
        nodes = current_device_data.get("NODES", {}) if isinstance(current_device_data, dict) else {}
        standard_nodes = []
        project_nodes = []
        for node_key, node_entry in (nodes or {}).items():
            if not isinstance(node_entry, dict):
                continue
            node_type = str(node_entry.get("node_type", "STANDARD")).strip().upper()
            node_name = node_entry.get("name", node_key)
            node_path = node_entry.get("path", "")
            if node_type == "PROJECT":
                project_nodes.append((node_name, node_path))
            else:
                standard_nodes.append((node_name, node_path))
        
        # Project information
        logger.colour_log("!info", "📋 Project Information:")
        project_info = global_config.get("INFO", {})
        logger.colour_log(
            "!list",
            "  Name:",
            "!thisfolder",
            project_info.get("PROJECT_NAME", global_config.get("PROJECT_NAME", "N/A"))
        )
        logger.colour_log(
            "!list",
            "  Version:",
            "!thisfolder",
            project_info.get("VERSION", global_config.get("VERSION", "N/A"))
        )
        logger.colour_log(
            "!list",
            "  Author:",
            "!thisfolder",
            project_info.get("AUTHOR", global_config.get("AUTHOR", "N/A"))
        )
        logger.colour_log("!list", "  Info Display:", "!thisfolder", info_display)
        
        print()
        logger.colour_log("!info", "🖥️  Device Configuration:")
        if is_verbose:
            if current_device_file:
                logger.colour_log("!list", "  Device File:", "!thisfolder", current_device_file.name)
                logger.colour_log(
                    "!list",
                    "  Device Name:",
                    "!thisfolder",
                    str(current_device_data.get("name", current_device_file.stem))
                )
                logger.colour_log(
                    "!list",
                    "  Hostname:",
                    "!thisfolder",
                    str(current_device_data.get("hostname", "N/A"))
                )
                logger.colour_log(
                    "!list",
                    "  Role:",
                    "!thisfolder",
                    str(current_device_data.get("role", "N/A")).upper()
                )
                logger.colour_log(
                    "!list",
                    "  Enabled:",
                    "!thisfolder",
                    str(current_device_data.get("enabled", "N/A"))
                )
                logger.colour_log(
                    "!list",
                    "  OS:",
                    "!thisfolder",
                    str(current_device_data.get("os", "N/A"))
                )
                logger.colour_log(
                    "!list",
                    "  OS Version:",
                    "!thisfolder",
                    str(current_device_data.get("os_version", "N/A"))
                )
                logger.colour_log(
                    "!list",
                    "  Manufacturer:",
                    "!thisfolder",
                    str(current_device_data.get("manufacturer", "N/A"))
                )
                logger.colour_log(
                    "!list",
                    "  Model:",
                    "!thisfolder",
                    str(current_device_data.get("model", "N/A"))
                )
            else:
                logger.colour_log("!warn", "  No matching device config found for current host")

            logger.colour_log("!list", "  HUB Entries:", "!thisfolder", str(len(hubs or {})))
            logger.colour_log("!list", "  NODE Entries:", "!thisfolder", str(len(nodes or {})))

            if standard_nodes:
                logger.colour_log("!info", "  Standard Repositories:")
                for node_name, node_path in standard_nodes:
                    logger.colour_log("!list", "    •", "!thisfolder", f"{node_name} -> {node_path}")
            if project_nodes:
                logger.colour_log("!info", "  Project Repositories:")
                for node_name, node_path in project_nodes:
                    logger.colour_log("!list", "    •", "!thisfolder", f"{node_name} -> {node_path}")
            if not standard_nodes and not project_nodes:
                logger.colour_log("!warn", "  No repository NODE entries configured for this device")
        else:
            logger.colour_log("!list", "  Hostname:", "!thisfolder", current_hostname)
            logger.colour_log(
                "!list",
                "  Active Device:",
                "!thisfolder",
                current_device_file.name if current_device_file else "N/A"
            )
            logger.colour_log("!list", "  HUB Entries:", "!thisfolder", str(len(hubs or {})))
            logger.colour_log("!list", "  NODE Entries:", "!thisfolder", str(len(nodes or {})))
            logger.colour_log("!list", "  Standard Repos:", "!thisfolder", str(len(standard_nodes)))
            logger.colour_log("!list", "  Project Repos:", "!thisfolder", str(len(project_nodes)))
        
        print()
        logger.colour_log("!info", "💾 Backup Mode:")
        backup_mode = global_config.get("BACKUP_MODE", {})
        mode = backup_mode.get("mode", "N/A")
        logger.colour_log("!list", "  Mode:", "!thisfolder", mode)
        logger.colour_log("!list", "  Description:", "!thisfolder", backup_mode.get("description", "N/A"))
        
        if mode == "repository_folder":
            umbrellas = backup_mode.get("repository_folder_umbrellas", [])
            logger.colour_log("!info", "  Repository Umbrellas:")
            for umbrella in umbrellas:
                logger.colour_log("!list", "    •", "!thisfolder", umbrella)

        print()
        logger.colour_log("!info", "🧭 Root Modes & Path Resolution:")
        if is_verbose:
            logger.colour_log("!info", "  Root Base Paths:")
            for root_key in ["PROJECT", "WORKSPACE", "TUILKIT"]:
                if root_key in roots:
                    logger.colour_log("!list", f"    {root_key}:", "!thisfolder", str(roots[root_key]))
            logger.colour_log("!info", "  Resolved Paths by Mode:")

        for mode_key, mode_value in root_modes.items():
            if mode_key.startswith("ROOT_MODES:"):
                continue
            mode_lower = str(mode_value).strip().lower()
            if mode_lower not in {"project", "workspace"}:
                continue

            configured_path = paths.get(mode_key, "")
            resolved_path = resolve_mode_path(mode_key)
            if is_verbose:
                logger.colour_log(
                    "!list",
                    f"  {mode_key} [{mode_lower}]",
                    "!info",
                    f"path='{configured_path}'",
                    "!thisfolder",
                    str(resolved_path)
                )
            elif mode_key in {"CONFIG", "LOGS", "INPUTS", "OUTPUTS"}:
                logger.colour_log(
                    "!list",
                    f"  {mode_key} [{mode_lower}] ->",
                    "!thisfolder",
                    str(resolved_path)
                )
        
        print()
        logger.colour_log("!info", "📁 Log Files Location:")
        log_files = global_config.get("LOG_FILES", {})
        resolved_log_base = resolve_mode_path("LOGS")
        for log_name, log_path in log_files.items():
            log_path_obj = Path(str(log_path))
            resolved_log_path = (
                log_path_obj if log_path_obj.is_absolute() else resolved_log_base / log_path_obj
            )
            if is_verbose:
                logger.colour_log(
                    "!list",
                    f"  {log_name}:",
                    "!info",
                    str(log_path),
                    "!thisfolder",
                    str(resolved_log_path)
                )
            else:
                logger.colour_log("!list", f"  {log_name}:", "!thisfolder", str(resolved_log_path))

        print()
        logger.colour_log("!info", "🧩 Device Config Framework Status:")
        counts = count_primary_hubs_and_nodes()
        logger.colour_log("!list", "  Device configs:", "!thisfolder", str(counts["device_count"]))
        logger.colour_log("!list", "  Primary HUBs:", "!thisfolder", str(counts["primary_hub_count"]))
        logger.colour_log("!list", "  Primary NODEs:", "!thisfolder", str(counts["primary_node_count"]))
        if counts["device_count"] == 0 or counts["primary_hub_count"] == 0 or counts["primary_node_count"] == 0:
            logger.colour_log("!warn", "  Setup incomplete. Use 'First-Time Setup Wizard' from main menu.")
        
        print()
        logger.colour_log("!info", "✅ Setup review complete!")
        
    except Exception as e:
        logger.colour_log("!error", f"Error reviewing setup: {e}", log_files=list(LOG_FILES.values()))
    
    print()
    input("Press ENTER to return to main menu...")

def review_hubs():
    """Display accessible HUBs with status and path information"""
    print()
    apply_menu_header(text="🗂️  Accessible HUBs Review")
    print()
    
    try:
        logger.colour_log("!info", "Current HUB repository mappings:")

        device_config_dir = get_device_config_dir()
        if device_config_dir.exists():
            device_files = list(device_config_dir.glob("*.yaml"))
            if device_files:
                logger.colour_log("!list", f"  Found {len(device_files)} device configuration(s)")
                for device_file in device_files:
                    try:
                        with open(device_file, 'r') as f:
                            device_config = yaml.safe_load(f)
                            device_name = device_config.get("name", device_file.stem)
                            hubs = device_config.get("HUBS", {}) or {}
                            logger.colour_log("!list", f"    • {device_name}")
                            if not hubs:
                                logger.colour_log("!list", "      (no HUB entries)")
                                continue

                            for hub_key, hub_entry in hubs.items():
                                if not isinstance(hub_entry, dict):
                                    continue
                                hub_path = str(hub_entry.get("path", ""))
                                is_valid, resolved, error_msg = validate_path(hub_path, f"HUB '{hub_key}' path")
                                primary_marker = " [primary]" if hub_entry.get("is_primary") else ""
                                if is_valid:
                                    logger.colour_log("!done", f"      ✓ {hub_key}{primary_marker}")
                                    logger.colour_log("!list", "        Path:", "!thisfolder", str(resolved))
                                else:
                                    logger.colour_log("!error", f"      ✗ {hub_key}{primary_marker}")
                                    logger.colour_log("!list", "        Path:", "!error", hub_path)
                                    logger.colour_log("!list", "        Status:", "!warn", error_msg or "Not accessible")
                    except Exception as e:
                        logger.colour_log("!error", f"    Error reading {device_file.name}: {e}")
            else:
                logger.colour_log("!list", "  No device configurations found")
        else:
            logger.colour_log("!error", "  Device config directory not found")
        
        print()
        logger.colour_log("!info", "✅ HUB review complete!")
        
    except Exception as e:
        logger.colour_log("!error", f"Error reviewing HUBs: {e}", log_files=list(LOG_FILES.values()))
    
    print()
    input("Press ENTER to return to main menu...")

def edit_config_files():
    """Allow editing of accessible configuration files"""
    print()
    apply_menu_header(text="⚙️  Configuration Files Editor")
    print()

    global_config = config_loader.global_config
    menu_paths = resolve_menu_config_paths(global_config)
    colours_desc = "Colour schemes (use tUilKit colour editor)"
    borders_desc = "Border style patterns"
    if menu_paths.get("shared_enabled"):
        shared_path = menu_paths.get("shared_path") or "GLOBAL_SHARED.d"
        colours_desc += f" [shared: {shared_path}]"
        borders_desc += f" [shared: {shared_path}]"
    
    # Define available config files
    config_files = {
        "1": (
            "Syncbot_CONFIG.json",
            menu_paths["Syncbot_CONFIG.json"],
            "Main Syncbot configuration"
        ),
        "2": ("COLOURS.json", menu_paths["COLOURS.json"], colours_desc),
        "3": (
            "BORDER_PATTERNS.json",
            menu_paths["BORDER_PATTERNS.json"],
            borders_desc
        ),
    }
    
    logger.colour_log("!info", "📋 Available Configuration Files:")
    for key, (name, path, desc) in config_files.items():
        exists = "✓" if path.exists() else "✗"
        logger.colour_log("!list", key, "!info", f". {exists} {name} - {desc}")
    
    logger.colour_log("!list", "4", "!info", ". 🖥️  Edit Device Configuration")
    logger.colour_log("!list", "5", "!info", ". 🔙 Back to Main Menu")
    
    choice = input("\nSelect file to edit (1-5): ").strip()
    
    if choice in config_files:
        name, path, desc = config_files[choice]
        edit_config_file(name, path)
    elif choice == "4":
        print()
        edit_device_config()
    elif choice == "5":
        return
    else:
        print()
        logger.colour_log("!error", "❌ Invalid selection")

def edit_config_file(name, file_path):
    """Edit a specific configuration file"""
    print()
    
    if not file_path.exists():
        logger.colour_log("!error", f"File not found: {file_path}", log_files=list(LOG_FILES.values()))
        input("Press ENTER to continue...")
        return
    
    logger.colour_log("!info", f"📝 Editing: {name}")
    logger.colour_log("!info", f"Path: {file_path}")
    print()
    
    # For COLOURS.json, offer special handling
    if name == "COLOURS.json":
        logger.colour_log("!info", "💡 Tip: Use tUilKit's colour editor for COLOURS.json")
        logger.colour_log("!info", "  Run: python -m tUilKit.tools.colour_editor")
        print()
    
    logger.colour_log("!info", "Choose action:")
    logger.colour_log("!list", "1", "!info", ". View file content")
    logger.colour_log("!list", "2", "!info", ". Open in text editor (notepad)")
    logger.colour_log("!list", "3", "!info", ". Back")
    
    action = input("\nSelect action (1-3): ").strip()
    
    if action == "1":
        print()
        display_file_content(file_path)
    elif action == "2":
        try:
            print()
            logger.colour_log("!info", "Opening file in text editor...")
            open_in_system_editor(file_path)
            logger.colour_log("!done", "✓ File opened in editor")
        except Exception as e:
            logger.colour_log("!error", f"Could not open file: {e}", log_files=list(LOG_FILES.values()))
        
        print()
        input("Press ENTER to continue...")
    
    print()
    edit_config_files()  # Return to config menu

def display_file_content(file_path):
    """Display file content with syntax highlighting info"""
    try:
        path_obj = Path(file_path)
        if path_obj.is_dir():
            logger.colour_log(
                "!error",
                f"Expected a file but received a directory: {path_obj}",
                log_files=list(LOG_FILES.values())
            )
            return

        with open(path_obj, 'r') as f:
            content = f.read()
        
        logger.colour_log("!info", f"📖 Content of {path_obj.name}:")
        logger.colour_log("!info", "─" * 70)
        print(content[:2000])  # Limit to first 2000 chars
        if len(content) > 2000:
            logger.colour_log("!info", "... (truncated)")
        logger.colour_log("!info", "─" * 70)
    except Exception as e:
        logger.colour_log("!error", f"Error reading file: {e}", log_files=list(LOG_FILES.values()))

def edit_device_config():
    """Allow editing of device configuration files"""
    print()
    apply_menu_header(text="🖥️  Device Configuration", border_rainbow=False)
    print()
    
    device_config_dir = get_device_config_dir()
    
    if not device_config_dir.exists():
        logger.colour_log("!error", f"Device config directory not found: {device_config_dir}", log_files=list(LOG_FILES.values()))
        input("Press ENTER to continue...")
        return
    
    device_files = sorted(device_config_dir.glob("*.yaml"))
    
    if not device_files:
        logger.colour_log("!warn", "No device configuration files found")
        choice = input("Run first-time setup wizard now? (Y/n): ").strip().lower()
        if choice in {"", "y", "yes"}:
            initialize_device_setup_wizard()
        return
    
    logger.colour_log("!info", "Available Devices:")
    for i, device_file in enumerate(device_files, 1):
        logger.colour_log("!list", str(i), "!info", f". {device_file.stem}")
    
    logger.colour_log("!list", str(len(device_files) + 1), "!info", ". 🔙 Back")
    
    choice = input(f"\nSelect device (1-{len(device_files) + 1}): ").strip()
    
    try:
        choice_num = int(choice)
        if choice_num == len(device_files) + 1:
            return
        if 1 <= choice_num <= len(device_files):
            device_file = device_files[choice_num - 1]
            edit_device_file(device_file)
    except ValueError:
        logger.colour_log("!error", "Invalid selection")

def edit_device_file(device_file):
    """Edit a specific device configuration file"""
    print()
    
    logger.colour_log("!info", f"📝 Editing: {device_file.name}")
    print()
    logger.colour_log("!info", "Choose action:")
    logger.colour_log("!list", "1", "!info", ". View content")
    logger.colour_log("!list", "2", "!info", ". Open in text editor")
    logger.colour_log("!list", "3", "!info", ". Back")
    
    action = input("\nSelect action (1-3): ").strip()
    
    if action == "1":
        print()
        display_file_content(device_file)
    elif action == "2":
        try:
            print()
            logger.colour_log("!info", "Opening file in text editor...")
            open_in_system_editor(device_file)
            logger.colour_log("!done", "✓ File opened in editor")
        except Exception as e:
            logger.colour_log("!error", f"Could not open file: {e}", log_files=list(LOG_FILES.values()))
        
        print()
        input("Press ENTER to continue...")
    
    print()
    edit_device_config()  # Return to device config menu

def add_hub():
    """Add a new HUB repository"""
    print()
    apply_menu_header(text="➕ Add New HUB Repository")
    print()
    
    logger.colour_log("!info", "📝 Enter HUB Details:")
    
    hub_name = input("HUB Name (e.g., 'NAS Storage'): ").strip()
    if not hub_name:
        logger.colour_log("!error", "HUB name cannot be empty")
        input("Press ENTER to continue...")
        return
    
    print()
    hub_path = prompt_for_path("HUB Path (local or network)", allow_browse=True)
    if not hub_path:
        logger.colour_log("!error", "HUB path cannot be empty")
        input("Press ENTER to continue...")
        return
    
    is_valid, resolved, error_msg = validate_path(hub_path, "HUB path")
    
    print()
    if not is_valid:
        logger.colour_log("!error", "⚠️  Warning: Path validation failed")
        logger.colour_log("!warn", f"  {error_msg}")
        logger.colour_log("!warn", "  You can still add this HUB, but verify it exists before backing up.")
        confirm = input("\nCreate anyway? (y/N): ").strip().lower()
        if confirm != 'y':
            print()
            logger.colour_log("!warn", "HUB creation cancelled")
            input("Press ENTER to continue...")
            return
    else:
        logger.colour_log("!done", "✓ Path is accessible")
    
    device_file = select_device_file()
    if device_file is None:
        logger.colour_log("!error", "No target device selected for HUB update", log_files=list(LOG_FILES.values()))
        input("Press ENTER to continue...")
        return

    device_data = load_device_yaml(device_file)
    ensure_hubs_nodes_sections(device_data)
    hub_key = hub_name.strip().lower().replace(" ", "_")
    if not hub_key:
        hub_key = "hub"

    hub_primary_choice = input("Mark as primary HUB? (y/N): ").strip().lower()
    make_primary = hub_primary_choice in {"y", "yes"}
    if make_primary:
        for key, hub_entry in device_data["HUBS"].items():
            if isinstance(hub_entry, dict):
                hub_entry["is_primary"] = False

    device_data["HUBS"][hub_key] = {
        "name": hub_name,
        "path": hub_path,
        "is_primary": make_primary,
        "enabled": True,
        "repository_role": "HUB",
        "description": "Added from Syncbot menu",
        "user_group": "",
        "last_validated": datetime.now().isoformat(timespec="seconds"),
    }

    save_device_yaml(device_file, device_data)

    print()
    logger.colour_log("!info", "HUB Configuration Summary:")
    logger.colour_log("!list", "  Device File:", "!thisfolder", device_file.name)
    logger.colour_log("!list", "  HUB Key:", "!thisfolder", hub_key)
    logger.colour_log("!list", "  Name:", "!thisfolder", hub_name)
    logger.colour_log("!list", "  Path:", "!thisfolder", hub_path)
    
    print()
    logger.colour_log("!done", "✅ HUB added successfully!")
    logger.colour_log("!info", "Next steps:")
    logger.colour_log("!list", "  1. Configure device to use this HUB")
    logger.colour_log("!list", "  2. Select repositories to backup to this HUB")
    logger.colour_log("!list", "  3. Run backup to test")
    
    input("\nPress ENTER to continue...")

def add_project():
    """Add a new project or folder node to backup"""
    print()
    apply_menu_header(text="📦 Add New Project/Folder Node")
    print()
    
    logger.colour_log("!info", "📝 Enter Repository/Folder Details:")
    
    project_name = input("Project/Folder Name: ").strip()
    if not project_name:
        logger.colour_log("!error", "Repository name cannot be empty")
        input("Press ENTER to continue...")
        return
    
    print()
    project_path = prompt_for_path("Repository/Folder Path (local path)", allow_browse=True)
    if not project_path:
        logger.colour_log("!error", "Repository path cannot be empty")
        input("Press ENTER to continue...")
        return
    
    node_role = input("Repository role [NODE/HUB] (default NODE): ").strip().upper() or "NODE"
    if node_role not in {"NODE", "HUB"}:
        node_role = "NODE"

    node_type = input("Node type [STANDARD/PROJECT/CUSTOM] (default STANDARD): ").strip().upper() or "STANDARD"
    if node_type not in {"STANDARD", "PROJECT", "CUSTOM"}:
        node_type = "STANDARD"

    ownership = input("Ownership (USER:GROUP, optional): ").strip()

    is_valid, resolved, error_msg = validate_path(project_path, "Repository path")
    
    print()
    if not is_valid:
        logger.colour_log("!error", "⚠️  Path validation failed")
        logger.colour_log("!warn", f"  {error_msg}")
        confirm = input("\nCreate node anyway? (y/N): ").strip().lower()
        if confirm != 'y':
            print()
            logger.colour_log("!warn", "Repository creation cancelled")
            input("Press ENTER to continue...")
            return
    else:
        logger.colour_log("!done", "✓ Path is accessible")
    
    device_file = select_device_file()
    if device_file is None:
        logger.colour_log("!error", "No target device selected for NODE update", log_files=list(LOG_FILES.values()))
        input("Press ENTER to continue...")
        return

    device_data = load_device_yaml(device_file)
    ensure_hubs_nodes_sections(device_data)
    node_key = project_name.strip().lower().replace(" ", "_")
    if not node_key:
        node_key = "node"

    primary_choice = input("Mark as primary NODE? (y/N): ").strip().lower()
    make_primary = primary_choice in {"y", "yes"}
    if make_primary:
        for key, node_entry in device_data["NODES"].items():
            if isinstance(node_entry, dict):
                node_entry["is_primary"] = False

    device_data["NODES"][node_key] = {
        "name": project_name,
        "path": project_path,
        "is_primary": make_primary,
        "enabled": True,
        "repository_role": node_role,
        "node_type": node_type,
        "ownership": ownership,
        "description": "Added from Syncbot menu",
    }

    save_device_yaml(device_file, device_data)

    print()
    logger.colour_log("!info", "Repository Configuration Summary:")
    logger.colour_log("!list", "  Device File:", "!thisfolder", device_file.name)
    logger.colour_log("!list", "  Node Key:", "!thisfolder", node_key)
    logger.colour_log("!list", "  Name:", "!thisfolder", project_name)
    logger.colour_log("!list", "  Path:", "!thisfolder", project_path)
    logger.colour_log("!list", "  Role:", "!thisfolder", node_role)
    logger.colour_log("!list", "  Type:", "!thisfolder", node_type)
    if ownership:
        logger.colour_log("!list", "  Ownership:", "!thisfolder", ownership)
    
    print()
    logger.colour_log("!done", "✅ Repository/Folder node created successfully!")
    logger.colour_log("!info", "Next steps:")
    logger.colour_log("!list", "  1. Review device configuration to enable this repository")
    logger.colour_log("!list", "  2. Configure backup destination HUB")
    logger.colour_log("!list", "  3. Run backup to sync this repository")
    
    input("\nPress ENTER to continue...")

def configure_hub_or_project():
    """Configure an existing HUB or Project/Folder node"""
    print()
    apply_menu_header(text="🔧 Configure HUB or Project/Folder")
    print()
    
    logger.colour_log("!info", "Select what to configure:")
    logger.colour_log("!list", "1", "!info", ". 🗂️  Configure HUB (backup destination)")
    logger.colour_log("!list", "2", "!info", ". 📦 Configure Project/Folder")
    logger.colour_log("!list", "3", "!info", ". 🔙 Back")
    
    choice = input("\nSelect (1-3): ").strip()
    
    if choice == "1":
        print()
        logger.colour_log("!info", "🔧 HUB Configuration")
        logger.colour_log("!info", "Edit Syncbot_CONFIG.json to change HUB settings")
        logger.colour_log("!info", "Key settings:")
        logger.colour_log("!list", "  • WORKSPACE.backup_destination: HUB location path")
        logger.colour_log("!list", "  • BACKUP_MODE.mode: 'repository_folder' or 'single_folder'")
        print()
    elif choice == "2":
        print()
        logger.colour_log("!info", "📦 Project/Folder Configuration")
        logger.colour_log("!info", "Edit device configuration file to manage repository NODE mappings")
        logger.colour_log("!info", "Location: config/devices.d/")
        logger.colour_log("!info", "Edit 'NODES' (and related 'HUBS') sections in device YAML file")
        print()
    elif choice == "3":
        return
    else:
        logger.colour_log("!error", "Invalid selection")
        input("Press ENTER to continue...")
        return
    
    logger.colour_log("!info", "Choose action:")
    logger.colour_log("!list", "1", "!info", ". View related config file")
    logger.colour_log("!list", "2", "!info", ". Edit config in text editor")
    logger.colour_log("!list", "3", "!info", ". Back")
    
    action = input("\nSelect (1-3): ").strip()

    def select_device_config_file():
        """Prompt user to select a device YAML file and return its path."""
        device_config_dir = get_device_config_dir()
        device_files = sorted(device_config_dir.glob("*.yaml"))

        if not device_files:
            logger.colour_log(
                "!warn",
                f"No device configuration files found in: {device_config_dir}",
                log_files=list(LOG_FILES.values())
            )
            return None

        print()
        logger.colour_log("!info", "Select device configuration file:")
        for i, device_file in enumerate(device_files, 1):
            logger.colour_log("!list", str(i), "!info", f". {device_file.stem}")
        logger.colour_log("!list", str(len(device_files) + 1), "!info", ". 🔙 Back")

        selection = input(f"\nSelect device (1-{len(device_files) + 1}): ").strip()
        try:
            selection_num = int(selection)
            if selection_num == len(device_files) + 1:
                return None
            if 1 <= selection_num <= len(device_files):
                return device_files[selection_num - 1]
        except ValueError:
            pass

        logger.colour_log("!error", "Invalid device selection", log_files=list(LOG_FILES.values()))
        return None
    
    if action == "1":
        print()
        if choice == "1":
            config_file = get_config_dir() / "Syncbot_CONFIG.json"
        else:
            config_file = select_device_config_file()
            if config_file is None:
                return
        
        display_file_content(config_file)
    elif action == "2":
        try:
            if choice == "1":
                config_file = get_config_dir() / "Syncbot_CONFIG.json"
            else:
                config_file = select_device_config_file()
                if config_file is None:
                    return
            
            print()
            logger.colour_log("!info", "Opening file in text editor...")
            open_in_system_editor(config_file)
            logger.colour_log("!done", "✓ File opened in editor")
        except Exception as e:
            logger.colour_log("!error", f"Could not open file: {e}", log_files=list(LOG_FILES.values()))
    
    print()
    input("Press ENTER to continue...")
