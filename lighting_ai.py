"""
Personalized AI Lighting Controller for Windows
Listens to voice commands and controls keyboard RGB lighting based on mood and time
"""

import os
import sys
import json
import time
import threading
import subprocess
from datetime import datetime
from pathlib import Path
import speech_recognition as sr
from colorsys import hsv_to_rgb
import requests
from enum import Enum

class Mood(Enum):
    """Mood states for lighting"""
    FOCUSED = (200, 100, 100)      # Cool blue
    RELAXED = (30, 100, 100)       # Warm amber
    ENERGETIC = (120, 100, 100)    # Vibrant green
    CALM = (270, 50, 100)          # Soft purple
    CREATIVE = (0, 100, 100)       # Vibrant red
    DEFAULT = (0, 0, 50)           # Dim white

class TimeOfDay(Enum):
    """Time-based lighting profiles"""
    MORNING = "morning"      # Energizing
    WORK = "work"            # Focused
    EVENING = "evening"      # Relaxing
    NIGHT = "night"          # Minimal/off

class LightingController:
    def __init__(self):
        self.current_mood = Mood.DEFAULT
        self.current_brightness = 50
        self.is_running = True
        self.recognizer = sr.Recognizer()
        self.config_file = Path(__file__).parent / "lighting_config.json"
        self.load_config()
        
    def load_config(self):
        """Load saved preferences"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {
                "mood_preferences": {},
                "voice_enabled": True,
                "auto_brightness": True
            }
            self.save_config()
    
    def save_config(self):
        """Save preferences"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get_time_of_day(self):
        """Determine current time period"""
        hour = datetime.now().hour
        if 5 <= hour < 12:
            return TimeOfDay.MORNING
        elif 12 <= hour < 17:
            return TimeOfDay.WORK
        elif 17 <= hour < 21:
            return TimeOfDay.EVENING
        else:
            return TimeOfDay.NIGHT
    
    def parse_voice_command(self, text):
        """Parse voice commands to mood/color"""
        text_lower = text.lower()
        
        # Mood detection
        if any(word in text_lower for word in ["focus", "work", "concentrate"]):
            return Mood.FOCUSED
        elif any(word in text_lower for word in ["relax", "chill", "calm"]):
            return Mood.CALM
        elif any(word in text_lower for word in ["energy", "boost", "pump up"]):
            return Mood.ENERGETIC
        elif any(word in text_lower for word in ["creative", "create", "design"]):
            return Mood.CREATIVE
        elif any(word in text_lower for word in ["dim", "off", "dark"]):
            self.current_brightness = 10
            return Mood.DEFAULT
        elif any(word in text_lower for word in ["bright", "max", "full"]):
            self.current_brightness = 100
            return Mood.DEFAULT
        
        return None
    
    def listen_for_commands(self):
        """Background thread to listen for voice commands"""
        print("[Listening...] Say commands like: 'focus', 'relax', 'creative', 'dim', 'bright'")
        
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            while self.is_running:
                try:
                    # Listen with timeout
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                    
                    # Recognize speech
                    text = self.recognizer.recognize_google(audio)
                    print(f"[Command heard] {text}")
                    
                    mood = self.parse_voice_command(text)
                    if mood:
                        self.set_mood(mood)
                        
                except sr.UnknownValueError:
                    pass  # Couldn't understand
                except sr.RequestError:
                    pass  # API error
                except sr.WaitTimeoutError:
                    pass  # No speech detected
                except Exception as e:
                    print(f"[Error] {e}")
    
    def set_mood(self, mood):
        """Set lighting mood"""
        self.current_mood = mood
        self.apply_lighting()
    
    def apply_lighting(self):
        """Apply current mood + time-of-day to lighting"""
        time_period = self.get_time_of_day()
        
        # Adjust brightness by time
        brightness = self.current_brightness
        if time_period == TimeOfDay.NIGHT:
            brightness = min(brightness, 20)  # Dim at night
        elif time_period == TimeOfDay.MORNING:
            brightness = min(brightness, 100)  # Full in morning
        
        h, s, v = self.current_mood.value
        v = brightness
        
        # Convert HSV to RGB
        r, g, b = hsv_to_rgb(h/360, s/100, v/100)
        r, g, b = int(r*255), int(g*255), int(b*255)
        
        self.set_keyboard_color(r, g, b)
        print(f"[Lighting] Mood: {self.current_mood.name}, Time: {time_period.value}, RGB: ({r},{g},{b})")
    
    def set_keyboard_color(self, r, g, b):
        """
        Set keyboard RGB color.
        This uses generic approaches for common keyboards.
        """
        try:
            # Try OpenRGB (works with most RGB keyboards on Windows)
            self.set_openrgb_color(r, g, b)
        except:
            try:
                # Fallback: Try direct WMI for some keyboard models
                self.set_wmi_color(r, g, b)
            except:
                print(f"[Warning] Could not set keyboard RGB. Ensure your keyboard is supported.")
    
    def set_openrgb_color(self, r, g, b):
        """Use OpenRGB daemon if available"""
        try:
            # This requires OpenRGB to be running
            # Common endpoint for OpenRGB REST API
            response = requests.post(
                "http://localhost:6742/api/v1/devices/0/colors",
                json={"mode": "static", "red": r, "green": g, "blue": b},
                timeout=1
            )
            if response.status_code == 200:
                print("[RGB Control] OpenRGB updated")
        except:
            raise
    
    def set_wmi_color(self, r, g, b):
        """Try Windows native RGB control (Razer, Corsair, etc.)"""
        try:
            # For Razer keyboards
            hex_color = f"{r:02x}{g:02x}{b:02x}"
            subprocess.run(
                ["powershell", "-Command", f"Set-ItemProperty -Path 'HKCU:\\Software\\Razer\\ChromaSDK\\Color' -Name 'CurrentColor' -Value '0x{hex_color}'"],
                capture_output=True,
                timeout=2
            )
        except:
            raise
    
    def start(self):
        """Start the lighting AI"""
        print("🎨 Personalized AI Lighting Controller Started")
        print("=" * 50)
        
        # Start voice listener in background thread
        listener_thread = threading.Thread(target=self.listen_for_commands, daemon=True)
        listener_thread.start()
        
        # Main loop for time-based adjustments
        try:
            while self.is_running:
                self.apply_lighting()
                time.sleep(60)  # Update every minute
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stop the controller"""
        print("\n🎨 Lighting Controller Stopped")
        self.is_running = False
        sys.exit(0)


if __name__ == "__main__":
    controller = LightingController()
    controller.start()
