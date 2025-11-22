# FS-Code Installation Guide

Complete guide for installing and running FS-Code on different platforms.

---

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Installation Methods](#installation-methods)
  - [Method 1: Run Directly (Recommended for Development)](#method-1-run-directly)
  - [Method 2: Install as Python Package](#method-2-install-as-python-package)
  - [Method 3: Build Standalone Executable](#method-3-build-standalone-executable)
- [Platform-Specific Instructions](#platform-specific-instructions)
  - [Windows](#windows)
  - [Linux](#linux)
  - [macOS](#macos)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required
- **Python 3.7 or higher** (3.8+ recommended)
- **Tkinter** (usually comes with Python)

### Optional (for building executables)
- **PyInstaller** (install via: `pip install pyinstaller`)

### Verify Installation

```bash
# Check Python version
python3 --version

# Check if Tkinter is available
python3 -c "import tkinter; print('Tkinter is installed')"
```

---

## Quick Start

The fastest way to run FS-Code:

```bash
# Download/clone the repository
git clone https://github.com/yourusername/fs-code.git
cd fs-code

# Run the IDE
python3 app.py
```

That's it! FS-Code should now be running.

---

## Installation Methods

### Method 1: Run Directly

**Best for:** Development, testing, quick usage

```bash
# Navigate to the FS-Code directory
cd /path/to/fs-code

# Run the application
python3 app.py
```

**Pros:**
- No installation needed
- Easy to modify code
- Instant updates

**Cons:**
- Need to navigate to directory each time
- Requires Python installed

---

### Method 2: Install as Python Package

**Best for:** Regular use, system-wide access

```bash
# Navigate to the FS-Code directory
cd /path/to/fs-code

# Install in development mode
pip install -e .

# Now run from anywhere
fs-code
```

**Pros:**
- Run from anywhere with `fs-code` command
- Easy to uninstall: `pip uninstall fs-code`
- Updates automatically in dev mode

**Cons:**
- Still requires Python installed

---

### Method 3: Build Standalone Executable

**Best for:** Distribution, users without Python

```bash
# Use the provided build script
python3 build.py

# Or manually with PyInstaller:
pip install pyinstaller
pyinstaller --onefile --windowed --name="FS-Code" app.py

# The executable will be in: dist/FS-Code
```

**Pros:**
- No Python installation required for end users
- Single file distribution
- Professional deployment

**Cons:**
- Larger file size (includes Python runtime)
- Separate build for each platform
- Takes time to build

---

## Platform-Specific Instructions

### Windows

#### Option A: Run with Python

1. **Install Python:**
   - Download from [python.org](https://www.python.org/downloads/)
   - ✅ Check "Add Python to PATH" during installation
   - Install with default settings

2. **Run FS-Code:**
   ```cmd
   cd C:\path\to\fs-code
   python app.py
   ```

#### Option B: Create Desktop Shortcut

1. Right-click on `app.py`
2. Create shortcut
3. Right-click shortcut → Properties
4. Change Target to: `C:\Python3X\pythonw.exe "C:\path\to\fs-code\app.py"`
5. Change "Start in" to: `C:\path\to\fs-code`
6. Optional: Add an icon

#### Option C: Build Executable

```cmd
python build.py
```

The `.exe` file will be in the `dist` folder.

---

### Linux

#### Option A: Run with Python

```bash
# Python and Tkinter should be pre-installed
# If not, install via:
sudo apt-get install python3 python3-tk    # Ubuntu/Debian
sudo dnf install python3 python3-tkinter   # Fedora
sudo pacman -S python python-tk            # Arch

# Run FS-Code
cd ~/fs-code
python3 app.py
```

#### Option B: Create Application Launcher

1. **Edit the desktop file:**
   ```bash
   nano fs-code.desktop
   ```

2. **Update the Exec path:**
   ```
   Exec=python3 /home/yourusername/fs-code/app.py
   ```

3. **Install the launcher:**
   ```bash
   cp fs-code.desktop ~/.local/share/applications/
   chmod +x ~/.local/share/applications/fs-code.desktop
   ```

4. **Update application menu:**
   ```bash
   update-desktop-database ~/.local/share/applications/
   ```

Now FS-Code will appear in your application menu!

#### Option C: Create Bash Alias

Add to `~/.bashrc` or `~/.zshrc`:

```bash
alias fs-code='python3 /path/to/fs-code/app.py'
```

Then run with: `fs-code`

---

### macOS

#### Option A: Run with Python

```bash
# Python 3 should be pre-installed
# If not, install via Homebrew:
brew install python-tk

# Run FS-Code
cd ~/fs-code
python3 app.py
```

#### Option B: Create Application Bundle

1. **Use Automator:**
   - Open Automator
   - Create new "Application"
   - Add "Run Shell Script" action
   - Enter: `python3 /path/to/fs-code/app.py`
   - Save as "FS-Code.app"

2. **Or build with PyInstaller:**
   ```bash
   python3 build.py
   ```
   
The app bundle will be in the `dist` folder.

#### Option C: Create Bash Alias

Add to `~/.zshrc`:

```bash
alias fs-code='python3 /path/to/fs-code/app.py'
```

---

## Troubleshooting

### Issue: "tkinter not found"

**Solution:**
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# macOS
brew install python-tk

# Windows
Reinstall Python with "tcl/tk and IDLE" option checked
```

### Issue: "python3: command not found"

**Solution:**
- Try `python` instead of `python3`
- Or add Python to your PATH environment variable

### Issue: "No module named 'tkinter'"

**Solution:**
- On Linux: Install `python3-tk`
- On macOS: Ensure you're using the official Python, not system Python
- On Windows: Reinstall Python with all options

### Issue: Fonts don't look good

**Solution:**
- On Windows: The default fonts should work
- On Linux: Install Microsoft fonts: `sudo apt-get install ttf-mscorefonts-installer`
- Or edit `app.py` to use different fonts available on your system

### Issue: High DPI scaling issues

**Solution:**
Add this to the beginning of `app.py` (after imports):

```python
# For Windows
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)
```

### Issue: Executable too large

**Solution:**
- The executable includes Python runtime (~20-40 MB)
- This is normal for PyInstaller executables
- Use UPX to compress: `pyinstaller --onefile --upx-dir=/path/to/upx app.py`

---

## Uninstallation

### If installed as package:
```bash
pip uninstall fs-code
```

### If run directly:
Just delete the directory:
```bash
rm -rf /path/to/fs-code
```

### Remove desktop entries (Linux):
```bash
rm ~/.local/share/applications/fs-code.desktop
update-desktop-database ~/.local/share/applications/
```

---

## Getting Help

If you encounter issues:

1. Check this guide thoroughly
2. Look at the main [README.md](README.md)
3. Open an issue on GitHub with:
   - Your OS and version
   - Python version (`python3 --version`)
   - Error message (full output)
   - What you've tried

---

**Happy Coding with FS-Code! 🚀**
