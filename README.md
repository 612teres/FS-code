# FS-code: Desktop Python IDE

FS-code is a lightweight Tk/ttk-based desktop IDE tailored for quick Python experiments. It ships with file management, a dual-pane layout, dark/light themes, and a non-blocking runner so you can edit and execute code without leaving the app.

## Highlights

- Modern toolbar + menu bar with New/Open/Save/Run controls
- Resizable split interface for the editor and output console
- Built-in process manager with Run (F5) and Stop (F6) plus status feedback
- Light/dark theme toggle, adjustable editor font size, and read-only output view
- Keyboard shortcuts for common actions and a status bar with caret + file info

## Requirements

- Python 3.10+ (ships with Tk on most platforms)
- No external dependencies for running from source

## Run from Source

```bash
python3 app.py
```

## Keyboard Shortcuts

- `Ctrl + N` New file
- `Ctrl + O` Open file
- `Ctrl + S` Save
- `Ctrl + Shift + S` Save As
- `Ctrl + T` Toggle theme
- `F5` Run current buffer
- `F6` Stop running process

## Package as a Desktop App

1. Install PyInstaller (once):
   ```bash
   python3 -m pip install pyinstaller
   ```
2. Build the application bundle:
   ```bash
   pyinstaller --name FS-code --windowed --noconfirm app.py
   ```
3. Distribute the generated executable:
   - macOS: `dist/FS-code.app`
   - Windows: `dist/FS-code/FS-code.exe`
   - Linux: `dist/FS-code`

You can adjust the PyInstaller flags (icon, splash screen, signing) to match your platform requirements.


##  UI Preview (Text Description)

```
┌─────────────────────────────────────────────────────┐
│  FS-Code - Modern Python IDE                        │
├─────────────────────────────────────────────────────┤
│  File  Edit  Run  Help                              │
├─────────────────────────────────────────────────────┤
│ [📄 New] [📁 Open] [💾 Save] │ [▶ Run] [🗑️ Clear]   │
├─────────────────────────────────────────────────────┤
│ [Untitled] [script.py] [*test.py]  ← Tabs          │
├───┬─────────────────────────────────────────────────┤
│ 1 │ def hello():                    ← Line Numbers │
│ 2 │     print("Hello, World!")      ← Syntax       │
│ 3 │                                 ← Highlighting │
│ 4 │ hello()                                         │
│ 5 │                                                 │
│   │                                                 │
├───┴─────────────────────────────────────────────────┤
│ Output Console                                      │
├─────────────────────────────────────────────────────┤
│ Hello, World!                       ← Green output │
│                                                     │
├─────────────────────────────────────────────────────┤
│ Ready - Press F5 to run code        │ Ln 1, Col 1  │
└─────────────────────────────────────────────────────┘
```

## Next Steps (Optional Enhancements)

If you want to add more features later:

1. **Find & Replace** - Ctrl+F functionality
2. **Auto-completion** - Code suggestions
3. **Debugger** - Breakpoints and stepping
4. **Git Integration** - Version control
5. **Themes** - Light mode, custom colors
6. **Multi-language** - JavaScript, C++, etc.
7. **Terminal** - Integrated command line
8. **Project Explorer** - Sidebar file browser
9. **Plugins** - Extension system
10. **Minimap** - Code overview

The architecture supports all of these!

---

## Contributing

Issues and pull requests are welcome. Feel free to propose UI ideas, syntax-highlighting integrations, or platform-specific installers.

## License

MIT © Fabian Teres