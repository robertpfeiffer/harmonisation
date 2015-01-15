class HarmonicStyle(object):
    """Representation of a Harmonic Style"""
    
    def __init__(self, name, description, progressions):
        self.name = name
        self.description = description
        self.progressions = progressions

class ChordProgression(object):
    """A single Chord Progession"""
    
    def __init__(self, weight, chords, description):
        self.weight = weight
        self.chords = chords
        self.description = description

    def __repr__(self):
        return 'ChordProgression(' + repr(self.weight) + ',' + repr(self.chords) + ',' + repr(self.description) + ')'

class Chord(object):
    """A set of simultaneous notes"""
    
    def __init__(self, notes):
        self._notes = frozenset(notes)
        self._normalize()

    def _normalize(self):
        self._notes = frozenset({x % 12 for x in self._notes})
    
    def contains_note(self, note):
        """Tests whether the Chord contains the Note"""
        return note in self._notes

    def get_notes(self):
        """Returns the notes as a sorted list"""
        self._normalize()
        notes = list(self._notes)
        notes.sort()
        return notes

    def get_note_set(self):
        """Returns the notes as a set"""
        self._normalize()
        return self._notes

    def transpose(self,n):
        return Chord({x+n for x in self._notes})

    def __str__(self):
        return str(self.get_notes())

    def __repr__(self):
        return "Chord(" + repr(self.get_notes()) + ")"

    def __eq__(x, y):
        return x.get_notes() == y.get_notes()

    def __hash__(self):
        return hash(self.get_note_set())
