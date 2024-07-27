"""This code provides a set of utility functions for working with musical scales, chords, and note names in both English and French notations. It includes functionality for identifying chord types, generating scale 
notes, formatting note names, and finding enharmonic equivalents"""
# common.py

# This function returns a dictionary of all scales with their corresponding intervals
def get_all_scales():
    # Each scale is represented by a list of semitone intervals from the root note
    return {
        'ionien': [0, 2, 4, 5, 7, 9, 11],
        'dorien': [0, 2, 3, 5, 7, 9, 10],
        'phrygien': [0, 1, 3, 5, 7, 8, 10],
        'lydien': [0, 2, 4, 6, 7, 9, 11],
        'mixolydien': [0, 2, 4, 5, 7, 9, 10],
        'éolien': [0, 2, 3, 5, 7, 8, 10],
        'locrien': [0, 1, 3, 5, 6, 8, 10],
        'mineur mélodique': [0, 2, 3, 5, 7, 9, 11],
        'dorien b2': [0, 1, 3, 5, 7, 9, 10],
        'lydien augmenté': [0, 2, 4, 6, 8, 9, 11],
        'lydien dominant': [0, 2, 4, 6, 7, 9, 10],
        'mixolydien b6': [0, 2, 4, 5, 7, 8, 10],
        'éolien b5': [0, 2, 3, 5, 6, 8, 10],
        'super locrien': [0, 1, 3, 4, 6, 8, 10],
        'mineur harmonique': [0, 2, 3, 5, 7, 8, 11],
        'locrien #6': [0, 1, 3, 5, 6, 9, 10],
        'ionien #5': [0, 2, 4, 5, 8, 9, 11],
        'dorien #4': [0, 2, 3, 6, 7, 9, 10],
        'phrygien dominant': [0, 1, 4, 5, 7, 8, 10],
        'lydien #2': [0, 3, 4, 6, 7, 9, 11],
        'super locrien bb7': [0, 1, 3, 4, 6, 8, 9]
    }

# This function generates the notes of a scale based on the given intervals, tonic, and notation
def get_scale_notes(intervals, tonic, notation='en'):
    # Define note names in English and French
    notes_en = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    notes_fr = ['Do', 'Do#', 'Ré', 'Ré#', 'Mi', 'Fa', 'Fa#', 'Sol', 'Sol#', 'La', 'La#', 'Si']
    
    # Choose the appropriate note list based on the notation
    notes = notes_en if notation == 'en' else notes_fr
    tonic = tonic.capitalize()
    
    # Find the index of the tonic note
    tonic_index = notes.index(tonic)
    scale_notes = []
    
    # Generate the scale notes by applying the intervals to the tonic
    for interval in intervals:
        note_index = (tonic_index + interval) % 12
        scale_notes.append(notes[note_index])
    
    return scale_notes

# This function identifies the chord type and usual name based on the given notes
def identify_chord(chord, notation):
    # Define note names and create dictionaries for translation between French and English
    notes_en = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    notes_fr = ['Do', 'Do#', 'Ré', 'Ré#', 'Mi', 'Fa', 'Fa#', 'Sol', 'Sol#', 'La', 'La#', 'Si']
    notes_fr_to_en = dict(zip(notes_fr, notes_en))
    notes_en_to_fr = dict(zip(notes_en, notes_fr))
    
    # Capitalize all notes in the chord
    chord = [note.capitalize() for note in chord]
    
    # Convert French notation to English if necessary
    if notation == 'fr':
        notes = notes_fr
        chord_en = [notes_fr_to_en[note] if note in notes_fr_to_en else note for note in chord]
    else:
        notes = notes_en
        chord_en = chord
    
    # Extract root, third, and fifth from the chord
    root, third, fifth = chord_en[:3]
    
    # Calculate intervals between root and other notes
    root_index = notes_en.index(root)
    third_interval = (notes_en.index(third) - root_index) % 12
    fifth_interval = (notes_en.index(fifth) - root_index) % 12
    
    # Initialize chord type and usual name
    chord_type = ""
    usual_name = ""

    # Identify chord type for triads
    if len(chord_en) == 3:  # Triade
        if third_interval == 4 and fifth_interval == 7:
            chord_type = "majeur"
            usual_name = chord[0] if notation == 'fr' else root
        elif third_interval == 3 and fifth_interval == 7:
            chord_type = "mineur"
            usual_name = f"{chord[0]}m" if notation == 'fr' else f"{root}m"
        elif third_interval == 3 and fifth_interval == 6:
            chord_type = "diminué"
            usual_name = f"{chord[0]}dim" if notation == 'fr' else f"{root}dim"
        elif third_interval == 4 and fifth_interval == 8:
            chord_type = "augmenté"
            usual_name = f"{chord[0]}aug" if notation == 'fr' else f"{root}aug"
    elif len(chord_en) == 4:  # Tétrade
        seventh = chord_en[3]
        seventh_interval = (notes_en.index(seventh) - root_index) % 12
        
    # Identify chord type for tetrads
    elif len(chord_en) == 4:
        seventh = chord_en[3]
        seventh_interval = (notes_en.index(seventh) - root_index) % 12

        if third_interval == 4 and fifth_interval == 7:
            if seventh_interval == 11:
                chord_type = "majeur 7"
                usual_name = f"{chord[0]}maj7" if notation == 'fr' else f"{root}maj7"
            elif seventh_interval == 10:
                chord_type = "dominant 7"
                usual_name = f"{chord[0]}7" if notation == 'fr' else f"{root}7"
        elif third_interval == 3 and fifth_interval == 7:
            if seventh_interval == 10:
                chord_type = "mineur 7"
                usual_name = f"{chord[0]}m7" if notation == 'fr' else f"{root}m7"
            elif seventh_interval == 11:
                chord_type = "mineur majeur 7"
                usual_name = f"{chord[0]}mMaj7" if notation == 'fr' else f"{root}mMaj7"
        elif third_interval == 3 and fifth_interval == 6:
            if seventh_interval == 9:
                chord_type = "diminué 7"
                usual_name = f"{chord[0]}dim7" if notation == 'fr' else f"{root}dim7"
            elif seventh_interval == 10:
                chord_type = "demi-diminué 7"
                usual_name = f"{chord[0]}m7b5" if notation == 'fr' else f"{root}m7b5"
        elif third_interval == 4 and fifth_interval == 8 and seventh_interval == 11:
            chord_type = "majeur 7 quinte augmenté"
            usual_name = f"{chord[0]}maj7(#5)" if notation == 'fr' else f"{root}maj7(#5)"

    # If chord type is not identified, mark as non-standard
    if not chord_type:
        chord_type = "non standard"
        usual_name = "N/A"
    
    return chord_type, usual_name

# This function prints the chords with their names and usual names
def print_chords(chords, chord_type, notation):
    for i, chord in enumerate(chords, 1):
        chord_name, usual_name = identify_chord(chord, notation)
        print(f"{chord_type} {i}: {' - '.join(chord)} ({chord[0]} {chord_name}, nom usuel: {usual_name})")

# This function formats note names based on the notation
def format_note_name(note, notation):
    if notation == 'fr':
        notes_fr = ['Do', 'Do#', 'Ré', 'Ré#', 'Mi', 'Fa', 'Fa#', 'Sol', 'Sol#', 'La', 'La#', 'Si']
        notes_fr_formatted = ['Do', 'Do#', 'Ré', 'Ré#', 'Mi', 'Fa', 'Fa#', 'Sol', 'Sol#', 'La', 'La#', 'Si']
        note_dict = dict(zip(notes_fr, notes_fr_formatted))
        return note_dict.get(note, note)
    else:
        return note.capitalize()
    
# This function formats a list of notes based on the notation

def format_notes(notes, notation):
    return [format_note_name(note, notation) for note in notes]

# This function returns the enharmonic equivalent of a given note
def get_enharmonic_equivalent(note, notation):
    # Define enharmonic equivalents for English and French notations
    enharmonic_dict_en = {
        'C#': 'Db', 'D#': 'Eb', 'E#': 'F', 'F#': 'Gb', 'G#': 'Ab', 'A#': 'Bb', 'B#': 'C',
        'Db': 'C#', 'Eb': 'D#', 'Fb': 'E', 'Gb': 'F#', 'Ab': 'G#', 'Bb': 'A#', 'Cb': 'B'
    }
    enharmonic_dict_fr = {
        'Do#': 'Réb', 'Ré#': 'Mib', 'Mi#': 'Fa', 'Fa#': 'Solb', 'Sol#': 'Lab', 'La#': 'Sib', 'Si#': 'Do',
        'Réb': 'Do#', 'Mib': 'Ré#', 'Fab': 'Mi', 'Solb': 'Fa#', 'Lab': 'Sol#', 'Sib': 'La#', 'Dob': 'Si'
    }
    # Return the enharmonic equivalent based on the notation
    if notation == 'en':
        return enharmonic_dict_en.get(note, note)
    else:
        return enharmonic_dict_fr.get(note, note)