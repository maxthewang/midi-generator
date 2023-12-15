"""
Processing Chords

This file contains functions which process the chords from text files in a folder.

Copyright (c) 2020 Max Wang
"""
from typing import List


def extract_all_chords(folder: str, use_simple_chords: bool) -> List[List[List]]:
    """
    Extract all chords from each song in the folder.

    Preconditions:
     - folder contains folders with POP909 text files

    >>> songs = extract_all_chords('POP909', True)
    >>> songs[0][0]
    ['B', 'maj7']
    """
    songs = []

    # Iterate through all folders
    for inner_folder in range(1, 910):
        inner_folder = str(inner_folder).zfill(3)
        filename = f'{folder}/{inner_folder}/chord_audio.txt'
        songs.append(extract_chords(filename, use_simple_chords))

    return songs


def extract_chords(filename: str, use_simple_chords: bool) -> List[List[str]]:
    """
    Extract a list of chords from a chord_audio text file.

    Preconditions:
    - filename is a valid file
    - filename[-15:] == 'chord_audio.txt'

    >>> song = extract_chords('POP909/001/chord_audio.txt', True)
    >>> song[0]
    ['B', 'maj7']
    """
    new_note_names = {'Eb': 'D#', 'Gb': 'F#', 'Ab': 'G#', 'Bb': 'A#'}
    simpler_chords = {'maj6': 'maj', 'min6': 'min', '7': 'maj7', 'maj9': 'maj7', 'min9': 'min7',
                     '9': 'maj7', 'aug': 'maj', 'dim': 'min', 'hdim7': 'min7', 'minmaj7': 'min7',
                     'min11': 'min7', '11': 'maj7'}

    with open(filename) as text:
        chords = []

        for line in text:
            # Find chord name
            chord = line.split('\t')[2][:-1]
            if chord != 'N':
                # Split chord into list [root note, quality]
                chord = chord.split(':')
                if chord[0] in new_note_names:
                    chord[0] = new_note_names[chord[0]]
                # Remove slashes and parentheses (those chords are too complicated)
                chord[1] = chord[1].split('/')[0]
                chord[1] = chord[1].split('(')[0]
                chords.append(chord)

    # Reduce chords to simpler chords if use_simple_chords is True
    if use_simple_chords:
        for chord in chords:
            if chord[1] not in ['maj', 'min', 'maj7', 'min7', 'sus2', 'sus4']:
                chord[1] = simpler_chords[chord[1]]

    return chords


if __name__ == '__main__':
    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import python_ta

    python_ta.check_all(config={
        'extra-imports': [],
        'allowed-io': ['extract_chords'],
        'max-line-length': 100,
        'disable': ['E1136']
    })

    import doctest

    doctest.testmod()
