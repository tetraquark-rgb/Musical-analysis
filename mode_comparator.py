"""This code creates a graphical user interface for comparing two musical modes. It allows users to select a notation system, two modes, and their respective tonics. The interface then displays the notes of each mode, common notes, and different notes between the two modes."""
# Import necessary libraries and modules
import tkinter as tk
from tkinter import ttk
from common import get_all_scales, get_scale_notes, get_enharmonic_equivalent, format_notes

# Function to compare two musical modes
def compare_modes(mode1, tonic1, mode2, tonic2, notation, output_text):
    scales = get_all_scales()
    # Check if both modes are valid
    if mode1.lower() not in scales or mode2.lower() not in scales:
        output_text.insert("1.0", "Un ou plusieurs modes non reconnus.\n\n")
        return

    # Get and format notes for both modes
    notes1 = get_scale_notes(scales[mode1.lower()], tonic1, notation)
    notes2 = get_scale_notes(scales[mode2.lower()], tonic2, notation)
    notes1_formatted = format_notes(notes1, notation)
    notes2_formatted = format_notes(notes2, notation)

    # Create main frame for displaying results
    main_frame = tk.Frame(output_text, bd=2, relief=tk.SOLID)
    
    # Add title
    title_label = tk.Label(main_frame, text=f"Comparaison entre {tonic1} {mode1} et {tonic2} {mode2}", font=("Arial", 14, "bold"), anchor="w")
    title_label.pack(fill=tk.X, padx=5, pady=5)

    # Display notes of both modes
    notes_frame = tk.Frame(main_frame)
    notes_frame.pack(fill=tk.X, padx=5, pady=2)
    tk.Label(notes_frame, text=f"{tonic1} {mode1}:", font=("Arial", 12, "bold"), anchor="w").pack(side=tk.LEFT)
    tk.Label(notes_frame, text=" - ".join(notes1_formatted), anchor="w").pack(side=tk.LEFT, padx=(5, 0))

    notes_frame2 = tk.Frame(main_frame)
    notes_frame2.pack(fill=tk.X, padx=5, pady=2)
    tk.Label(notes_frame2, text=f"{tonic2} {mode2}:", font=("Arial", 12, "bold"), anchor="w").pack(side=tk.LEFT)
    tk.Label(notes_frame2, text=" - ".join(notes2_formatted), anchor="w").pack(side=tk.LEFT, padx=(5, 0))

    # Display common notes
    common_notes = list(set(notes1) & set(notes2))
    common_notes_formatted = format_notes(common_notes, notation)
    common_frame = tk.Frame(main_frame)
    common_frame.pack(fill=tk.X, padx=5, pady=2)
    tk.Label(common_frame, text="Notes communes:", font=("Arial", 12, "bold"), anchor="w").pack(side=tk.LEFT)
    tk.Label(common_frame, text=" - ".join(common_notes_formatted), anchor="w").pack(side=tk.LEFT, padx=(5, 0))

    # Display different notes
    diff_notes1 = list(set(notes1) - set(notes2))
    diff_notes2 = list(set(notes2) - set(notes1))
    diff_notes1_formatted = format_notes(diff_notes1, notation)
    diff_notes2_formatted = format_notes(diff_notes2, notation)
    diff_frame = tk.Frame(main_frame)
    diff_frame.pack(fill=tk.X, padx=5, pady=2)
    tk.Label(diff_frame, text="Notes différentes:", font=("Arial", 12, "bold"), anchor="w").pack(side=tk.LEFT)
    tk.Label(diff_frame, text=f"{tonic1} {mode1}: {' - '.join(diff_notes1_formatted)} | {tonic2} {mode2}: {' - '.join(diff_notes2_formatted)}", anchor="w", wraplength=400).pack(side=tk.LEFT, padx=(5, 0))

    # Insert the main frame into the Text widget
    output_text.window_create("1.0", window=main_frame)
    output_text.insert("1.0", "\n\n")

# Function to update tonality options based on selected notation
def update_tonality_options(notation_choice, tonic_combo):
    if notation_choice == "Français":
        tonalities = ['Do', 'Do#/Réb', 'Ré', 'Ré#/Mib', 'Mi', 'Fa', 'Fa#/Solb', 'Sol', 'Sol#/Lab', 'La', 'La#/Sib', 'Si']
    else:
        tonalities = ['C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B']
    tonic_combo['values'] = tonalities
    tonic_combo.set(tonalities[0])

# Function to create the main GUI
def create_gui(root):
    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Dropdown menu for notation choice
    ttk.Label(frame, text="Notation:").grid(column=0, row=0, sticky=tk.W)
    notation_choice = ttk.Combobox(frame, values=["Français", "Anglais"], state="readonly")
    notation_choice.grid(column=1, row=0, sticky=(tk.W, tk.E))
    notation_choice.set("Français")

    # Get list of modes
    modes = list(get_all_scales().keys())

    # Fields for the first mode
    ttk.Label(frame, text="Mode 1:").grid(column=0, row=1, sticky=tk.W)
    mode1_combo = ttk.Combobox(frame, values=modes, state="readonly")
    mode1_combo.grid(column=1, row=1, sticky=(tk.W, tk.E))
    mode1_combo.set(modes[0])

    ttk.Label(frame, text="Tonique 1:").grid(column=0, row=2, sticky=tk.W)
    tonic1_combo = ttk.Combobox(frame, state="readonly")
    tonic1_combo.grid(column=1, row=2, sticky=(tk.W, tk.E))

    # Fields for the second mode
    ttk.Label(frame, text="Mode 2:").grid(column=0, row=3, sticky=tk.W)
    mode2_combo = ttk.Combobox(frame, values=modes, state="readonly")
    mode2_combo.grid(column=1, row=3, sticky=(tk.W, tk.E))
    mode2_combo.set(modes[0])

    ttk.Label(frame, text="Tonique 2:").grid(column=0, row=4, sticky=tk.W)
    tonic2_combo = ttk.Combobox(frame, state="readonly")
    tonic2_combo.grid(column=1, row=4, sticky=(tk.W, tk.E))

    # Function to update all tonality options when notation changes
    def update_all_tonalities(*args):
        update_tonality_options(notation_choice.get(), tonic1_combo)
        update_tonality_options(notation_choice.get(), tonic2_combo)

    notation_choice.bind("<<ComboboxSelected>>", update_all_tonalities)
    update_all_tonalities()

    # Compare button
    compare_button = ttk.Button(frame, text="Comparer", 
                                command=lambda: compare_modes(mode1_combo.get(), tonic1_combo.get().split('/')[0], 
                                                              mode2_combo.get(), tonic2_combo.get().split('/')[0], 
                                                              'fr' if notation_choice.get() == "Français" else 'en', 
                                                              output_text))
    compare_button.grid(column=0, row=5, columnspan=2, pady=10)

    # Text area for displaying results
    output_text = tk.Text(frame, wrap=tk.WORD, width=60, height=20)
    output_text.grid(column=0, row=6, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Scrollbar for the text area
    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=output_text.yview)
    scrollbar.grid(column=2, row=6, sticky=(tk.N, tk.S))
    output_text['yscrollcommand'] = scrollbar.set

    # Configure resizing behavior
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(6, weight=1)

# Main function to run the application
def main():
    root = tk.Tk()
    root.title("Comparateur de Modes")
    create_gui(root)
    root.mainloop()

# Run the main function if this script is executed directly
if __name__ == "__main__":
    main()
