"""Creates a graphical user interface for searching musical modes based on input notes or chords. It allows users to select a notation system, input type, and enter notes or chords to find matching modes."""

# Import necessary libraries and modules
import tkinter as tk
from tkinter import ttk
from common import get_all_scales, get_scale_notes, format_notes, get_enharmonic_equivalent

# Function to parse chord input and return a list of notes
def parse_chord(chord_str, notation):
    # Define note names in English and French
    notes_en = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    notes_fr = ['Do', 'Do#', 'Ré', 'Ré#', 'Mi', 'Fa', 'Fa#', 'Sol', 'Sol#', 'La', 'La#', 'Si']
    notes_fr_to_en = dict(zip(notes_fr, notes_en))
    
    # Define chord types and their corresponding intervals
    chord_types = {
        '': [0, 4, 7],  # Major
        'm': [0, 3, 7],  # Minor
        'dim': [0, 3, 6],  # Diminished
        'aug': [0, 4, 8],  # Augmented
        '7': [0, 4, 7, 10],  # Dominant 7th
        'maj7': [0, 4, 7, 11],  # Major 7th
        'm7': [0, 3, 7, 10],  # Minor 7th
        'dim7': [0, 3, 6, 9],  # Diminished 7th
        'm7b5': [0, 3, 6, 10]  # Half-diminished 7th
    }
    
    # Choose the appropriate note list based on the notation
    notes = notes_en if notation == 'en' else notes_fr
    
    # Convert input to appropriate format
    chord_str = chord_str.capitalize()
    
    # Check if the chord is in the format "Am", "Cmaj7", etc.
    for chord_type, intervals in chord_types.items():
        if chord_str.lower().endswith(chord_type.lower()):
            root = chord_str[:-len(chord_type) if chord_type else None]
            if notation == 'fr':
                root = notes_fr_to_en.get(root, root)
            if root in notes_en:
                root_index = notes_en.index(root)
                return [notes[(root_index + interval) % 12] for interval in intervals]
    
    # If not, split the chord string by '-'
    return [note.strip().capitalize() for note in chord_str.split('-')]

# Function to find scales containing the input notes or chords
def find_scales_with_input(input_items, notation, is_chord):
    scales = get_all_scales()
    notes_en = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    notes_fr = ['Do', 'Do#', 'Ré', 'Ré#', 'Mi', 'Fa', 'Fa#', 'Sol', 'Sol#', 'La', 'La#', 'Si']
    notes = notes_en if notation == 'en' else notes_fr
    matching_scales = []

    # Convert inputs to appropriate format
    input_items = [item.capitalize() for item in input_items]

    # Check each scale for containing the input notes or chords
    for tonic in notes:
        for scale_name, intervals in scales.items():
            scale_notes = get_scale_notes(intervals, tonic, notation)
            if is_chord:
                if all(all(note in scale_notes or get_enharmonic_equivalent(note, notation) in scale_notes for note in parse_chord(chord, notation)) for chord in input_items):
                    matching_scales.append((tonic, scale_name))
            else:
                if all(note in scale_notes or get_enharmonic_equivalent(note, notation) in scale_notes for note in input_items):
                    matching_scales.append((tonic, scale_name))

    return matching_scales

# Function to format input string based on notation
def format_input(input_string, notation):
    if notation == 'fr':
        notes = ['Do', 'Ré', 'Mi', 'Fa', 'Sol', 'La', 'Si']
    else:
        notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    
    formatted_input = []
    for item in input_string.split():
        for note in notes:
            if item.lower() == note.lower():
                formatted_input.append(note)
                break
        else:
            formatted_input.append(item.capitalize())
    
    return ' '.join(formatted_input)

# Function to search for scales and display results
def search_scales(input_type, input_string, notation, output_text):
    input_items = input_string.split()
    is_chord = input_type == "Accords"

    matching_scales = find_scales_with_input(input_items, notation, is_chord)

    # Format input for display
    formatted_input = format_input(input_string, notation)

    # Create main frame for displaying results
    main_frame = tk.Frame(output_text, bd=2, relief=tk.SOLID)
    
    # Add title
    title_label = tk.Label(main_frame, text=f"Recherche de modes contenant la série de {input_type.lower()} : {formatted_input}", font=("Arial", 12, "bold"), anchor="w", wraplength=400)
    title_label.pack(fill=tk.X, padx=5, pady=5)

    # Display matching scales or no result message
    if matching_scales:
        result_text = tk.Text(main_frame, wrap=tk.WORD, height=10, width=50)
        result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)
        result_text.insert(tk.END, "Modes correspondants :\n")
        for tonic, scale_name in matching_scales:
            result_text.insert(tk.END, f"• {tonic} {scale_name}\n")
        result_text.config(state=tk.DISABLED)
    else:
        no_result_label = tk.Label(main_frame, text=f"Aucun mode ne contient la série de {input_type.lower()} spécifiée.", anchor="w", wraplength=400)
        no_result_label.pack(fill=tk.X, padx=5, pady=2)

    # Insert the main frame into the Text widget
    output_text.window_create("1.0", window=main_frame)
    output_text.insert("1.0", "\n\n")

# Function to update tonality options based on selected notation
def update_tonality_options(notation_choice, tonic_combo):
    if notation_choice == "Français":
        tonalities = ['Do', 'Ré', 'Mi', 'Fa', 'Sol', 'La', 'Si']
    else:
        tonalities = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
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

    # Dropdown menu for input type (Notes or Chords)
    ttk.Label(frame, text="Type d'entrée:").grid(column=0, row=1, sticky=tk.W)
    input_type = ttk.Combobox(frame, values=["Notes", "Accords"], state="readonly")
    input_type.grid(column=1, row=1, sticky=(tk.W, tk.E))
    input_type.set("Notes")

    # Input field for notes or chords
    ttk.Label(frame, text="Entrez les notes ou accords\n(séparés par des espaces)").grid(column=0, row=2, sticky=tk.W)
    input_entry = ttk.Entry(frame, width=40)
    input_entry.grid(column=1, row=2, sticky=(tk.W, tk.E))

    # Search button
    search_button = ttk.Button(frame, text="Rechercher", 
                               command=lambda: search_scales(input_type.get(), input_entry.get(), 'fr' if notation_choice.get() == "Français" else 'en', output_text))
    search_button.grid(column=0, row=3, columnspan=2, pady=10)

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
    root.title("Recherche de Modes")
    create_gui(root)
    root.mainloop()

# Run the main function if this script is executed directly
if __name__ == "__main__":
    main()
