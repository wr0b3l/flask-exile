# 🎮 Pixel Bot - User Guide

## **What is Pixel Bot?**

Pixel Bot is a desktop automation tool that monitors specific pixels on your screen and triggers keyboard actions when those pixels change color. Perfect for gaming automation, workflow automation, and repetitive tasks!

---

## **Quick Start (Standalone .exe)**

### **Step 1: Download**
- Download `PixelBot.exe` (or run the installer)
- No installation needed for the .exe version!

### **Step 2: Run**
- Double-click `PixelBot.exe`
- Your browser opens automatically with the dashboard
- You'll see a console window (this is normal - shows logs)

### **Step 3: Create Your First Monitor**

1. Click **"Add Monitor"** button
2. Fill in the details:
   - **Name**: e.g., "Health Low Alert"
   - **Tolerance**: 10 (how much color can vary)
   
3. Go to **"Pixels" tab**:
   - Click **"Pick Pixel from Screen"**
   - Your screen shows a crosshair overlay
   - Click on the pixel you want to monitor
   - The coordinates and color are automatically filled in

4. Go to **"Type & Mode" tab**:
   - **Monitor Type**: Normal (or Master/Slave for advanced setups)
   - **Trigger Mode**: 
     - **"Match"** = triggers when pixel IS the target color
     - **"No Match"** = triggers when pixel is NOT the target color

5. Go to **"Action" tab**:
   - **Action Type**: Key Press / Hotkey / Log Only
   - **Key/Hotkey**: The key(s) to press (e.g., "r", "ctrl+1")
   - **Cooldown**: Minimum time (ms) between triggers

6. Click **"Add Monitor"**

### **Step 4: Use Your Monitor**
- Monitor starts automatically
- You'll see it in the "Active Monitors" list
- Stats update in real-time
- Activity logs show all actions

---

## **Dashboard Overview**

### **Main Sections:**

```
┌─────────────────────────────────────────────┐
│  PIXEL BOT                    🟢 Connected  │
├─────────────────────────────────────────────┤
│                                             │
│  [Add Monitor]  [Actions]                  │
│                                             │
│  ┌─────────────────┐  ┌──────────────────┐│
│  │ Active Monitors │  │  Activity Logs   ││
│  │                 │  │                  ││
│  │ • HP Monitor    │  │  ✓ HP triggered  ││
│  │ • Mana Monitor  │  │  ✓ Key pressed   ││
│  │                 │  │                  ││
│  └─────────────────┘  └──────────────────┘│
└─────────────────────────────────────────────┘
```

### **Active Monitors**
- Shows all your monitors
- Green = active and checking
- Click to pause/resume
- Edit or delete monitors

### **Activity Logs**
- Real-time event feed
- Shows triggers, actions, and state changes
- Auto-scrolls to latest

---

## **Monitor Types**

### **1. Normal Monitor** (Simple)
- Checks one pixel
- Triggers action when condition met
- Independent of other monitors

**Example:** Health low → Press health potion key

---

### **2. Master Monitor** (Advanced)
- Can check **multiple pixels** (up to 6)
- Controls "slave" monitors
- When master is ACTIVE → slaves can run
- When master is INACTIVE → slaves are blocked

**Logic Options:**
- **All Match**: ALL pixels must match to activate
- **Any Match**: ANY pixel matching activates

**Example:** Check if game UI is visible (3 UI corners) → Enable all other monitors

---

### **3. Slave Monitor** (Advanced)
- Linked to a master monitor
- Only runs when master is active
- Prevents false triggers during loading screens

**Example:** HP monitor (slave) → Only works when UI is visible (master)

---

## **Trigger Modes**

### **Match Mode** ✅
- Triggers when pixel **IS** the target color
- Use for: Detecting something appeared

**Example:** 
- Pixel turns RED → Trigger
- Health bar full → Trigger

### **No Match Mode** ❌
- Triggers when pixel **is NOT** the target color  
- Use for: Detecting something disappeared or changed

**Example:**
- Pixel NOT blue anymore → Trigger
- Mana bar empty → Trigger

---

## **Action Types**

### **1. Key Press**
- Press a single key
- Examples: `r`, `1`, `F1`, `space`

### **2. Hotkey**
- Press multiple keys simultaneously
- Examples: `ctrl+1`, `shift+f`, `alt+q`

### **3. Log Only**
- No action, just logs the trigger
- Useful for testing

---

## **Tips & Best Practices**

### **✅ DO:**
- Use **Master-Slave** for loading screen protection
- Set **cooldowns** to prevent spam (1000ms = 1 second)
- Use **"No Match"** for detecting changes
- Test with **"Log Only"** first
- Use descriptive monitor names

### **❌ DON'T:**
- Set cooldown too low (causes spam)
- Monitor pixels that change constantly
- Use on always-changing colors (gradients, animations)
- Forget to pause monitors when done

---

## **Common Use Cases**

### **Example 1: Health Potion Bot**
```
Type: Normal Monitor
Pixel: Health bar (e.g., at 50% mark)
Trigger: No Match (pixel NOT red = health dropped)
Action: Press '1' (health potion key)
Cooldown: 5000ms (5 seconds)
```

### **Example 2: Loading Screen Protection**
```
Master Monitor:
  Name: "UI Visible"
  Pixels: 3 UI corners (All Match)
  Trigger: Match (all pixels = UI colors)
  Action: Log Only

Slave Monitors:
  All your game monitors linked to "UI Visible"
  → Only run when UI is actually visible
```

### **Example 3: Multi-Pixel Detection**
```
Type: Master Monitor
Pixels: 
  - Top-left UI corner
  - Top-right UI corner
  - Health bar location
Logic: All Match (all 3 must match)
Trigger: Match
Action: Log "UI Fully Loaded"
```

---

## **Troubleshooting**

### **Problem: "Port already in use"**
**Solution:** Pixel Bot automatically finds a free port. Check the console window to see which port is being used.

### **Problem: Monitor not triggering**
**Possible causes:**
1. **Wrong pixel location** → Re-pick the pixel
2. **Tolerance too low** → Increase tolerance (try 15-20)
3. **In cooldown** → Wait for cooldown to expire
4. **Master monitor inactive** → Check if master is blocking
5. **Wrong trigger mode** → Switch Match/No Match

### **Problem: Too many triggers (spam)**
**Solution:** Increase cooldown (e.g., 2000ms = 2 seconds)

### **Problem: Pixel picker not working**
**Solution:** 
- Make sure no other overlay apps are running
- Try running as Administrator
- Check console for errors

### **Problem: Actions not executing**
**Possible causes:**
1. **Game in fullscreen** → Try borderless windowed
2. **Admin privileges** → Run Pixel Bot as Administrator
3. **Wrong key name** → Check key spelling
4. **Cooldown active** → Wait and try again

---

## **Configuration File (Advanced)**

Create `pixelbot_config.ini` next to `PixelBot.exe`:

```ini
[server]
port = 5000

[monitoring]
check_interval = 0.1
default_tolerance = 10
default_cooldown = 1000

[advanced]
log_level = INFO
picker_timeout = 30
```

**Settings:**
- `check_interval`: 0.1 = 10 checks/sec (lower = faster, more CPU)
- `default_tolerance`: 0-255 (higher = more lenient matching)
- `default_cooldown`: Milliseconds between triggers

---

## **Keyboard Shortcuts**

| Key | Action |
|-----|--------|
| Click monitor name | Toggle pause/resume |
| - | - |

*More shortcuts coming soon!*

---

## **Known Limitations**

1. **Tesseract OCR**: Not included in standalone build. Install separately if using OCR features.
2. **Admin games**: Some games require Pixel Bot to run as Administrator
3. **Fullscreen**: Works best with borderless windowed mode
4. **Multiple monitors**: Pick pixels carefully - coordinates are global

---

## **FAQ**

**Q: Is this a virus?**
A: No! Antivirus may flag it (false positive) because PyInstaller executables are sometimes misidentified. You can check the source code or build it yourself.

**Q: Does this work with game X?**
A: Works with any game/app that displays on screen. Some anti-cheat systems may block it.

**Q: Can I run multiple instances?**
A: Yes! Each instance automatically uses a different port.

**Q: How do I stop it?**
A: Close the browser tab and the console window (or press Ctrl+C in console).

**Q: Where are my monitors saved?**
A: In `monitors_config.json` next to `PixelBot.exe` (auto-created).

**Q: Can I backup my monitors?**
A: Yes! Copy `monitors_config.json` to another location.

---

## **Support**

- **GitHub**: [Your GitHub repo URL]
- **Issues**: [GitHub Issues URL]
- **Logs**: Check the console window for detailed logs

---

## **Legal**

**Important:** Always check your game's Terms of Service before using automation tools. Some games prohibit automation and may ban accounts.

**Pixel Bot is provided as-is with no warranty. Use at your own risk.**

---

**Version:** 1.0.0
**Last Updated:** 2024

---

**Enjoy automating! 🚀**

