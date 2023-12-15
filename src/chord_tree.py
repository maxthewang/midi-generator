"""
Creating a Chord Tree

This file contains functions which create a tree based on chord information.
This code is largely borrowed from Assignment 2.

Copyright (c) 2020 Max Wang
"""
from __future__ import annotations
from typing import List, Optional


class ChordTree:
    """
    A tree of possible chords.

    Instance Attributes:
     - chord: a list containing the root note and quality of the chord represented in this tree
    """
    chord: Optional[List[str]]

    # Private Instance Attributes:
    #  - _subtrees: subtrees which correspond to possible following chords
    _subtrees: list[ChordTree]

    def __init__(self, chord: Optional[List[str]] = None) -> None:
        """
        Initialize the chord tree.

        >>> chord_tree = ChordTree()
        >>> chord_tree.chord is None
        True
        """
        self.chord = chord
        self._subtrees = []

    def get_subtrees(self) -> list[ChordTree]:
        """
        Return the subtrees of this chord tree.
        """
        return self._subtrees

    def find_subtree_by_chord(self, chord: List[str, str]) -> Optional[ChordTree]:
        """
        Return the subtree corresponding to the given chord.

        Return None if no subtree corresponds to that chord.
        """
        for subtree in self._subtrees:
            if subtree.chord == chord:
                return subtree

        return None

    def add_subtree(self, subtree: ChordTree) -> None:
        """
        Add a subtree to this chord tree.
        """
        self._subtrees.append(subtree)

    def insert_chord_progression(self, chords: List, depth_limit: int = 4) -> None:
        """
        Insert a chord progression into this tree.
        """
        while len(chords) > 0:
            if len(chords) >= depth_limit:
                # Create list of chords of length depth_limit
                chords_section = chords[:depth_limit]
                chords = chords[depth_limit:]
            else:
                break
            tree = self
            while len(chords_section) > 0:
                # Move through tree until the next chord is not in the tree
                if tree.find_subtree_by_chord(chords_section[0]) is None:
                    break
                tree = tree.find_subtree_by_chord(chords_section[0])
                chords_section = chords_section[1:]
            if chords_section != []:
                # Insert tree
                reverse_chords = list(reversed(chords_section))
                new_subtree = self.tree_maker(reverse_chords)
                tree.add_subtree(new_subtree)

    def tree_maker(self, chords: List) -> ChordTree:
        """
        Create a ChordTree based on the given moves.
        """
        if len(chords) == 1:
            return ChordTree(chords[0])
        else:
            new_chord = chords.pop()
            tree = ChordTree(new_chord)
            tree.add_subtree(self.tree_maker(chords))
            return tree


if __name__ == '__main__':
    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import python_ta

    python_ta.check_all(config={
        'extra-imports': [],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['E1136']
    })

    import doctest

    doctest.testmod()
