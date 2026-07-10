"""
Install and manage Lighting AI as Windows Background Service
Run as Administrator: python service_installer.py install
"""

import sys
import os
import subprocess
from pathlib import Path

class LightingAIService:
    SERVICE_NAME = "LightingAI"
    SERVICE_DISPLAY = "AI Lighting Controller"
    
    @staticmethod
    def get_script_path():
        """Get path to the main script"""
        return Path(__file__).parent / "lighting_ai.py"
    
    @staticmethod
    def check_admin():
        """Check if running as administrator"""
        try:
            return os.getuid() == 0
        except AttributeError:
            import ctypes
            return ctypes.windll.shell.IsUserAnAdmin()
    
    @classmethod
    def install(cls):
        """Install as Windows service"""
        if not cls.check_admin():
            print("❌ Please run as Administrator!")
            sys.exit(1)
        
        script_path = cls.get_script_path()
        python_path = sys.executable
        
        try:
            # Create NSSM wrapper or use python-service-win
            # For simplicity, we'll use a scheduled task instead
            
            cmd = [
                "powershell", "-Command",
                f"$action = New-ScheduledTaskAction -Execute '{python_path}' -Argument '{script_path}' -WorkingDirectory '{script_path.parent}';"
                f"$trigger = New-ScheduledTaskTrigger -AtLogon;"
                f"Register-ScheduledTask -TaskName '{cls.SERVICE_NAME}' -Action $action -Trigger $trigger -RunLevel Highest -Force"
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ {cls.SERVICE_DISPLAY} installed as startup task!")
            print(f"   Service will start automatically on next login.")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Installation failed: {e.stderr.decode()}")
            sys.exit(1)
    
    @classmethod
    def uninstall(cls):
        """Remove from Windows services"""
        if not cls.check_admin():
            print("❌ Please run as Administrator!")
            sys.exit(1)
        
        try:
            cmd = [
                "powershell", "-Command",
                f"Unregister-ScheduledTask -TaskName '{cls.SERVICE_NAME}' -Confirm:$false"
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ {cls.SERVICE_DISPLAY} uninstalled!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Uninstall failed: {e.stderr.decode()}")
            sys.exit(1)
    
    @classmethod
    def start(cls):
        """Start the service"""
        if not cls.check_admin():
            print("❌ Please run as Administrator!")
            sys.exit(1)
        
        try:
            cmd = [
                "powershell", "-Command",
                f"Start-ScheduledTask -TaskName '{cls.SERVICE_NAME}'"
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ {cls.SERVICE_DISPLAY} started!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to start: {e.stderr.decode()}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python service_installer.py [install|uninstall|start]")
        print(f"\nExamples:")
        print(f"  python service_installer.py install    # Install as startup service")
        print(f"  python service_installer.py start      # Start the service now")
        print(f"  python service_installer.py uninstall  # Remove the service")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "install":
        LightingAIService.install()
    elif command == "uninstall":
        LightingAIService.uninstall()
    elif command == "start":
        LightingAIService.start()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
