"""graphical user interface (GUI) for various musical analysis programs. """
# Import necessary libraries
import tkinter as tk
from tkinter import ttk
import mode_analysis
import mode_search
import mode_comparator

# Define functions to open each program in a new window
def open_program1():
    program1_window = tk.Toplevel(root)
    program1_window.title("Analyse de Mode")
    mode_analysis.create_gui(program1_window)

def open_program2():
    program2_window = tk.Toplevel(root)
    program2_window.title("Recherche de Modes")
    mode_search.create_gui(program2_window)

def open_program3():
    program3_window = tk.Toplevel(root)
    program3_window.title("Comparateur de Modes")
    mode_comparator.create_gui(program3_window)

# Create the main window
root = tk.Tk()
root.title("Programmes d'Analyse Musicale")
root.configure(bg='#f0f0f0')

# Add the main title to the window
title_label = tk.Label(root, text="Programmes d'Analyse Musicale", bg='#f0f0f0', font=('Arial', 16, 'bold'))
title_label.pack(pady=10)

# Create a frame for the buttons
button_frame = tk.Frame(root, bg='#f0f0f0')
button_frame.pack(pady=10)

# Configure button style
style = ttk.Style()
style.configure('TButton', font=('Arial', 12))

# Create buttons for each program
button1 = ttk.Button(button_frame, text="Analyse de Mode", command=open_program1)
button1.pack(side=tk.LEFT, padx=5)

button2 = ttk.Button(button_frame, text="Recherche de Modes", command=open_program2)
button2.pack(side=tk.LEFT, padx=5)

button3 = ttk.Button(button_frame, text="Comparateur de Modes", command=open_program3)
button3.pack(side=tk.LEFT, padx=5)

# Add instructions and copyright information
instructions = tk.Label(root, text="Sélectionnez un programme\n© 2024 Aurélien GIRY", 
                        bg='#f0f0f0', font=('Arial', 10, 'italic'))
instructions.pack(pady=5)

# Start the main event loop
root.mainloop()
