import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox, font
import subprocess
import re
import os
from pathlib import Path


class SyntaxHighlightedText(tk.Text):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Define syntax highlighting tags with vibrant colors
        self.tag_configure("keyword", foreground="#569CD6")      # Blue - keywords
        self.tag_configure("string", foreground="#CE9178")     # Orange - strings
        self.tag_configure("comment", foreground="#6A9955")      # Green - comments
        self.tag_configure("function", foreground="#DCDCAA")     # Yellow - function names
        self.tag_configure("number", foreground="#B5CEA8")      # Light green - numbers
        self.tag_configure("builtin", foreground="#4EC9B0")      # Cyan - built-ins
        self.tag_configure("class", foreground="#4EC9B0")       # Cyan - class names
        self.tag_configure("operator", foreground="#D4D4D4")      # Light gray - operators
        self.tag_configure("decorator", foreground="#C586C0")   # Purple - decorators
        
        # Bind events to trigger highlighting
        self.bind("<KeyRelease>", lambda e: self.after_idle(self._highlight_syntax))
        self.bind("<ButtonRelease>", lambda e: self.after_idle(self._highlight_syntax))
        self.bind("<<Modified>>", lambda e: self.after_idle(self._highlight_syntax))
        
    def _highlight_syntax(self, event=None):
        """Apply comprehensive syntax highlighting to the text"""
        # Remove all tags first
        for tag in ["keyword", "string", "comment", "function", "number", "builtin", "class", "operator", "decorator"]:
            self.tag_remove(tag, "1.0", tk.END)
        
        code = self.get("1.0", tk.END)
        if not code.strip():
            return
        
        # Process line by line for better accuracy
        lines = code.split('\n')
        char_offset = 0
        
        for line_num, line in enumerate(lines):
            line_start = char_offset
            line_end = char_offset + len(line)
            
            # Comments (must be first to avoid highlighting inside strings)
            comment_match = re.search(r'#.*$', line)
            if comment_match:
                start_pos = line_start + comment_match.start()
                end_pos = line_start + comment_match.end()
                self.tag_add("comment", f"1.0 + {start_pos} chars", f"1.0 + {end_pos} chars")
            
            # Strings (single and double quotes, including triple quotes)
            string_patterns = [
                (r'""".*?"""', re.DOTALL),  # Triple double quotes
                (r"'''.*?'''", re.DOTALL),  # Triple single quotes
                (r'"[^"]*"', 0),            # Double quotes
                (r"'[^']*'", 0),            # Single quotes
            ]
            for pattern, flags in string_patterns:
                for match in re.finditer(pattern, line, flags):
                    start_pos = line_start + match.start()
                    end_pos = line_start + match.end()
                    self.tag_add("string", f"1.0 + {start_pos} chars", f"1.0 + {end_pos} chars")
            
            # Decorators
            decorator_match = re.search(r'@\w+', line)
            if decorator_match:
                start_pos = line_start + decorator_match.start()
                end_pos = line_start + decorator_match.end()
                self.tag_add("decorator", f"1.0 + {start_pos} chars", f"1.0 + {end_pos} chars")
            
            # Keywords (Python reserved words)
            keywords = r'\b(and|as|assert|async|await|break|class|continue|def|del|elif|else|except|False|finally|for|from|global|if|import|in|is|lambda|None|nonlocal|not|or|pass|raise|return|True|try|while|with|yield)\b'
            for match in re.finditer(keywords, line):
                start_pos = line_start + match.start()
                end_pos = line_start + match.end()
                self.tag_add("keyword", f"1.0 + {start_pos} chars", f"1.0 + {end_pos} chars")
            
            # Class definitions
            class_match = re.search(r'\bclass\s+(\w+)', line)
            if class_match:
                start_pos = line_start + class_match.start(1)
                end_pos = line_start + class_match.end(1)
                self.tag_add("class", f"1.0 + {start_pos} chars", f"1.0 + {end_pos} chars")
            
            # Function definitions
            func_match = re.search(r'\bdef\s+(\w+)', line)
            if func_match:
                start_pos = line_start + func_match.start(1)
                end_pos = line_start + func_match.end(1)
                self.tag_add("function", f"1.0 + {start_pos} chars", f"1.0 + {end_pos} chars")
            
            # Built-in functions and types
            builtins = r'\b(print|len|range|str|int|float|bool|list|dict|set|tuple|open|input|type|isinstance|enumerate|zip|map|filter|sum|max|min|abs|round|sorted|reversed|iter|next|any|all|bin|hex|oct|ord|chr|repr|eval|exec|compile|hash|id|vars|dir|hasattr|getattr|setattr|delattr|isinstance|issubclass|super|property|staticmethod|classmethod)\b'
            for match in re.finditer(builtins, line):
                start_pos = line_start + match.start()
                end_pos = line_start + match.end()
                self.tag_add("builtin", f"1.0 + {start_pos} chars", f"1.0 + {end_pos} chars")
            
            # Numbers (integers, floats, hex, binary)
            numbers = r'\b(0x[0-9a-fA-F]+|0b[01]+|\d+\.?\d*)\b'
            for match in re.finditer(numbers, line):
                start_pos = line_start + match.start()
                end_pos = line_start + match.end()
                self.tag_add("number", f"1.0 + {start_pos} chars", f"1.0 + {end_pos} chars")
            
            # Operators
            operators = r'[+\-*/%=<>!&|^~]'
            for match in re.finditer(operators, line):
                start_pos = line_start + match.start()
                end_pos = line_start + match.end()
                self.tag_add("operator", f"1.0 + {start_pos} chars", f"1.0 + {end_pos} chars")
            
            char_offset = line_end + 1  # +1 for newline character


class Terminal(tk.Frame):
    """Terminal widget for running shell commands with Linux support"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.command_history = []
        self.history_index = -1
        self.current_directory = Path.cwd()
        self.shell = self._detect_linux_shell()
        self.is_windows = os.name == 'nt'
        
        # Create terminal header
        header = tk.Frame(self, bg="#2d2d30", height=30)
        header.pack(fill=tk.X)
        tk.Label(header, text="Terminal", bg="#2d2d30", fg="#cccccc", 
                font=("Segoe UI", 9, "bold"), anchor=tk.W, padx=10).pack(side=tk.LEFT, fill=tk.Y)
        
        # Terminal output area
        output_frame = tk.Frame(self)
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        self.output = tk.Text(
            output_frame,
            wrap=tk.WORD,
            bg="#1e1e1e",
            fg="#cccccc",
            font=("Consolas", 10),
            borderwidth=0,
            highlightthickness=0,
            padx=10,
            pady=10,
            state=tk.DISABLED,
        )
        self.output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar for terminal output
        scrollbar = AutoHideScrollbar(output_frame, command=self.output.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output.configure(yscrollcommand=scrollbar.set)
        
        # Command input area
        input_frame = tk.Frame(self, bg="#252526", height=35)
        input_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        prompt_label = tk.Label(input_frame, text=">", bg="#252526", fg="#569cd6", 
                font=("Consolas", 11, "bold"))
        prompt_label.pack(side=tk.LEFT, padx=(10, 5))
        
        self.input_entry = tk.Entry(
            input_frame,
            bg="#1e1e1e",
            fg="#cccccc",
            insertbackground="#cccccc",
            font=("Consolas", 10),
            borderwidth=0,
            relief=tk.FLAT,
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), pady=5)
        self.input_entry.bind("<Return>", self._execute_command)
        self.input_entry.bind("<Up>", self._history_up)
        self.input_entry.bind("<Down>", self._history_down)
        
        # Show initial prompt
        shell_info = f"Using: {self.shell['name']}" if self.shell else "Using: Default shell"
        self._write_output(f"Terminal ready. Current directory: {self.current_directory}\n", "info")
        self._write_output(f"{shell_info}\n", "info")
        self._write_output("Type 'help' for available commands.\n\n", "info")
        self._show_prompt()
    
    def _detect_linux_shell(self):
        """Detect available Linux-compatible shell on Windows"""
        if os.name != 'nt':
            # Already on Linux/Unix
            return {'name': 'bash', 'command': ['bash', '-c'], 'available': True}
        
        # Check for WSL
        try:
            result = subprocess.run(['wsl', '--list', '--quiet'], 
                                  capture_output=True, timeout=2)
            if result.returncode == 0:
                return {'name': 'WSL', 'command': ['wsl'], 'available': True}
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        
        # Check for Git Bash
        git_bash_paths = [
            r"C:\Program Files\Git\bin\bash.exe",
            r"C:\Program Files (x86)\Git\bin\bash.exe",
            r"C:\Program Files\Git\usr\bin\bash.exe",
        ]
        for path in git_bash_paths:
            if os.path.exists(path):
                return {'name': 'Git Bash', 'command': [path], 'available': True}
        
        # Check for MSYS2
        msys2_paths = [
            r"C:\msys64\usr\bin\bash.exe",
            r"C:\msys32\usr\bin\bash.exe",
        ]
        for path in msys2_paths:
            if os.path.exists(path):
                return {'name': 'MSYS2', 'command': [path], 'available': True}
        
        # No Linux shell found, will use command mapping
        return {'name': 'Windows CMD (with Linux command mapping)', 'command': None, 'available': False}
    
    def _write_output(self, text, tag="normal"):
        """Write text to terminal output"""
        self.output.configure(state=tk.NORMAL)
        self.output.insert(tk.END, text, tag)
        self.output.see(tk.END)
        self.output.configure(state=tk.DISABLED)
    
    def _show_prompt(self):
        """Show command prompt"""
        prompt = f"{self.current_directory}> "
        self._write_output(prompt, "prompt")
    
    def _execute_command(self, event=None):
        """Execute the entered command"""
        command = self.input_entry.get().strip()
        if not command:
            return
        
        # Add to history
        if command and (not self.command_history or self.command_history[-1] != command):
            self.command_history.append(command)
        self.history_index = len(self.command_history)
        
        # Display command
        self._write_output(f"{command}\n", "command")
        
        # Clear input
        self.input_entry.delete(0, tk.END)
        
        # Handle special commands
        if command.lower() == "help":
            self._show_help()
        elif command.lower() == "clear" or command.lower() == "cls":
            self.output.configure(state=tk.NORMAL)
            self.output.delete("1.0", tk.END)
            self.output.configure(state=tk.DISABLED)
            self._show_prompt()
        elif command.startswith("cd "):
            self._change_directory(command[3:].strip())
        else:
            # Execute system command
            self._run_command(command)
    
    def _map_linux_command(self, command):
        """Map Linux commands to Windows equivalents if no Linux shell is available"""
        if self.shell and self.shell['available']:
            return command  # Use Linux shell directly
        
        # Command mapping for Windows
        cmd_parts = command.split()
        if not cmd_parts:
            return command
        
        cmd = cmd_parts[0].lower()
        args = ' '.join(cmd_parts[1:]) if len(cmd_parts) > 1 else ''
        
        # Map common Linux commands to Windows
        command_map = {
            'ls': f'dir /b {args}' if args else 'dir /b',
            'll': f'dir {args}' if args else 'dir',
            'pwd': 'cd',
            'cat': f'type {args}' if args else 'type',
            'grep': f'findstr {args}' if args else 'findstr',
            'which': f'where {args}' if args else 'where',
            'rm': f'del {args}' if args else 'del',
            'rmdir': f'rmdir {args}' if args else 'rmdir',
            'mv': f'move {args}' if args else 'move',
            'cp': f'copy {args}' if args else 'copy',
            'touch': f'type nul > {args}' if args else 'type nul',
            'clear': 'cls',
        }
        
        if cmd in command_map:
            return command_map[cmd]
        return command
    
    def _run_command(self, command):
        """Run a system command with Linux support"""
        try:
            # Map Linux commands if needed
            if self.is_windows and (not self.shell or not self.shell['available']):
                command = self._map_linux_command(command)
            
            # Use Linux shell if available
            if self.shell and self.shell['available']:
                if self.shell['name'] == 'WSL':
                    # WSL command
                    full_command = self.shell['command'] + ['bash', '-c', 
                        f"cd '{self.current_directory}' && {command}"]
                elif 'bash' in self.shell['name'].lower():
                    # Git Bash or MSYS2
                    full_command = self.shell['command'] + ['-c', 
                        f"cd '{self.current_directory}' && {command}"]
                else:
                    full_command = command
                    shell = True
            else:
                full_command = command
                shell = True
            
            # Execute command
            if self.shell and self.shell['available']:
                process = subprocess.Popen(
                    full_command,
                    shell=False,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
            else:
                process = subprocess.Popen(
                    full_command,
                    shell=shell,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=str(self.current_directory),
                )
            
            stdout, stderr = process.communicate(timeout=30)
            
            if stdout:
                self._write_output(stdout, "output")
            if stderr:
                self._write_output(stderr, "error")
            
            if not stdout and not stderr and process.returncode == 0:
                # Command succeeded silently
                pass
            elif process.returncode != 0:
                self._write_output(f"Command failed with exit code: {process.returncode}\n", "error")
        except subprocess.TimeoutExpired:
            process.kill()
            self._write_output("Command timed out after 30 seconds.\n", "error")
        except Exception as e:
            self._write_output(f"Error: {str(e)}\n", "error")
        
        self._show_prompt()
    
    def _change_directory(self, path):
        """Change the current directory"""
        try:
            if not path:
                path = str(Path.home())
            new_path = Path(self.current_directory) / path
            if new_path.exists() and new_path.is_dir():
                self.current_directory = new_path.resolve()
                self._write_output(f"Changed directory to: {self.current_directory}\n", "info")
            else:
                self._write_output(f"Directory not found: {path}\n", "error")
        except Exception as e:
            self._write_output(f"Error changing directory: {str(e)}\n", "error")
        self._show_prompt()
    
    def _show_help(self):
        """Show help message"""
        shell_note = ""
        if self.shell and self.shell['available']:
            shell_note = f"\nNote: Using {self.shell['name']} - Linux commands are supported!\n"
        elif self.is_windows:
            shell_note = "\nNote: Linux commands will be automatically mapped to Windows equivalents.\n"
        
        help_text = f"""
Available commands:
  help              - Show this help message
  clear / cls       - Clear terminal output
  cd <path>         - Change directory
  <command>         - Execute any system command
{shell_note}
Linux Commands (auto-mapped on Windows if no Linux shell):
  ls, ll            - List directory
  pwd               - Print working directory
  cat <file>        - Display file contents
  grep <pattern>    - Search for pattern
  which <cmd>       - Find command location
  rm <file>         - Remove file
  mv <src> <dst>    - Move/rename file
  cp <src> <dst>    - Copy file
  touch <file>      - Create empty file

Examples:
  cd Documents      - Change to Documents folder
  ls                - List directory (Linux-style)
  dir               - List directory (Windows)
  python --version  - Check Python version
  pip list          - List installed packages
  cat app.py        - View file contents
"""
        self._write_output(help_text, "info")
        self._show_prompt()
    
    def _history_up(self, event):
        """Navigate command history up"""
        if self.command_history and self.history_index > 0:
            self.history_index -= 1
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, self.command_history[self.history_index])
        return "break"
    
    def _history_down(self, event):
        """Navigate command history down"""
        if self.command_history:
            if self.history_index < len(self.command_history) - 1:
                self.history_index += 1
                self.input_entry.delete(0, tk.END)
                self.input_entry.insert(0, self.command_history[self.history_index])
            else:
                self.history_index = len(self.command_history)
                self.input_entry.delete(0, tk.END)
        return "break"
    
    def apply_theme(self, colors):
        """Apply theme colors to terminal"""
        self.output.configure(bg=colors["bg"], fg=colors["fg"])
        self.input_entry.configure(bg=colors["panel"], fg=colors["fg"], insertbackground=colors["accent"])
        
        # Configure text tags
        self.output.tag_configure("normal", foreground=colors["fg"])
        self.output.tag_configure("command", foreground=colors["accent"])
        self.output.tag_configure("output", foreground=colors["fg"])
        self.output.tag_configure("error", foreground="#f48771")
        self.output.tag_configure("info", foreground="#4ec9b0")
        self.output.tag_configure("prompt", foreground=colors["accent"])


class AutoHideScrollbar(ttk.Scrollbar):
    """Completely hidden scrollbar - still functional but invisible"""
    
    def __init__(self, parent, text_widget=None, **kwargs):
        super().__init__(parent, **kwargs)
        # Hide permanently - scrollbars are invisible but still functional
        self.grid_remove()
    
    def grid(self, **kwargs):
        """Override grid to keep scrollbar hidden"""
        # Never actually show the scrollbar
        pass
    
    def grid_remove(self):
        """Keep scrollbar hidden"""
        super().grid_remove()


class LineNumbers(tk.Canvas):
    """Line number widget for the text editor"""
    
    def __init__(self, parent, text_widget, **kwargs):
        super().__init__(parent, **kwargs)
        self.text_widget = text_widget
        self.line_color = "#858585"  # Default color
        
    def set_line_color(self, color: str) -> None:
        """Set the color for line numbers"""
        self.line_color = color
        
    def redraw(self, *args):
        """Redraw line numbers"""
        if not self.text_widget:
            return
        self.delete("all")
        
        i = self.text_widget.index("@0,0")
        while True:
            dline = self.text_widget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            # Get font size from text widget if available
            font_size = 10
            if hasattr(self.text_widget, 'cget'):
                try:
                    font_tuple = self.text_widget.cget("font")
                    if isinstance(font_tuple, (list, tuple)) and len(font_tuple) >= 2:
                        font_size = font_tuple[1]
                except:
                    pass
            self.create_text(2, y, anchor="nw", text=linenum, fill=self.line_color, 
                           font=(self.text_widget.cget("font")[0] if hasattr(self.text_widget, 'cget') else "Consolas", font_size))
            i = self.text_widget.index(f"{i}+1line")


class EditorTab:
    """Represents a single editor tab"""
    
    def __init__(self, parent, notebook):
        self.notebook = notebook
        self.filepath = None
        self.modified = False
        
        # Create main frame
        self.frame = ttk.Frame(parent)
        
        # Create editor frame with line numbers
        editor_frame = tk.Frame(self.frame, bg="#1E1E1E")
        editor_frame.pack(fill=tk.BOTH, expand=True)
        
        # Line numbers
        self.line_numbers = LineNumbers(editor_frame, None, width=40, bg="#252526", highlightthickness=0)
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        # Code editor with scrollbar
        scrollbar = ttk.Scrollbar(editor_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.code_area = SyntaxHighlightedText(
            editor_frame,
            wrap=tk.NONE,
            undo=True,
            maxundo=-1,
            bg="#1E1E1E",
            fg="#D4D4D4",
            insertbackground="#FFFFFF",
            selectbackground="#264F78",
            font=("Consolas", 11),
            relief=tk.FLAT,
            padx=10,
            pady=10,
            yscrollcommand=scrollbar.set
        )
        self.code_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.code_area.yview)
        
        # Link line numbers to text widget
        self.line_numbers.text_widget = self.code_area
        
        # Bind events
        self.code_area.bind("<KeyRelease>", self._on_content_change)
        self.code_area.bind("<Button-1>", self._on_content_change)
        self.code_area.bind("<Configure>", self.line_numbers.redraw)
        self.code_area.bind("<MouseWheel>", lambda e: self.line_numbers.redraw())
        
    def _on_content_change(self, event=None):
        """Handle content changes"""
        if not self.modified:
            self.modified = True
            self._update_tab_title()
        self.line_numbers.redraw()
        return None
    
    def _update_tab_title(self):
        """Update tab title with modified indicator"""
        title = self.get_title()
        tab_id = self.notebook.index(self.frame)
        self.notebook.tab(tab_id, text=title)
    
    def get_title(self):
        """Get tab title"""
        name = Path(self.filepath).name if self.filepath else "Untitled"
        return f"{'*' if self.modified else ''}{name}"
    
    def get_code(self):
        """Get code from editor"""
        return self.code_area.get("1.0", tk.END)
    
    def set_code(self, code):
        """Set code in editor"""
        self.code_area.delete("1.0", tk.END)
        self.code_area.insert("1.0", code)
        self.modified = False
        self._update_tab_title()
        self.line_numbers.redraw()


class FSCodeIDE:
    """Main IDE application"""
    
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("FS-Code - Modern Python IDE")
        self.window.geometry("1200x800")
        self.window.configure(bg="#252526")
        
        # Set icon (will use default if icon file doesn't exist)
        try:
            self.window.iconbitmap("icon.ico")
        except:
            pass
        
        self.tabs = []
        self.current_tab = None
        
        self._create_menu()
        self._create_toolbar()
        self._create_main_area()
        self._create_output_area()
        self._create_status_bar()
        
        # Create initial tab
        self.new_file()
        
        # Bind keyboard shortcuts
        self.window.bind("<Control-n>", lambda e: self.new_file())
        self.window.bind("<Control-o>", lambda e: self.open_file())
        self.window.bind("<Control-s>", lambda e: self.save_file())
        self.window.bind("<Control-Shift-S>", lambda e: self.save_file_as())
        self.window.bind("<Control-w>", lambda e: self.close_tab())
        self.window.bind("<F5>", lambda e: self.run_code())
        self.window.bind("<Control-q>", lambda e: self.quit_app())
        
    def _create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.window)
        
        # File menu
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New File", command=self.new_file, accelerator="Ctrl+N")
        filemenu.add_command(label="Open...", command=self.open_file, accelerator="Ctrl+O")
        filemenu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        filemenu.add_command(label="Save As...", command=self.save_file_as, accelerator="Ctrl+Shift+S")
        filemenu.add_separator()
        filemenu.add_command(label="Close Tab", command=self.close_tab, accelerator="Ctrl+W")
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit_app, accelerator="Ctrl+Q")
        menubar.add_cascade(label="File", menu=filemenu)
        
        # Edit menu
        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Undo", command=lambda: self._current_editor().code_area.edit_undo(), accelerator="Ctrl+Z")
        editmenu.add_command(label="Redo", command=lambda: self._current_editor().code_area.edit_redo(), accelerator="Ctrl+Y")
        editmenu.add_separator()
        editmenu.add_command(label="Cut", command=lambda: self._current_editor().code_area.event_generate("<<Cut>>"), accelerator="Ctrl+X")
        editmenu.add_command(label="Copy", command=lambda: self._current_editor().code_area.event_generate("<<Copy>>"), accelerator="Ctrl+C")
        editmenu.add_command(label="Paste", command=lambda: self._current_editor().code_area.event_generate("<<Paste>>"), accelerator="Ctrl+V")
        menubar.add_cascade(label="Edit", menu=editmenu)
        
        # Run menu
        runmenu = tk.Menu(menubar, tearoff=0)
        runmenu.add_command(label="Run Code", command=self.run_code, accelerator="F5")
        runmenu.add_command(label="Clear Output", command=self.clear_output, accelerator="Ctrl+L")
        menubar.add_cascade(label="Run", menu=runmenu)
        
        # Help menu
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=helpmenu)
        
        self.window.config(menu=menubar)
    
    def _create_toolbar(self):
        """Create toolbar with buttons"""
        toolbar = tk.Frame(self.window, bg="#2D2D30", relief=tk.FLAT, height=40)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        button_style = {
            "bg": "#007ACC",
            "fg": "white",
            "relief": tk.FLAT,
            "padx": 15,
            "pady": 5,
            "font": ("Segoe UI", 9, "bold"),
            "cursor": "hand2",
            "activebackground": "#005A9E",
            "activeforeground": "white"
        }
        
        tk.Button(toolbar, text="📄 New", command=self.new_file, **button_style).pack(side=tk.LEFT, padx=2, pady=5)
        tk.Button(toolbar, text="📁 Open", command=self.open_file, **button_style).pack(side=tk.LEFT, padx=2, pady=5)
        tk.Button(toolbar, text="💾 Save", command=self.save_file, **button_style).pack(side=tk.LEFT, padx=2, pady=5)
        
        # Separator
        tk.Frame(toolbar, bg="#404040", width=2).pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        run_button = tk.Button(toolbar, text="▶ Run (F5)", command=self.run_code, 
                               bg="#16825D", fg="white", relief=tk.FLAT, padx=15, pady=5,
                               font=("Segoe UI", 9, "bold"), cursor="hand2",
                               activebackground="#0F5940", activeforeground="white")
        run_button.pack(side=tk.LEFT, padx=2, pady=5)
        
        tk.Button(toolbar, text="🗑️ Clear", command=self.clear_output, **button_style).pack(side=tk.LEFT, padx=2, pady=5)
    
    def _create_main_area(self):
        """Create main editor area with tabs"""
        # Create notebook for tabs
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#2D2D30', borderwidth=0)
        style.configure('TNotebook.Tab', background='#2D2D30', foreground='#CCCCCC', 
                       padding=[10, 5], borderwidth=0)
        style.map('TNotebook.Tab', background=[('selected', '#1E1E1E')], 
                 foreground=[('selected', '#FFFFFF')])
        
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)
    
    def _create_output_area(self):
        """Create output console area"""
        output_frame = tk.Frame(self.window, bg="#1E1E1E")
        output_frame.pack(fill=tk.BOTH, expand=False, pady=(0, 0))
        
        # Output label
        label_frame = tk.Frame(output_frame, bg="#2D2D30", height=25)
        label_frame.pack(fill=tk.X)
        tk.Label(label_frame, text="Output Console", bg="#2D2D30", fg="#CCCCCC", 
                font=("Segoe UI", 9, "bold"), anchor=tk.W, padx=10).pack(side=tk.LEFT)
        
        # Output text area
        self.output_area = scrolledtext.ScrolledText(
            output_frame,
            height=10,
            bg="#1E1E1E",
            fg="#CCCCCC",
            insertbackground="#FFFFFF",
            font=("Consolas", 10),
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.output_area.pack(fill=tk.BOTH, expand=True)
        
        # Configure tags for colored output
        self.output_area.tag_configure("error", foreground="#F48771")
        self.output_area.tag_configure("success", foreground="#4EC9B0")
    
    def _create_status_bar(self):
        """Create status bar"""
        self.status_bar = tk.Frame(self.window, bg="#007ACC", height=25)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_label = tk.Label(self.status_bar, text="Ready", bg="#007ACC", 
                                     fg="white", anchor=tk.W, padx=10, 
                                     font=("Segoe UI", 9))
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.cursor_label = tk.Label(self.status_bar, text="Ln 1, Col 1", bg="#007ACC", 
                                     fg="white", anchor=tk.E, padx=10,
                                     font=("Segoe UI", 9))
        self.cursor_label.pack(side=tk.RIGHT)
    
    def _current_editor(self):
        """Get current editor tab"""
        if self.current_tab is not None and self.current_tab < len(self.tabs):
            return self.tabs[self.current_tab]
        return None
    
    def _on_tab_changed(self, event):
        """Handle tab change"""
        self.current_tab = self.notebook.index(self.notebook.select())
        editor = self._current_editor()
        if editor:
            self.update_status(f"Editing: {editor.get_title()}")
    
    def new_file(self):
        """Create new file tab"""
        editor = EditorTab(self.notebook, self.notebook)
        self.tabs.append(editor)
        self.notebook.add(editor.frame, text=editor.get_title())
        self.notebook.select(len(self.tabs) - 1)
        self.current_tab = len(self.tabs) - 1
        self.update_status("New file created")
    
    def open_file(self):
        """Open file dialog and load file"""
        filepath = filedialog.askopenfilename(
            title="Open File",
            filetypes=[("Python Files", "*.py"), ("All Files", "*.*")]
        )
        
        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    code = file.read()
                
                editor = EditorTab(self.notebook, self.notebook)
                editor.filepath = filepath
                editor.set_code(code)
                
                self.tabs.append(editor)
                self.notebook.add(editor.frame, text=editor.get_title())
                self.notebook.select(len(self.tabs) - 1)
                self.current_tab = len(self.tabs) - 1
                
                self.update_status(f"Opened: {filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file:\n{str(e)}")
    
    def save_file(self):
        """Save current file"""
        editor = self._current_editor()
        if not editor:
            return
        
        if editor.filepath:
            try:
                with open(editor.filepath, 'w', encoding='utf-8') as file:
                    file.write(editor.get_code())
                editor.modified = False
                editor._update_tab_title()
                self.update_status(f"Saved: {editor.filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file:\n{str(e)}")
        else:
            self.save_file_as()
    
    def save_file_as(self):
        """Save file with new name"""
        editor = self._current_editor()
        if not editor:
            return
        
        filepath = filedialog.asksaveasfilename(
            title="Save File As",
            defaultextension=".py",
            filetypes=[("Python Files", "*.py"), ("All Files", "*.*")]
        )
        
        if filepath:
            try:
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(editor.get_code())
                editor.filepath = filepath
                editor.modified = False
                editor._update_tab_title()
                self.update_status(f"Saved as: {filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file:\n{str(e)}")
    
    def close_tab(self):
        """Close current tab"""
        if not self.tabs:
            return
        
        editor = self._current_editor()
        if editor and editor.modified:
            result = messagebox.askyesnocancel(
                "Unsaved Changes",
                f"Do you want to save changes to {editor.get_title()}?"
            )
            if result is None:  # Cancel
                return
            elif result:  # Yes
                self.save_file()
        
        if self.current_tab is not None:
            self.notebook.forget(self.current_tab)
            self.tabs.pop(self.current_tab)
            
            if self.tabs:
                self.current_tab = min(self.current_tab, len(self.tabs) - 1)
            else:
                self.current_tab = None
                self.new_file()  # Create new tab if all closed
    
    def run_code(self):
        """Execute the code"""
        editor = self._current_editor()
        if not editor:
            return
        
        code = editor.get_code()
        
        self.output_area.delete("1.0", tk.END)
        self.update_status("Running code...")
        
        try:
            process = subprocess.Popen(
                ["python", "-c", code],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            output, error = process.communicate(timeout=30)
            
            if output:
                self.output_area.insert(tk.END, output, "success")
            if error:
                self.output_area.insert(tk.END, error, "error")
            
            if not output and not error:
                self.output_area.insert(tk.END, "Code executed successfully (no output)", "success")
            
            self.update_status("Code execution completed")
        except subprocess.TimeoutExpired:
            self.output_area.insert(tk.END, "Error: Code execution timed out (30 seconds)", "error")
            self.update_status("Execution timed out")
        except Exception as e:
            self.output_area.insert(tk.END, f"Error: {str(e)}", "error")
            self.update_status("Execution error")
    
    def clear_output(self):
        """Clear output console"""
        self.output_area.delete("1.0", tk.END)
        self.update_status("Output cleared")
    
    def quit_app(self):
        """Quit application"""
        # Check for unsaved changes
        unsaved = [tab for tab in self.tabs if tab.modified]
        if unsaved:
            result = messagebox.askyesnocancel(
                "Unsaved Changes",
                f"You have {len(unsaved)} unsaved file(s). Do you want to quit anyway?"
            )
            if not result:
                return
        
        self.window.quit()
    
    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo(
            "About FS-Code",
            "FS-Code - Modern Python IDE\n\n"
            "Version: 2.0\n"
            "Author: FABIAN TERES\n\n"
            "A professional Python IDE with:\n"
            "• Syntax highlighting\n"
            "• Tabbed interface\n"
            "• Line numbers\n"
            "• Modern dark theme\n"
            "• File operations\n"
            "• Keyboard shortcuts"
        )
    
    def update_status(self, message):
        """Update status bar message"""
        self.status_label.config(text=message)
    
    def run(self):
        """Start the application"""
        self.update_status("Ready - Press F5 to run code")
        self.window.mainloop()


def main():
    """Main entry point for the application"""
    app = FSCodeIDE()
    app.run()

# Enhanced FS Code IDE desktop application
import subprocess
import sys
import threading
from pathlib import Path

import tkinter as tk
import tkinter.font as tkfont
from tkinter import filedialog, messagebox, ttk


class FSCodeIDE(tk.Tk):
    """Feature-rich yet lightweight desktop IDE for Python scripts."""

    THEMES = {
        "dark": {
            "bg": "#1e1e1e",
            "panel": "#252526",
            "fg": "#f5f5f5",
            "accent": "#569cd6",
            "output_bg": "#101010",
        },
        "light": {
            "bg": "#f5f5f5",
            "panel": "#ffffff",
            "fg": "#1f1f1f",
            "accent": "#0063b1",
            "output_bg": "#f0f0f0",
        },
    }

    def __init__(self) -> None:
        super().__init__()
        self.title("FS-code IDE")
        self.geometry("1100x700")
        self.minsize(900, 600)

        self.current_file: Path | None = None
        self.is_dirty = False
        self.theme = "dark"
        self.process: subprocess.Popen | None = None
        self.font_family = self._default_font()
        self.font_size = tk.IntVar(value=14)
        self.status_var = tk.StringVar(value="Ready")
        self.terminal_visible = False
        self.terminal_visible = False

        self.style = ttk.Style(self)
        self._create_styles()
        self._create_menu()
        self._create_toolbar()
        self._create_layout()
        self._bind_shortcuts()
        self.apply_theme()
        self.update_title()
        # Initial line number redraw
        if hasattr(self, 'line_numbers'):
            self.line_numbers.redraw()

    # ------------------------------------------------------------------ UI setup
    def _create_styles(self) -> None:
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass
        
        # Configure sleek scrollbar styles
        self._update_scrollbar_styles()
    
    def _update_scrollbar_styles(self) -> None:
        """Update scrollbar styles to be sleek and modern"""
        colors = self.THEMES[self.theme]
        
        # Scrollbar colors based on theme
        if self.theme == "dark":
            trough_color = "#2d2d30"
            slider_color = "#424242"
            slider_hover = "#4e4e4e"
            arrow_color = "#858585"
        else:
            trough_color = "#e0e0e0"
            slider_color = "#b0b0b0"
            slider_hover = "#999999"
            arrow_color = "#666666"
        
        # Vertical scrollbar style - sleek and modern
        self.style.configure(
            "Vertical.TScrollbar",
            background=trough_color,
            troughcolor=trough_color,
            borderwidth=0,
            arrowcolor=arrow_color,
            darkcolor=slider_color,
            lightcolor=slider_color,
            width=10,  # Sleek thin scrollbar
            relief=tk.FLAT,
        )
        self.style.map(
            "Vertical.TScrollbar",
            background=[("active", slider_hover), ("pressed", slider_hover), ("!active", slider_color)],
        )
        
        # Horizontal scrollbar style - sleek and modern
        self.style.configure(
            "Horizontal.TScrollbar",
            background=trough_color,
            troughcolor=trough_color,
            borderwidth=0,
            arrowcolor=arrow_color,
            darkcolor=slider_color,
            lightcolor=slider_color,
            width=10,  # Sleek thin scrollbar
            relief=tk.FLAT,
        )
        self.style.map(
            "Horizontal.TScrollbar",
            background=[("active", slider_hover), ("pressed", slider_hover), ("!active", slider_color)],
        )

    def _create_menu(self) -> None:
        menubar = tk.Menu(self)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", accelerator="Ctrl+N", command=self.new_file)
        file_menu.add_command(label="Open…", accelerator="Ctrl+O", command=self.open_file)
        file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.save_file)
        file_menu.add_command(label="Save As…", accelerator="Ctrl+Shift+S", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        run_menu = tk.Menu(menubar, tearoff=0)
        run_menu.add_command(label="Run", accelerator="F5", command=self.run_code)
        run_menu.add_command(label="Stop", accelerator="F6", command=self.stop_code)
        menubar.add_cascade(label="Run", menu=run_menu)

        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Toggle Theme", accelerator="Ctrl+T", command=self.toggle_theme)
        menubar.add_cascade(label="View", menu=view_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menubar)

    def _create_toolbar(self) -> None:
        self.toolbar = ttk.Frame(self, padding=(10, 8))
        self.toolbar.pack(fill=tk.X)

        self.run_button = ttk.Button(self.toolbar, text="▶ Run", command=self.run_code)
        self.run_button.pack(side=tk.LEFT, padx=(0, 6))

        self.stop_button = ttk.Button(self.toolbar, text="■ Stop", command=self.stop_code, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=(0, 6))

        ttk.Button(self.toolbar, text="Clear Output", command=self.clear_output).pack(side=tk.LEFT, padx=(0, 6))
        ttk.Button(self.toolbar, text="Terminal", command=self.toggle_terminal).pack(side=tk.LEFT, padx=(0, 6))
        ttk.Button(self.toolbar, text="Toggle Theme", command=self.toggle_theme).pack(side=tk.LEFT, padx=(0, 6))

        ttk.Label(self.toolbar, text="Font size").pack(side=tk.LEFT, padx=(12, 4))
        self.font_size_box = tk.Spinbox(
            self.toolbar,
            from_=8,
            to=32,
            width=4,
            textvariable=self.font_size,
            command=self.update_font,
        )
        self.font_size_box.pack(side=tk.LEFT)
        self.font_size.trace_add("write", lambda *_: self.update_font())

        ttk.Label(self.toolbar, text="  ").pack(side=tk.LEFT, expand=True)

    def _create_layout(self) -> None:
        # Main container with horizontal paned window for terminal sidebar
        self.main_container = ttk.Frame(self)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Horizontal paned window for terminal sidebar
        self.horizontal_paned = ttk.Panedwindow(self.main_container, orient=tk.HORIZONTAL)
        self.horizontal_paned.pack(fill=tk.BOTH, expand=True)
        
        # Terminal sidebar (initially hidden)
        self.terminal_frame = ttk.Frame(self.horizontal_paned, width=350)
        self.terminal = Terminal(self.terminal_frame)
        self.terminal.pack(fill=tk.BOTH, expand=True)
        self.terminal_frame.pack_propagate(False)
        
        # Main content area
        self.content_frame = ttk.Frame(self.horizontal_paned)
        
        # Add content frame to paned window first (terminal hidden initially)
        self.horizontal_paned.add(self.content_frame, weight=1)
        
        # Vertical paned window for editor and output
        self.paned = ttk.Panedwindow(self.content_frame, orient=tk.VERTICAL)
        self.paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Editor panel
        editor_frame = ttk.Frame(self.paned, padding=5)
        editor_frame.columnconfigure(1, weight=1)
        editor_frame.rowconfigure(0, weight=1)
        
        # Line numbers
        self.line_numbers = LineNumbers(
            editor_frame,
            None,
            width=50,
            highlightthickness=0,
            borderwidth=0
        )
        self.line_numbers.grid(row=0, column=0, sticky="ns")
        
        # Code editor with syntax highlighting
        self.code_area = SyntaxHighlightedText(
            editor_frame,
            wrap=tk.NONE,
            undo=True,
            font=(self.font_family, self.font_size.get()),
            borderwidth=0,
            highlightthickness=0,
            padx=10,
            pady=10,
            insertwidth=2,
        )
        self.code_area.grid(row=0, column=1, sticky="nsew")
        
        # Link line numbers to text widget
        self.line_numbers.text_widget = self.code_area
        
        # Bind events
        self.code_area.bind("<<Modified>>", self._on_modified)
        self.code_area.bind("<KeyRelease>", self._on_code_change)
        self.code_area.bind("<ButtonRelease>", self._on_code_change)
        self.code_area.bind("<Return>", self._handle_return)
        self.code_area.bind("<Configure>", lambda e: self.line_numbers.redraw())
        self.code_area.bind("<MouseWheel>", lambda e: self.line_numbers.redraw())

        self.code_scroll_y = AutoHideScrollbar(editor_frame, text_widget=self.code_area, command=self.code_area.yview, orient=tk.VERTICAL, style="Vertical.TScrollbar")
        self.code_scroll_y.grid(row=0, column=2, sticky="ns")
        self.code_area.configure(yscrollcommand=self.code_scroll_y.set)

        self.code_scroll_x = AutoHideScrollbar(editor_frame, text_widget=self.code_area, command=self.code_area.xview, orient=tk.HORIZONTAL, style="Horizontal.TScrollbar")
        self.code_scroll_x.grid(row=1, column=1, sticky="ew")
        self.code_area.configure(xscrollcommand=self.code_scroll_x.set)

        # Output panel
        output_frame = ttk.Frame(self.paned, padding=5)
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)

        self.output_area = tk.Text(
            output_frame,
            wrap=tk.WORD,
            state=tk.DISABLED,
            borderwidth=0,
            highlightthickness=0,
            padx=10,
            pady=10,
            font=(self.font_family, 12),
        )
        self.output_area.grid(row=0, column=0, sticky="nsew")

        self.output_scroll = AutoHideScrollbar(output_frame, text_widget=self.output_area, command=self.output_area.yview, orient=tk.VERTICAL, style="Vertical.TScrollbar")
        self.output_scroll.grid(row=0, column=1, sticky="ns")
        self.output_area.configure(yscrollcommand=self.output_scroll.set)

        self.paned.add(editor_frame, weight=3)
        self.paned.add(output_frame, weight=2)

        # Status bar
        status_bar = ttk.Frame(self, padding=(10, 4))
        status_bar.pack(fill=tk.X)
        ttk.Label(status_bar, textvariable=self.status_var, anchor="w").pack(fill=tk.X)

    def _bind_shortcuts(self) -> None:
        self.bind("<Control-n>", lambda event: self.new_file())
        self.bind("<Control-o>", lambda event: self.open_file())
        self.bind("<Control-s>", lambda event: self.save_file())
        self.bind("<Control-S>", lambda event: self.save_file_as())
        self.bind("<Control-t>", lambda event: self.toggle_theme())
        self.bind("<Control-backslash>", lambda event: self.toggle_terminal())  # Ctrl+` for terminal
        self.bind("<F5>", lambda event: self.run_code())
        self.bind("<F6>", lambda event: self.stop_code())

    # ------------------------------------------------------------------ Command handlers
    def new_file(self) -> None:
        if not self._maybe_save_changes():
            return
        self.code_area.delete("1.0", tk.END)
        self.current_file = None
        self.is_dirty = False
        self.update_title()
        self.line_numbers.redraw()
        self.append_output("New file ready.\n", replace=True)

    def open_file(self) -> None:
        if not self._maybe_save_changes():
            return
        file_path = filedialog.askopenfilename(
            filetypes=[("Python files", "*.py"), ("All files", "*.*")],
            defaultextension=".py",
        )
        if not file_path:
            return
        try:
            contents = Path(file_path).read_text(encoding="utf-8")
        except OSError as exc:
            messagebox.showerror("Open failed", str(exc))
            return

        self.code_area.delete("1.0", tk.END)
        self.code_area.insert("1.0", contents)
        # Trigger syntax highlighting after content is loaded
        self.code_area.after_idle(self.code_area._highlight_syntax)
        self.current_file = Path(file_path)
        self.is_dirty = False
        self.update_title()
        self.update_status_bar()
        self.line_numbers.redraw()
        self.append_output(f"Opened {self.current_file}\n", replace=True)

    def save_file(self) -> bool:
        if self.current_file is None:
            return self.save_file_as()
        return self._write_to_path(self.current_file)

    def save_file_as(self) -> bool:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".py",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")],
        )
        if not file_path:
            return False
        self.current_file = Path(file_path)
        return self._write_to_path(self.current_file)

    def clear_output(self) -> None:
        self.append_output("", replace=True)
        self.status_var.set("Output cleared.")

    def run_code(self) -> None:
        code = self.code_area.get("1.0", tk.END)
        if not code.strip():
            messagebox.showinfo("Run code", "Nothing to run. Please add some Python code first.")
            return

        self.stop_code()
        self.append_output("▶ Running code...\n", replace=True)
        self.status_var.set("Running...")
        self.run_button.state(["disabled"])
        self.stop_button.state(["!disabled"])

        thread = threading.Thread(target=self._execute_code, args=(code,), daemon=True)
        thread.start()

    def stop_code(self) -> None:
        if not self.process:
            return
        if self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=1)
            except subprocess.TimeoutExpired:
                self.process.kill()
            self.append_output("\n■ Execution stopped by user.\n")
        self.process = None
        self.run_button.state(["!disabled"])
        self.stop_button.state(["disabled"])
        self.status_var.set("Ready")

    def toggle_theme(self) -> None:
        self.theme = "light" if self.theme == "dark" else "dark"
        self.apply_theme()
    
    def toggle_terminal(self) -> None:
        """Toggle terminal sidebar visibility"""
        # Get current panes
        try:
            panes = list(self.horizontal_paned.panes())
        except:
            panes = []
        
        terminal_in_panes = self.terminal_frame in panes
        content_in_panes = self.content_frame in panes
        
        if self.terminal_visible and terminal_in_panes:
            # Hide terminal
            try:
                self.horizontal_paned.forget(self.terminal_frame)
            except tk.TclError:
                pass
            self.terminal_visible = False
        elif not self.terminal_visible and not terminal_in_panes:
            # Show terminal - need to reorder panes
            try:
                # Remove content frame if it's in panes
                if content_in_panes:
                    self.horizontal_paned.forget(self.content_frame)
                # Add terminal first, then content
                self.horizontal_paned.add(self.terminal_frame, weight=0)
                if content_in_panes:
                    self.horizontal_paned.add(self.content_frame, weight=1)
            except tk.TclError as e:
                # If there's an error, try simpler approach
                try:
                    self.horizontal_paned.add(self.terminal_frame, weight=0)
                except:
                    pass
            self.terminal_visible = True

    def update_font(self) -> None:
        size = max(8, min(32, int(self.font_size.get())))
        self.code_area.configure(font=(self.font_family, size))
        self.line_numbers.redraw()

    def show_about(self) -> None:
        messagebox.showinfo(
            "About FS-code",
            "FS-code IDE\nA minimal desktop IDE for learning and quick experiments.",
        )

    # ------------------------------------------------------------------ Helpers
    def _write_to_path(self, path: Path) -> bool:
        try:
            path.write_text(self.code_area.get("1.0", tk.END), encoding="utf-8")
        except OSError as exc:
            messagebox.showerror("Save failed", str(exc))
            return False
        self.is_dirty = False
        self.update_title()
        self.status_var.set(f"Saved to {path}")
        return True

    def _maybe_save_changes(self) -> bool:
        if not self.is_dirty:
            return True
        response = messagebox.askyesnocancel(
            "Unsaved changes",
            "Do you want to save your current file before continuing?",
        )
        if response is None:
            return False
        if response:
            return self.save_file()
        return True

    def _execute_code(self, code: str) -> None:
        try:
            process = subprocess.Popen(
                [sys.executable, "-u", "-c", code],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            self.process = process
            stdout, stderr = process.communicate()
            returncode = process.returncode
        except Exception as exc:  # pragma: no cover - GUI feedback only
            self.after(0, lambda: self._finalize_run(error=str(exc)))
            return

        self.after(0, lambda: self._finalize_run(stdout, stderr, returncode))

    def _finalize_run(self, stdout: str = "", stderr: str = "", returncode: int | None = None, error: str | None = None) -> None:
        self.process = None
        self.run_button.state(["!disabled"])
        self.stop_button.state(["disabled"])

        output = ""
        if error:
            output = f"Error: {error}\n"
        else:
            if stdout:
                output += stdout
            if stderr:
                output += stderr
            if not output:
                output = "Process finished with no output.\n"
        self.append_output(output)
        status = "Finished" if not error and (returncode == 0) else "Completed with errors"
        self.status_var.set(status)

    def _on_modified(self, _event=None) -> None:
        if self.code_area.edit_modified():
            self.is_dirty = True
            self.update_title()
            self.update_status_bar()
            self.code_area.edit_modified(False)

    def _on_code_change(self, event=None) -> None:
        """Handle code changes - update status bar and line numbers"""
        self.update_status_bar()
        self.line_numbers.redraw()
        return None

    def update_status_bar(self) -> None:
        line, column = self.code_area.index(tk.INSERT).split(".")
        file_name = self.current_file.name if self.current_file else "Untitled"
        dirty = "*" if self.is_dirty else ""
        self.status_var.set(f"{dirty}{file_name}  |  Line {line}, Col {int(column) + 1}")

    def _handle_return(self, event) -> str:
        """Insert a newline that preserves the current indentation."""
        line_start = self.code_area.index("insert linestart")
        current_line = self.code_area.get(line_start, "insert")
        indent = ""
        for char in current_line:
            if char in (" ", "\t"):
                indent += char
            else:
                break
        suffix = indent
        if current_line.rstrip().endswith(":"):
            suffix += "    "
        self.code_area.insert(tk.INSERT, f"\n{suffix}")
        self.update_status_bar()
        self.line_numbers.redraw()
        return "break"

    def append_output(self, text: str, replace: bool = False) -> None:
        self.output_area.configure(state=tk.NORMAL)
        if replace:
            self.output_area.delete("1.0", tk.END)
        self.output_area.insert(tk.END, text)
        self.output_area.see(tk.END)
        self.output_area.configure(state=tk.DISABLED)

    def apply_theme(self) -> None:
        colors = self.THEMES[self.theme]
        self.configure(bg=colors["bg"])
        # Note: ttk widgets (toolbar, paned) are configured via styles below

        self.style.configure("TFrame", background=colors["panel"])
        self.style.configure("TLabel", background=colors["panel"], foreground=colors["fg"])
        self.style.configure("TButton", background=colors["panel"], foreground=colors["fg"])
        self.style.configure("TPanedwindow", background=colors["bg"])
        self.style.configure("TMenubutton", background=colors["panel"], foreground=colors["fg"])
        
        # Update scrollbar styles
        self._update_scrollbar_styles()

        text_config = {
            "bg": colors["panel"],
            "fg": colors["fg"],
            "insertbackground": colors["accent"],
            "selectbackground": colors["accent"],
            "selectforeground": colors["bg"],
        }
        self.code_area.configure(**text_config)
        self.output_area.configure(
            bg=colors["output_bg"],
            fg=colors["fg"],
            insertbackground=colors["accent"],
            selectbackground=colors["accent"],
            selectforeground=colors["bg"],
        )
        
        # Style line numbers
        line_num_bg = colors["panel"] if self.theme == "dark" else "#e8e8e8"
        line_num_fg = "#858585" if self.theme == "dark" else "#666666"
        self.line_numbers.configure(bg=line_num_bg)
        self.line_numbers.set_line_color(line_num_fg)
        # Update line number colors by redrawing
        self.line_numbers.redraw()
        
        # Apply theme to terminal
        if hasattr(self, 'terminal'):
            self.terminal.apply_theme(colors)
        
        self.update()

    def update_title(self) -> None:
        file_name = self.current_file.name if self.current_file else "Untitled"
        star = "*" if self.is_dirty else ""
        self.title(f"{star}{file_name} - FS-code IDE")

    def _default_font(self) -> str:
        candidates = ("JetBrains Mono", "Fira Code", "Consolas", "Menlo", "Courier New", "Courier")
        available = {name.lower() for name in tkfont.families()}
        for candidate in candidates:
            if candidate.lower() in available:
                return candidate
        return "Courier"


def main() -> None:
    app = FSCodeIDE()
    app.mainloop()

if __name__ == "__main__":
    main()
