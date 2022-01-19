def ABC():
    available_letters = ['c', 'c#', 'd', 'd#',
                        'e', 'f', 'f#', 'g',
                        'g#', 'a', 'a#', 'b']
    available_notes = []
    
    # generate list of all available notes
    for octave in range (-2, 13):
        for letter in available_letters:
            addNote = str(octave) + letter
            available_notes.append(addNote)
            
    return available_notes

print(ABC())
