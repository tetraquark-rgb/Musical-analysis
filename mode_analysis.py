"""This code creates a graphical user interface for analyzing musical modes. It allows users to select a notation system, tonality, and mode, and then displays the notes of the mode along with the corresponding triads and tetrads. """
# Import necessary libraries and modules
import tkinter as tk
from tkinter import ttk
from common import get_all_scales, get_scale_notes, identify_chord, format_notes, get_enharmonic_equivalent

# Function to generate triads and tetrads from a given set of mode notes
def generate_chords(mode_notes):
    triads = []
    tetrads = []
    for i in range(len(mode_notes)):
        root = mode_notes[i]
        third = mode_notes[(i + 2) % len(mode_notes)]
        fifth = mode_notes[(i + 4) % len(mode_notes)]
        seventh = mode_notes[(i + 6) % len(mode_notes)]
        triads.append([root, third, fifth])
        tetrads.append([root, third, fifth, seventh])
    return triads, tetrads

# Main function to analyze the selected mode and display results
def analyze_mode(tonic, mode, notation, output_text):
    scales = get_all_scales()
    if mode.lower() not in scales:
        output_text.insert("1.0", f"Mode '{mode}' non reconnu.\n\n")
        return

    # Get mode notes and format them
    mode_notes = get_scale_notes(scales[mode.lower()], tonic, notation)
    mode_notes_formatted = format_notes(mode_notes, notation)

    # Generate and format chords
    triads, tetrads = generate_chords(mode_notes)
    triads_formatted = [format_notes(chord, notation) for chord in triads]
    tetrads_formatted = [format_notes(chord, notation) for chord in tetrads]

    # Create main frame for displaying results
    main_frame = tk.Frame(output_text, bd=2, relief=tk.SOLID)
    
    # Add title
    title_label = tk.Label(main_frame, text=f"Analyse du mode {tonic} {mode}", font=("Arial", 14, "bold"), anchor="w")
    title_label.pack(fill=tk.X, padx=5, pady=5)

    # Display mode notes
    notes_frame = tk.Frame(main_frame)
    notes_frame.pack(fill=tk.X, padx=5, pady=2)
    tk.Label(notes_frame, text="Notes du mode:", font=("Arial", 12, "bold"), anchor="w").pack(side=tk.LEFT)
    tk.Label(notes_frame, text=" - ".join(mode_notes_formatted), anchor="w").pack(side=tk.LEFT, padx=(5, 0))

    # Display triads
    triads_frame = tk.Frame(main_frame)
    triads_frame.pack(fill=tk.X, padx=5, pady=2)
    tk.Label(triads_frame, text="Triades:", font=("Arial", 12, "bold"), anchor="w").pack(side=tk.LEFT)
    triads_label = tk.Label(triads_frame, text="", anchor="w", justify=tk.LEFT)
    triads_label.pack(side=tk.LEFT, padx=(5, 0))
    triads_text = ""
    for i, chord in enumerate(triads_formatted, 1):
        chord_type, usual_name = identify_chord(chord, notation)
        triads_text += f"Triade {i}: {' - '.join(chord)} ({chord[0]} {chord_type}, nom usuel: {usual_name})\n"
    triads_label.config(text=triads_text)

    # Display tetrads
    tetrads_frame = tk.Frame(main_frame)
    tetrads_frame.pack(fill=tk.X, padx=5, pady=2)
    tk.Label(tetrads_frame, text="Tétrades:", font=("Arial", 12, "bold"), anchor="w").pack(side=tk.LEFT)
    tetrads_label = tk.Label(tetrads_frame, text="", anchor="w", justify=tk.LEFT)
    tetrads_label.pack(side=tk.LEFT, padx=(5, 0))
    tetrads_text = ""
    for i, chord in enumerate(tetrads_formatted, 1):
        chord_type, usual_name = identify_chord(chord, notation)
        tetrads_text += f"Tétrade {i}: {' - '.join(chord)} ({chord[0]} {chord_type}, nom usuel: {usual_name})\n"
    tetrads_label.config(text=tetrads_text)

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

    # Dropdown menu for tonality choice
    ttk.Label(frame, text="Tonalité:").grid(column=0, row=1, sticky=tk.W)
    tonic_combo = ttk.Combobox(frame, state="readonly")
    tonic_combo.grid(column=1, row=1, sticky=(tk.W, tk.E))
    update_tonality_options(notation_choice.get(), tonic_combo)

    # Update tonalities when notation changes
    notation_choice.bind("<<ComboboxSelected>>", lambda event: update_tonality_options(notation_choice.get(), tonic_combo))

    # Dropdown menu for mode choice
    modes = list(get_all_scales().keys())
    ttk.Label(frame, text="Mode:").grid(column=0, row=2, sticky=tk.W)
    mode_combo = ttk.Combobox(frame, values=modes, state="readonly")
    mode_combo.grid(column=1, row=2, sticky=(tk.W, tk.E))
    mode_combo.set(modes[0])

    # Analyze button
    analyze_button = ttk.Button(frame, text="Analyser", 
                                command=lambda: analyze_mode(tonic_combo.get().split('/')[0], mode_combo.get(), 'fr' if notation_choice.get() == "Français" else 'en', output_text))
    analyze_button.grid(column=0, row=3, columnspan=2, pady=10)

    # Text area for displaying results
    output_text = tk.Text(frame, wrap=tk.WORD, width=60, height=20)
    output_text.grid(column=0, row=4, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
    output_text.tag_configure("bold", font=("Arial", 12, "bold"))

    # Scrollbar for the text area
    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=output_text.yview)
    scrollbar.grid(column=2, row=4, sticky=(tk.N, tk.S))
    output_text['yscrollcommand'] = scrollbar.set

    # Configure resizing behavior
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(4, weight=1)

# Main function to run the application
def main():
    root = tk.Tk()
    root.title("Analyse de Mode")
    create_gui(root)
    root.mainloop()

# Run the main function if this script is executed directly
if __name__ == "__main__":
    main()
