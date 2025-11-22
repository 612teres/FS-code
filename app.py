"""
FS-Code: A Modern Python IDE
Built with Tkinter featuring syntax highlighting, tabbed interface, and modern UI
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox, font
import subprocess
import re
import os
from pathlib import Path


class SyntaxHighlightedText(tk.Text):
    """Text widget with Python syntax highlighting"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Define syntax highlighting tags
        self.tag_configure("keyword", foreground="#569CD6")
        self.tag_configure("string", foreground="#CE9178")
        self.tag_configure("comment", foreground="#6A9955")
        self.tag_configure("function", foreground="#DCDCAA")
        self.tag_configure("number", foreground="#B5CEA8")
        self.tag_configure("builtin", foreground="#4EC9B0")
        
        # Bind key release to trigger highlighting
        self.bind("<KeyRelease>", self._highlight_syntax)
        self.bind("<Return>", self._highlight_syntax)
        
    def _highlight_syntax(self, event=None):
        """Apply syntax highlighting to the text"""
        # Remove all tags
        for tag in ["keyword", "string", "comment", "function", "number", "builtin"]:
            self.tag_remove(tag, "1.0", tk.END)
        
        code = self.get("1.0", tk.END)
        
        # Keywords
        keywords = r'\b(and|as|assert|break|class|continue|def|del|elif|else|except|False|finally|for|from|global|if|import|in|is|lambda|None|nonlocal|not|or|pass|raise|return|True|try|while|with|yield)\b'
        for match in re.finditer(keywords, code):
            start = f"1.0 + {match.start()} chars"
            end = f"1.0 + {match.end()} chars"
            self.tag_add("keyword", start, end)
        
        # Built-in functions
        builtins = r'\b(print|len|range|str|int|float|list|dict|set|tuple|open|input|type|isinstance|enumerate|zip|map|filter|sum|max|min|abs|round)\b'
        for match in re.finditer(builtins, code):
            start = f"1.0 + {match.start()} chars"
            end = f"1.0 + {match.end()} chars"
            self.tag_add("builtin", start, end)
        
        # Strings (single and double quotes)
        strings = r'(["\'])(?:(?=(\\?))\2.)*?\1'
        for match in re.finditer(strings, code):
            start = f"1.0 + {match.start()} chars"
            end = f"1.0 + {match.end()} chars"
            self.tag_add("string", start, end)
        
        # Comments
        comments = r'#.*?$'
        for match in re.finditer(comments, code, re.MULTILINE):
            start = f"1.0 + {match.start()} chars"
            end = f"1.0 + {match.end()} chars"
            self.tag_add("comment", start, end)
        
        # Numbers
        numbers = r'\b\d+\.?\d*\b'
        for match in re.finditer(numbers, code):
            start = f"1.0 + {match.start()} chars"
            end = f"1.0 + {match.end()} chars"
            self.tag_add("number", start, end)
        
        # Functions (def function_name)
        functions = r'\bdef\s+(\w+)'
        for match in re.finditer(functions, code):
            start = f"1.0 + {match.start(1)} chars"
            end = f"1.0 + {match.end(1)} chars"
            self.tag_add("function", start, end)
        
        return "break"  # Prevent default handler


class LineNumbers(tk.Canvas):
    """Line number widget for the text editor"""
    
    def __init__(self, parent, text_widget, **kwargs):
        super().__init__(parent, **kwargs)
        self.text_widget = text_widget
        
    def redraw(self, *args):
        """Redraw line numbers"""
        self.delete("all")
        
        i = self.text_widget.index("@0,0")
        while True:
            dline = self.text_widget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2, y, anchor="nw", text=linenum, fill="#858585", font=("Consolas", 10))
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


if __name__ == "__main__":
    main()
