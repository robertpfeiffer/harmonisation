from harmstyle import HarmonicStyle, ChordProgression, Chord
import random
import registry

class SimpleCreativity(object):
    """A simple creative style developer based on what sounds nice

    To be done!
    At the moment, this is a copy of the RandomCreativity."""
    
    def __init__(self, sigma_factor=0.1, flip_chance=0.02):
        self._sd_factor = sigma_factor
        self._flip_chance = flip_chance

    def develop(self, style, name="", description=""):
        """Takes a style and create a new one"""
        new_progessions = list(map(self.randomize_progression, style.progressions))
        return HarmonicStyle(name, description, new_progessions)

    def randomize_progression(self, progression):
        """Takes a ChordProgression and applies some random changes to it"""
        new_weight = random.gauss(progression.weight, self._sd_factor*progression.weight)
        new_chords = list(map(self.randomize_chord, progression.chords))
        return ChordProgression(new_weight, new_chords, description="NA")

    def randomize_chord(self, chord):
        """Takes a Chord and applies some random changes to it"""
        new_notes = set(chord.get_notes())
        for i in range(12):
            if random.random() < self._flip_chance:
                if i in new_notes:
                    new_notes.remove(i)
                else:
                    new_notes.add(i)
        return Chord(new_notes)

registry.register(SimpleCreativity)
