#!/usr/bin/env python3
"""
Build script for creating standalone executables of FS-Code
Supports Windows, Linux, and macOS
"""

import os
import sys
import subprocess
import platform

def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller
        return True
    except ImportError:
        return False

def install_pyinstaller():
    """Install PyInstaller"""
    print("Installing PyInstaller...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    print("PyInstaller installed successfully!")

def build_executable():
    """Build the standalone executable"""
    system = platform.system()
    
    print(f"\n{'='*60}")
    print(f"Building FS-Code for {system}")
    print(f"{'='*60}\n")
    
    # Base command
    cmd = [
        "pyinstaller",
        "--onefile",           # Create a single executable
        "--windowed",          # No console window (GUI app)
        "--name=FS-Code",      # Name of the executable
        "--clean",             # Clean PyInstaller cache
    ]
    
    # Add icon if available
    if system == "Windows" and os.path.exists("icon.ico"):
        cmd.append("--icon=icon.ico")
    elif system == "Darwin" and os.path.exists("icon.icns"):
        cmd.append("--icon=icon.icns")
    
    # Add the main script
    cmd.append("app.py")
    
    print(f"Running: {' '.join(cmd)}\n")
    
    try:
        subprocess.check_call(cmd)
        print(f"\n{'='*60}")
        print("Build completed successfully!")
        print(f"{'='*60}")
        print(f"\nExecutable location: dist/FS-Code{'.exe' if system == 'Windows' else ''}")
        print("\nYou can now distribute the executable in the 'dist' folder.")
        
        if system == "Linux":
            print("\nFor Linux, you may also want to create a .desktop file.")
            print("See the README for instructions.")
        elif system == "Darwin":
            print("\nFor macOS, the app bundle is ready for distribution.")
        
    except subprocess.CalledProcessError as e:
        print(f"\nError during build: {e}")
        sys.exit(1)

def main():
    """Main build function"""
    print("FS-Code Build Script")
    print("=" * 60)
    
    # Check and install PyInstaller if needed
    if not check_pyinstaller():
        print("PyInstaller not found.")
        response = input("Would you like to install it? (y/n): ")
        if response.lower() == 'y':
            install_pyinstaller()
        else:
            print("Cannot build without PyInstaller. Exiting.")
            sys.exit(1)
    
    # Build the executable
    build_executable()

if __name__ == "__main__":
    main()
