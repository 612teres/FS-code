import tkinter as tk
from tkinter import scrolledtext
import subprocess

def run_code():
    code = code_area.get("1.0", tk.END)

    try:
        #Execute code using subprocess
        process = subprocess.Popen(["python", "-c", code], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, error = process.communicate()

        #Clear the output area and insert the results
        output_area.delete("1.0", tk.END)
        if output:
            output_area.insert(tk.END, output)
        if error:
            output_area.insert(tk.END, error)
    except Exception as e:
        output_area.insert(tk.END, f"Error: {e}")

#Main window
window = tk.Tk()
window.title("FS-code")

#Code editor
code_area = scrolledtext.ScrolledText(window)
code_area.pack(fill=tk.BOTH, expand=True)

#Output area
output_area = scrolledtext.ScrolledText(window)
output_area.pack(fill=tk.BOTH, expand=True)

#Run button
run_button = tk.Button(window, text="Run")
run_button.pack()
run_button.config(command=run_code)

# Create a frame for the buttons
button_frame = tk.Frame(window)
button_frame.pack()

# Create the clear button
clear_button = tk.Button(button_frame, text="Clear", command=lambda: output_area.delete("1.0", tk.END))
clear_button.pack(side=tk.LEFT)

# Create a menu bar
menubar = tk.Menu(window)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Open")  # You'll need to implement the open functionality
filemenu.add_command(label="Save")  # You'll need to implement the save functionality
filemenu.add_separator()
filemenu.add_command(label="Exit", command=window.quit)
menubar.add_cascade(label="File", menu=filemenu)

window.config(menu=menubar)

window.mainloop()