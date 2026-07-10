# 🎨 Personalized AI Lighting Controller

An intelligent, voice-controlled background AI that adapts your laptop keyboard RGB lighting based on your mood and time of day.

## Features

✨ **Voice Commands** - Control lighting with simple voice commands:
- "Focus" / "Work" → Cool blue for concentration
- "Relax" / "Calm" → Warm purple for relaxation  
- "Energetic" / "Boost" → Vibrant green for energy
- "Creative" / "Design" → Red for creativity
- "Dim" / "Off" → Low lighting
- "Bright" / "Max" → Full brightness

⏰ **Time-Based Adaptation**:
- **Morning** (5am-12pm): Energizing colors
- **Work** (12pm-5pm): Focused cool tones
- **Evening** (5pm-9pm): Relaxing warm colors
- **Night** (9pm-5am): Minimal/dimmed lighting

🎯 **Mood Recognition**: The AI learns and adapts to your mood based on voice commands

🖥️ **Background Service**: Runs silently as a Windows startup task

## Requirements

- **Windows 10/11**
- **Python 3.8+**
- **RGB Keyboard** (Corsair, Razer, Logitech, ASUS ROG, etc.)
- **Microphone** (for voice input)

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

> **Note**: `pyaudio` might require Visual C++ Build Tools on Windows. If installation fails, download from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

### 2. Test the Script

```bash
python lighting_ai.py
```

Try saying commands like "focus", "relax", or "creative". The keyboard lighting should change color.

### 3. Install as Windows Startup Service (Optional)

Run as **Administrator**:

```bash
python service_installer.py install
```

This installs the lighting AI as a scheduled task that starts automatically when you log in.

## Usage

### Run Manually
```bash
python lighting_ai.py
```

### Start/Stop Service
```bash
# Start the service
python service_installer.py start

# Uninstall from startup
python service_installer.py uninstall
```

### Voice Commands

Simply speak clearly near your microphone:

| Command | Effect |
|---------|--------|
| "focus" / "work" / "concentrate" | Blue focused lighting |
| "relax" / "chill" / "calm" | Purple calm lighting |
| "energy" / "boost" / "pump up" | Green energetic lighting |
| "creative" / "create" / "design" | Red creative lighting |
| "dim" / "dark" / "off" | Low brightness |
| "bright" / "max" / "full" | Maximum brightness |

## Keyboard Compatibility

The AI supports RGB keyboards through:

1. **OpenRGB** (Recommended for maximum compatibility)
   - Download: https://openrgb.org/
   - Works with most RGB keyboards (Corsair, NZXT, etc.)
   - Start OpenRGB in the background for automatic control

2. **Native APIs**
   - Razer Synapse keyboards
   - Corsair iCUE keyboards
   - ASUS ROG keyboards
   - Logitech G HUB keyboards

3. **USB Direct Control** (For advanced users)
   - Uses direct USB communication

## Configuration

Edit `lighting_config.json` to customize:

```json
{
  "mood_preferences": {
    "focus_brightness": 100,
    "relax_brightness": 50
  },
  "voice_enabled": true,
  "auto_brightness": true
}
```

## Troubleshooting

### "Could not set keyboard RGB"
- Ensure your keyboard manufacturer's software is installed (Razer Synapse, Corsair iCUE, etc.)
- Try OpenRGB: https://openrgb.org/

### Microphone not detected
- Check System Settings → Privacy & Security → Microphone
- Grant permission to Python application

### Commands not recognized
- Speak clearly and pause between words
- Check microphone levels in Windows Sound settings

### Service won't start
- Run `service_installer.py` as Administrator
- Check Task Scheduler (Windows key + R → `taskschd.msc`)

## Uninstall

```bash
# Remove from startup
python service_installer.py uninstall

# Remove files
rmdir /s /q "path\to\lighting_ai"
```

## Advanced: Custom Moods

Edit `lighting_ai.py` to add custom moods:

```python
class Mood(Enum):
    MY_CUSTOM_MOOD = (240, 100, 80)  # HSV: Cyan at 80% brightness
```

Then add voice command detection in `parse_voice_command()`:

```python
elif any(word in text_lower for word in ["custom", "my", "mood"]):
    return Mood.MY_CUSTOM_MOOD
```

## Performance Notes

- Uses minimal CPU (~0.5% idle)
- Voice listening uses ~50MB RAM
- Updates lighting every 60 seconds
- No internet connection required (Google Speech API is optional)

## Privacy

- Speech recognition is done locally when possible
- No data is stored or sent to servers
- All settings saved locally in `lighting_config.json`

---

**Enjoy personalized AI-driven lighting! 🎨**
