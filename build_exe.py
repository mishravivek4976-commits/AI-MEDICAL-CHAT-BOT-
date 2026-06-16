"""
Script to build Windows EXE file from the FastAPI app
Run: python build_exe.py
"""

import os
import subprocess
import sys

def build_exe():
    """Build executable using PyInstaller"""
    
    print("🔨 Building EXE file...")
    print("-" * 50)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("❌ PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Build command
    command = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=MedicalChatbot",
        "--icon=chatbot.ico" if os.path.exists("chatbot.ico") else "",
        "--add-data=.env:." if os.path.exists(".env") else "",
        "app.py"
    ]
    
    # Remove empty strings
    command = [c for c in command if c]
    
    print(f"Command: {' '.join(command)}")
    print("-" * 50)
    
    try:
        subprocess.run(command, check=True)
        print("\n✅ EXE build successful!")
        print(f"📁 Location: dist/MedicalChatbot.exe")
        print("\n📋 Instructions:")
        print("1. Navigate to 'dist' folder")
        print("2. Double-click 'MedicalChatbot.exe' to run")
        print("3. Your browser will open with the chatbot")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build_exe()
