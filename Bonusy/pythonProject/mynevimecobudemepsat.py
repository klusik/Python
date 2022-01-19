# https://www.codewars.com/kata/5f2f0754a28d9b0010f17e72

'''
There are 12 notes in an chromatic scale:

C C# D D# E F F# G G# A A# B
An octave is "the interval between one musical pitch and another with double its frequency."
That means each note has exactly double the frequency that the same note had in the octave below.
A higher n number corresponds to a higher octave and a 2^n times higher frequency.
You'll be given a string describing a note and an octave like this:

"G#5"
Your task is to calculate the frequency of the given note in Hz. The standard frequency of A4 is 440 Hz.
If you know the frequency of one note, you can calculate the frequency of any other note by
f(sought) = f(known) * 2^(D/12),
where D is the distance of the sought note from the known one on the musical scale.

For example, G#5 has the frequency of 830.61 Hz, because the distance of G# from A on the scale is -1,
and its octave is one higher than A4, so 440 Hz * 2^(-1/12) * 2^1 = 830.61 Hz.
You can also view it like G#5 is 11 steps away from A4 considering the octaves as well,
so 440 Hz * 2^(11/12) = 830.61 Hz.

Octaves of a pitch in this Kata range from -2 to 12, each starting on C and ending on B.
'''

# define all available notes
def abc():
    available_letters = ['c', 'c#', 'd', 'd#',
                         'e', 'f', 'f#', 'g',
                         'g#', 'a', 'a#', 'b']
    available_notes = []

    # generate list of all available notes
    # as combination of available notes
    # and available octaves
    for octave in range(-2, 13):
        for letter in available_letters:
            add_note = letter + str(octave)
            available_notes.append(add_note)

    return available_notes

# find distance between basic note and user selected note
def find_dinstance(note, available_notes):
    '''
    :param note: note you are looking for
    :return: distance (count of notes) from a0
    '''
    # find index of user note
    if note in available_notes:
        note_index = available_notes.index(note)
    else:
        print('note not availabe')

    # base note is a0
    base_note = 'a0'
    # index of base note
    base_note_index = available_notes.index('a0')

    # calculate distance between notese using list slice
    distance = len(available_notes[base_note_index: note_index])
    # solution for notes lower than base note
    if base_note_index > note_index:
        distance = # 'offset' needed

    return distance

def calcfreq(available_notes):
    base_freq = 440
    base_note = 'a0'

    # dict will combine name of the note with it's frequency
    notes_freq = {}

    # fill dict of note/frequency pairs
    for note in available_notes:
        # calculate frequency of the note
        f_unknown = base_freq * 2 ** (abs(find_dinstance(note, available_notes) / 12))
        notes_freq[note] = f_unknown

    return notes_freq

# RUNTIME

mynotes = abc()
print(calcfreq(mynotes))




