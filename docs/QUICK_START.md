# Your Syncbot Multi-Hub Setup at a Glance

**Last Updated:** 2026-03-11

## 🎯 Your Current Configuration

### Device: Ghost (Running Syncbot)
```
hostname: GHOST
role: primary
can_be_hub: yes (can serve as hub for other devices)

LOCAL WORK:           BACKUP DESTINATIONS (in order):
C:/Repository/...    1. NAS: \\192.168.0.2\devsrc\dev_pi (preferred, fast)
                     2. OneDrive: C:/Users/.../OneDrive/... (fallback, cloud)

Projects syncing:     tUilKit, Syncbot, H3l3n (from Projects/)
                      reports (from _PORTS/)
```

### Device: NAS (Network Hub)
```
hostname: nas.local
role: hub (central storage)
can_be_hub: yes (always hub)

CENTRAL STORE: \\192.168.0.2\devsrc\dev_pi
(receives syncs from Ghost, Pi, Falcon)

Projects stored:      tUilKit, Syncbot, H3l3n
```

### Device: Pi (Optional Secondary)
```
hostname: johnnyfive
role: secondary
can_be_hub: no

LOCAL WORK:           BACKUP DESTINATIONS (in order):
/home/pi/Core/        1. NAS: \\192.168.0.2\devsrc\dev_pi
                     2. OneDrive: /mnt/onedrive/...

Projects syncing:     tUilKit, Syncbot, H3l3n
```

### Device: Falcon (Optional Secondary)
```
hostname: FALCON
role: secondary
can_be_hub: no

LOCAL WORK:           BACKUP DESTINATIONS (in order):
D:/Core/Applications/      1. NAS: \\192.168.0.2\devsrc\dev_pi
                      2. OneDrive: <onedrive_root>/...

Projects syncing:     tUilKit, Syncbot, H3l3n, Calendars
```

---

## 📊 Sync Flow Diagram

```
GHOST (Your Machine)
│
├─ Working Directory: ./Applications/
│  ├─ tUilKit/
│  ├─ Syncbot/
│  ├─ H3l3n/
│  └─ _PORTS/reports/
│
├─ PRIMARY HUB (Fast, Local Network)
│  └─ NAS: \\192.168.0.2\devsrc\dev_pi/
│     ├─ tUilKit/        (synced from Ghost)
│     ├─ Syncbot/        (synced from Ghost)
│     ├─ H3l3n/          (synced from Ghost)
│     └─ reports/        (synced from Ghost)
│
└─ FALLBACK HUB (Reliable, Cloud)
   └─ OneDrive: ./_backup/
      ├─ tUilKit/        (synced from Ghost if NAS offline)
      ├─ Syncbot/
      ├─ H3l3n/
      └─ reports/

WHEN YOU HIT "BACKUP":
  1. Check: Is NAS online? (\\192.168.0.2 accessible)
     YES  → Sync to NAS ✓
     NO   → Check OneDrive
  2. Check: Is OneDrive accessible?
     YES  → Sync to OneDrive ✓
     NO   → Error: No accessible hub

WHEN PI SYNCS:
  1. Check: Is NAS online?
     YES  → Pull from NAS to /home/pi/dev ✓
     NO   → Check OneDrive
  2. If NAS offline: Pull from OneDrive to /home/pi/dev ✓
```

---

## 🔄 What Happens During Sync

### Scenario 1: Primary Hub (NAS) Online ✓
```
Ghost backup command executes:
  1. Check NAS accessibility: \\192.168.0.2\devsrc\dev_pi
     → Responds? YES
  2. Sync project to NAS:
     C:/Repository/.../tUilKit/    →  \\192.168.0.2/.../tUilKit/
     C:/Repository/.../Syncbot/    →  \\192.168.0.2/.../Syncbot/
     ...
  3. Complete: Used NAS (fast local network)
```

### Scenario 2: NAS Offline, OneDrive Available ✓
```
Ghost backup command executes:
  1. Check NAS accessibility: \\192.168.0.2\devsrc\dev_pi
     → Responds? NO (offline)
  2. Try fallback: OneDrive C:/Users/.../OneDrive/**
     → Accessible? YES
  3. Sync to OneDrive instead:
     C:/Repository/.../tUilKit/    →  C:/Users/.../OneDrive/.../tUilKit/
     C:/Repository/.../Syncbot/    →  C:/Users/.../OneDrive/.../Syncbot/
     ...
  4. Complete: Used OneDrive (fallback successful)
```

### Scenario 3: Both Offline ✗
```
Ghost backup command executes:
  1. Check NAS: \\192.168.0.2... → NO
  2. Check OneDrive: C:/Users/.../OneDrive... → NO
  3. Error: No accessible sync destination
     Choose an action:
       - Retry
       - Check network
       - Manual intervention
```

---

## 🎮 Your Control Points

### What You Can Change (Edit YAML)

**Which hubs to use:**
```yaml
preferred_hubs: [nas]              # Only NAS
preferred_hubs: [onedrive]         # Only OneDrive
preferred_hubs: [nas, onedrive]    # NAS first, then OneDrive
preferred_hubs: [onedrive, nas]    # OneDrive first, then NAS
```

**Whether device can be a hub:**
```yaml
can_be_hub: false   # This device cannot serve as hub
can_be_hub: true    # This device can serve as hub
```

**Which repositories to sync:**
```yaml
NODES:
   tuilkit_repo:
      name: tUilKit
      path: ./Core/tUilKit
      connected_hub_IDs: [nas_primary]
   syncbot_repo:
      name: Syncbot
      path: ./Applications/Syncbot
      connected_hub_IDs: [nas_primary]
```

### What You Get (Automatically)

- ✅ Auto-detection of which device is running
- ✅ Automatic hub selection (try preferred first)
- ✅ Fallback to secondary hub if primary offline
- ✅ Real-time path accessibility checks
- ✅ Clear logging of which hub was used
- ✅ Visual topology showing device relationships

---

## 🔍 How to Check Your Setup

### See Which Device You're On
```bash
python -c "
import socket
hostname = socket.gethostname()
print(f'You are running on: {hostname}')
"
```
Expected: `GHOST`, `FALCON`, `johnnyfive` (Pi), or `nas.local` (NAS)

### See Which Hubs You're Using
```bash
python verify_multihub_system.py
```
Shows:
- Your device (auto-detected)
- Your assigned hubs
- Which hubs are accessible
- Example sync target

### Check Individual Path
```bash
# Check if NAS is accessible
python -c "from pathlib import Path; print(Path(r'\\192.168.0.2\devsrc\dev_pi').exists())"
# Result: True or False

# Check if OneDrive is accessible  
python -c "from pathlib import Path; print(Path('<onedrive_root>').exists())"
# Result: True or False
```

---

## 🆕 Adding a New Device

### Quick 4-Step Process

**Step 1**: Get info
```bash
python src/Syncbot/utils/system_info.py
```
Output:
```
Hostname: NEWDEVICE
Manufacturer: Dell
Model: XPS 13
OS: Windows 11
```

**Step 2**: Create `config/devices.d/newdevice.yaml`
```yaml
name: New Device
role: secondary
hostname: NEWDEVICE
manufacturer: Dell
model: XPS 13
os: Windows 11
os_version: 10.0.22621

local_path: D:/Core/Projects
hub_path: D:/Sync/work/dev

can_be_hub: false
preferred_hubs: [nas, onedrive]
peer_sync_enabled: false

enabled: true

NODES:
   tuilkit_repo:
      name: tUilKit
      path: D:/Core/Applications/tUilKit
      connected_hub_IDs: [nas_primary]
   syncbot_repo:
      name: Syncbot
      path: D:/Core/Applications/Syncbot
      connected_hub_IDs: [nas_primary]
  Ports: []

description: New development device
```

**Step 3**: Test auto-detection
```bash
# Run on the new device
python verify_multihub_system.py
```
Should show:
```
Device Roles:
  newdevice -> role=secondary, hub=False
```

**Step 4**: Done! 
It auto-syncs next time you run Syncbot.

---

## 📋 Cheat Sheet

### File Locations
| What | Where |
|------|-------|
| Device configs | `config/devices.d/*.yaml` |
| Ghost settings | `config/devices.d/ghost.yaml` |
| NAS settings | `config/devices.d/nas.yaml` |
| Schema reference | `config/devices.d/README.md` |
| Menu system | `docs/MENU_SYSTEM.md` |
| Config setup | `docs/CONFIG_SETUP.md` |

### Key Concepts
| Concept | What It Means |
|---------|---------------|
| `local_path` | Where you work on this device |
| `hub_path` | Where this device backs up to |
| `preferred_hubs` | Priority order of backup destinations |
| `can_be_hub` | Can other devices sync to this one? |
| `role: primary` | Main development machine |
| `role: secondary` | Backup/portable device |
| `role: hub` | Central storage (NAS, cloud) |

### Routing Decision Tree
```
User hits "Backup"
  │
  ├─ Check preferred_hubs in order
  │  ├─ Is hub #1 accessible? → YES: Use it ✓
  │  ├─ Is hub #1 accessible? → NO: Try hub #2
  │  │   ├─ Is hub #2 accessible? → YES: Use it ✓
  │  │   └─ Is hub #2 accessible? → NO: Try others
  │
  ├─ All hubs offline?
  │  └─ Error: No accessible hub
  │      (Check network, check hub status)
  │
  └─ Sync completes (to first accessible hub)
```

---

## ✅ Verification Checklist

- [ ] Read QUICK_START.md (this file) to understand the setup
- [ ] Run `python verify_multihub_system.py` to see your setup
- [ ] Check that your device was auto-detected correctly
- [ ] Verify your preferred hubs are in the right order
- [ ] Confirm your hub paths are accessible
- [ ] Understand the sync flow (how projects backup/restore)
- [ ] Know how to add new devices (4-step process above)
- [ ] Know how to change hub assignments (edit YAML)

---

## 🎓 Understanding the System

**Three Key Layers:**

1. **Device Detection** (device_detection.py)
   - Identifies which machine is running (hostname)
   - Determines what hubs are available
   - Assigns hubs in preference order

2. **Configuration Loading** (config_loader.py)
   - Loads device configs from devices.d/
   - Can load full set (all devices) or minimal set (self + hubs)
   - Merges device-specific options

3. **Path Resolution** (path_resolver.py)
   - Takes project name
   - Finds first accessible hub in preferred order
   - Returns path to sync to
   - If primary hub offline, automatically tries secondary

**Why This Design?**

✅ **Clear**: You see exactly which device you're on and where it syncs
✅ **Resilient**: If primary hub offline, falls back automatically
✅ **Flexible**: Change hub assignments anytime (just edit YAML)
✅ **Scalable**: Add new devices or hubs without code changes
✅ **Future-proof**: Infrastructure ready for peer-to-peer sync, config auto-sync, etc.

---

## 🚀 You're Ready To Use It!

You now have a **multi-hub Syncbot system that**:

1. **Auto-detects your device** when you run it
2. **Intelligently routes syncs** to your preferred hubs
3. **Falls back automatically** if primary hub is offline
4. **Validates paths in real-time** before attempting sync
5. **Clearly shows** what's happening and why
6. **Lets you change hubs** by editing YAML (no code changes)
7. **Scales to multiple devices** with simple YAML configs

All with **crystal clear visibility** into:
- Which device you're on ✓
- Where it syncs to ✓  
- In what order ✓
- Which path is actually accessible ✓
- How the routing works ✓

**Start using it now!** Configuration is ready, verified, and documented.

For advanced setup options, see `docs/CONFIG_SETUP.md`.
