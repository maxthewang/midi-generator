"""
Creating the Song

This file contains functions which generate a song using a ChordTree.

Copyright (c) 2020 Max Wang
"""
from typing import List
import random
import subprocess
from midiutil import MIDIFile
from chord_tree import ChordTree


def generate_chords(tree: ChordTree, length: int) -> List[List]:
    """
    Randomly generate chords using a ChordTree.

    Preconditions:
     - length % 4 == 0
    """
    chords = []
    new_tree = tree
    dominants = {'C': 'G', 'C#': 'G#', 'D': 'A', 'D#': 'A#', 'E': 'B', 'F': 'C',
                 'F#': 'C#', 'G': 'D', 'G#': 'D#', 'A': 'E', 'A#': 'F', 'B': 'F#'}
    first_chord = None
    chord = None

    # Generate *length* chords
    for number in range(length - 1):
        if new_tree.get_subtrees() == []:
            new_tree = tree
            new_tree = new_tree.find_subtree_by_chord(chord)

        # Choose random chord
        chord = random.choice(new_tree.get_subtrees()).chord
        new_tree = new_tree.find_subtree_by_chord(chord)
        chords.append(chord)

        if number == 0:
            first_chord = chord

    # End with dominant chord and first chord
    chords.append((dominants[first_chord[0]], '7'))
    chords.append(first_chord)

    return chords


def chords_to_degrees(chords: List[List]) -> List[List[int]]:
    """
    Convert chords to integers which correspond to pitch degrees.

    >>> chords = [['B', 'maj'], ['C#', 'maj'], ['A#', 'min'], ['D#', 'min'], ['B', 'maj']]
    >>> chords_to_degrees(chords)
    [[59, 63, 66], [49, 53, 56], [58, 61, 65], [51, 54, 58], [59, 63, 66]]
    """
    root_degrees = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5,
                    "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}
    qualities = {"maj": [0, 4, 7], "min": [0, 3, 7], "sus2": [0, 2, 7], "sus4": [0, 5, 7],
                 "maj7": [0, 4, 7, 11], "min7": [0, 3, 7, 10], "7": [0, 4, 7, 10],
                 "dim": [0, 3, 6], "aug": [0, 4, 8], "minmaj7": [0, 3, 7, 11],
                 "hdim7": [0, 3, 6, 10], "maj6": [0, 4, 7, 9], "min6": [0, 3, 7, 9],
                 "maj9": [0, 4, 7, 11, 14], "min9": [0, 3, 7, 10, 14], "9": [0, 4, 7, 10, 14],
                 "min11": [0, 3, 7, 10, 14, 17], "11": [0, 4, 7, 10, 14, 17]}
    chord_degrees = []

    # Calculate the pitches of each chord based on its root note and quality
    for chord in chords:
        root_number = root_degrees[chord[0]]
        quality = qualities[chord[1]]
        degrees = [degree + root_number + 48 for degree in quality]
        chord_degrees.append(degrees)

    return chord_degrees


def create_midi(degrees: List[List[int]], tempo: int, arpeggiate: bool,
                add_melody: bool, add_bassline) -> None:
    """
    Create the final MIDI file from the pitch degrees.
    """
    track = 0
    channel = 0
    time = 0
    duration = 4
    volume = 100

    # Initialize a MIDI file
    midi = MIDIFile(1)
    midi.addTempo(track, time, tempo)

    # Add the notes of each chord to the MIDI file
    for chord in degrees:
        if add_bassline:
            pitch = chord[0] - 12
            midi.addNote(track, channel, pitch, time, duration, volume)
        if arpeggiate:
            for pitch in chord:
                midi.addNote(track, channel, pitch, time, duration, volume)
                time += 0.5
                duration -= 0.5
            time += duration
            duration = 4
        else:
            for pitch in chord:
                midi.addNote(track, channel, pitch, time, duration, volume)
            time += duration

    # Create melody
    if add_melody:
        create_melody(midi, degrees)

    # Output the MIDI file
    with open("song.mid", "wb") as output_file:
        midi.writeFile(output_file)


def create_melody(midi: MIDIFile, degrees: List[List[int]]) -> None:
    """
    Create a melody by choosing random notes from a chord.
    """
    track = 0
    channel = 0
    time = 0
    volume = 100

    for chord in degrees:
        bar_position = 0
        while bar_position < 4:
            # Choose random notes from the current chord
            pitch = random.choice(chord) + 12

            # Choose random duration that will fit the current bar
            if bar_position > 2:
                duration = 4 - bar_position
            elif time == (len(degrees) - 1) * 4:
                duration = 4
            else:
                duration = random.choice([0.5, 1, 1.5, 2])

            midi.addNote(track, channel, pitch, time, duration, volume)
            time += duration
            bar_position += duration


def play() -> None:
    """
    Play the final result in a media player.
    """
    subprocess.Popen(["start", "song.mid"], shell=True)


if __name__ == '__main__':
    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['chord_tree', 'random', 'midiutil', 'subprocess'],
        'allowed-io': ['create_midi'],
        'max-line-length': 100,
        'disable': ['E1136']
    })

    import doctest

    doctest.testmod()
