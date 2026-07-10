# Quick Start Guide - Personalized AI Lighting Controller

## 📋 Setup Checklist

### Step 1: Install Python (if not already installed)
- Download from: https://www.python.org/downloads/ (Python 3.8 or higher)
- **Important**: Check "Add Python to PATH" during installation
- Verify: Open Command Prompt and run `python --version`

### Step 2: Clone/Download This Project
```
Location: Your preferred folder
```

### Step 3: Install Dependencies
```bash
# Open Command Prompt or PowerShell in the project folder
pip install -r requirements.txt
```

**Note**: If `pyaudio` fails to install:
1. Download pre-built wheel: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
2. Install with: `pip install path\to\PyAudio-0.2.13-cp311-cp311-win_amd64.whl`

### Step 4: Make Sure OpenRGB is Running (Optional but Recommended)
- Download from: https://openrgb.org/
- Extract and run `OpenRGB.exe`
- Keep it running in the background

### Step 5: Test the Script
```bash
python lighting_ai.py
```

**Then speak commands like:**
- "Focus" - Blue lighting for concentration
- "Relax" - Purple calm lighting
- "Creative" - Red for creative mode
- "Bright" - Maximum brightness
- "Dim" - Low lighting

### Step 6: Install as Windows Startup Service (Optional)

**Run Command Prompt as Administrator**, then:
```bash
python service_installer.py install
```

This will make the lighting AI start automatically when you log in.

---

## 🎤 Voice Commands Reference

| What to Say | Effect |
|------------|--------|
| Focus, Work, Concentrate | 🔵 Blue - Focused mode |
| Relax, Chill, Calm | 🟣 Purple - Relaxed mode |
| Energy, Boost, Pump up | 🟢 Green - Energetic mode |
| Creative, Create, Design | 🔴 Red - Creative mode |
| Dim, Dark, Off | 🔲 Low brightness |
| Bright, Max, Full | 💡 Maximum brightness |

---

## 🔧 Hardware Setup

### For Corsair Keyboards
- Ensure Corsair iCUE is installed
- App will auto-detect and control

### For Razer Keyboards
- Install Razer Synapse
- RGB will be controlled automatically

### For ASUS ROG Keyboards
- Install ASUS ROG software
- Should work automatically

### For Other RGB Keyboards
- **Best option**: Use OpenRGB (works with most brands)
- Download: https://openrgb.org/
- Start OpenRGB and keep it running

---

## ❓ Troubleshooting

### Keyboard RGB not changing?
1. Make sure your keyboard manufacturer's software is running (Corsair iCUE, Razer Synapse, etc.)
2. OR run OpenRGB in the background
3. Check that your keyboard is actually RGB-enabled

### Voice commands not working?
1. Check microphone is enabled in Windows Sound settings
2. Speak clearly and pause between words
3. Make sure this app has permission to use microphone (Settings → Privacy)

### Service won't start?
1. Run Command Prompt as Administrator
2. Make sure Python is installed and in PATH
3. Check Task Scheduler to see if task appears

---

## 📚 Advanced

### Custom Time Schedules
Edit the `get_time_of_day()` function in `lighting_ai.py` to change:
- What time "morning" starts
- When "work" mode begins
- Evening lighting schedule

### Add Custom Moods
Edit the `Mood` enum to add new HSV colors and voice commands.

### Disable Voice Recognition
Edit `lighting_ai.py` and set `voice_enabled = False` to run without listening to audio.

---

Enjoy your personalized AI lighting! 🎨
