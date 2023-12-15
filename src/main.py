"""
This file contains all main function calls which will create and play a randomly-generated song.

Copyright (c) 2021 Max Wang
"""
import process_chords
import chord_tree
import create_song

# Variables (feel free to experiment)
depth_limit = 5  # Maximum depth of chord tree
length = 16  # Length of song (in beats)
tempo = 128  # Tempo (BPM)
use_simple_chords = False  # If True, only use 6 types of chords (there are 18 types otherwise)
arpeggiate = True  # If True, play each note of a chord consecutively instead of at the same time
add_melody = True
add_bassline = True

print('Creating song...')

# Extract all chords
songs = process_chords.extract_all_chords('POP909', use_simple_chords)

# Create chord tree
tree = chord_tree.ChordTree()
for song in songs:
    tree.insert_chord_progression(song, depth_limit)

# Generate song
chords = create_song.generate_chords(tree, length)
degrees = create_song.chords_to_degrees(chords)
create_song.create_midi(degrees, tempo, arpeggiate, add_melody, add_bassline)

print('Song completed.')

# Play song
create_song.play()
