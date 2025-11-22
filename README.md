# FS-Code: A Modern Python IDE

<div align="center">

![Version](https://img.shields.io/badge/version-2.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

**A professional Python Integrated Development Environment with modern UI, syntax highlighting, and advanced features**

</div>

---

## ✨ Features

### 🎨 Modern User Interface
- **Dark Theme**: Professional VS Code-inspired dark color scheme
- **Syntax Highlighting**: Real-time Python syntax highlighting with color-coded keywords, strings, comments, functions, and numbers
- **Line Numbers**: Automatic line numbering for easy code navigation
- **Tabbed Interface**: Work on multiple files simultaneously with an intuitive tab system
- **Modern Toolbar**: Quick-access buttons with emoji icons for common operations

### 📝 Advanced Editor
- **Multiple File Support**: Open and edit multiple Python files in separate tabs
- **Smart File Operations**: Full support for New, Open, Save, and Save As operations
- **Undo/Redo**: Complete undo/redo functionality for all edits
- **Modified Indicator**: Visual asterisk (*) indicator for unsaved changes
- **Auto-saving Prompts**: Intelligent prompts to save changes before closing

### ⚡ Code Execution
- **Instant Execution**: Run Python code with F5 or the Run button
- **Colored Output**: Success messages in green, errors in red
- **Separate Console**: Dedicated output area for viewing execution results
- **Timeout Protection**: 30-second timeout to prevent infinite loops
- **Clear Output**: Quick clear button for the output console

### ⌨️ Keyboard Shortcuts
| Shortcut | Action |
|----------|--------|
| `Ctrl+N` | New File |
| `Ctrl+O` | Open File |
| `Ctrl+S` | Save File |
| `Ctrl+Shift+S` | Save As |
| `Ctrl+W` | Close Tab |
| `Ctrl+Z` | Undo |
| `Ctrl+Y` | Redo |
| `Ctrl+X/C/V` | Cut/Copy/Paste |
| `F5` | Run Code |
| `Ctrl+L` | Clear Output |
| `Ctrl+Q` | Quit Application |

### 🔧 Additional Features
- **Status Bar**: Real-time status updates and cursor position
- **Smart Menus**: Organized File, Edit, Run, and Help menus
- **Unsaved Changes Protection**: Warnings before closing unsaved files
- **Professional Fonts**: Consolas monospace font for optimal code readability
- **Window Management**: Resizable 1200x800 default window

---

## 📋 Requirements

- **Python 3.7+** (Python 3.8 or higher recommended)
- **Tkinter** (usually included with Python)
- **No external dependencies!** Uses only Python standard library

---

## 🚀 Installation & Usage

### Quick Start
```bash
# Clone or download the repository
git clone https://github.com/yourusername/fs-code.git
cd fs-code

# Run the IDE
python3 app.py
```

### Desktop Installation (Optional)
```bash
# Install as a desktop application
pip install -e .

# Run from anywhere
fs-code
```

### Building Standalone Executable
To create a standalone executable that doesn't require Python installation:

```bash
# Install PyInstaller
pip install pyinstaller

# Create standalone executable
pyinstaller --onefile --windowed --name="FS-Code" app.py

# The executable will be in the 'dist' folder
```

---

## 📖 How to Use

1. **Launch the IDE**: Run `python3 app.py` or use the installed executable
2. **Write Code**: Type your Python code in the editor (supports multiple tabs)
3. **Run Code**: Press `F5` or click the "▶ Run" button
4. **View Output**: Check the output console at the bottom
5. **Save Your Work**: Use `Ctrl+S` or the Save button
6. **Open Existing Files**: Use `Ctrl+O` to open Python files

### Example Workflow
```python
# Create a new file (Ctrl+N)
# Write some Python code
print("Hello, FS-Code!")
for i in range(5):
    print(f"Number: {i}")

# Run the code (F5)
# See the output in the console below
# Save your work (Ctrl+S)
```

---

## 🎯 Advanced Features Explained

### Syntax Highlighting
The editor automatically highlights:
- **Keywords** (if, for, while, def, class, etc.) in blue
- **Strings** in orange
- **Comments** in green
- **Functions** in yellow
- **Numbers** in light green
- **Built-in functions** (print, len, range, etc.) in cyan

### Tab Management
- Open multiple files in separate tabs
- Tab titles show the filename and modified status (*)
- Easy switching between files
- Automatic save prompts when closing modified tabs

### Professional UI
- **Dark Theme**: Easy on the eyes for long coding sessions
- **Modern Toolbar**: Quick access to common actions
- **Status Bar**: Shows current file and operation status
- **Line Numbers**: Helps with debugging and navigation

---

## 🛠️ Development

### Project Structure
```
fs-code/
├── app.py              # Main application file
├── setup.py            # Package setup for installation
├── requirements.txt    # Dependencies (none required!)
└── README.md          # This file
```

### Creating Desktop Shortcuts

**Windows:**
1. Right-click on `app.py`
2. Send to → Desktop (create shortcut)
3. Edit shortcut to run with `pythonw.exe app.py` for no console window

**Linux:**
Create a `.desktop` file:
```desktop
[Desktop Entry]
Name=FS-Code
Comment=Modern Python IDE
Exec=python3 /path/to/app.py
Icon=text-editor
Terminal=false
Type=Application
Categories=Development;IDE;
```

**macOS:**
Use Automator to create an Application that runs the Python script.

---

## 🔄 Version History

### Version 2.0 (Current)
- ✅ Complete UI overhaul with modern dark theme
- ✅ Syntax highlighting for Python code
- ✅ Line numbers with auto-scrolling
- ✅ Tabbed interface for multiple files
- ✅ Full file operations (New, Open, Save, Save As)
- ✅ Keyboard shortcuts for all major actions
- ✅ Status bar with real-time updates
- ✅ Professional toolbar with icons
- ✅ Undo/Redo functionality
- ✅ Smart unsaved changes handling
- ✅ Colored output console (errors in red, success in green)

### Version 1.0
- Basic text editor
- Simple code execution
- Basic UI with Run and Clear buttons

---

## 🎓 Future Enhancements

Potential features for future versions:
- [ ] Code auto-completion
- [ ] Find and Replace functionality
- [ ] Multiple programming language support
- [ ] Integrated debugger
- [ ] Plugin system
- [ ] Git integration
- [ ] Code snippets library
- [ ] Customizable themes
- [ ] Split-pane editing
- [ ] Project explorer sidebar

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2024 FABIAN TERES

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 👨‍💻 Author

**FABIAN TERES**

- Built with ❤️ using Python and Tkinter
- Inspired by modern IDEs like VS Code

---

## 🙏 Acknowledgments

- Python Software Foundation for the excellent Tkinter library
- The VS Code team for UI/UX inspiration
- All contributors and users of FS-Code

---

<div align="center">

**⭐ If you find this project useful, please consider giving it a star! ⭐**

Made with 💙 by FABIAN TERES

</div>