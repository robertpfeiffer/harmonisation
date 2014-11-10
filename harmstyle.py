class HarmonicStyle(object):
    """Representation of a Harmonic Style"""
    
    def __init__(self, name, description, progressions):
        self.name = name
        self.description = description
        self.progressions = progressions

class ChordProgression(object):
    """A single Chord Progession"""
    
    def __init__(self, weight, chords):
        self.weight = weight
        self.chords = chords

class Chord(object):
    """A set of simultaneous notes"""
    
    def __init__(self, notes):
        self._notes = set(notes)
        self._normalize()
        
    def _normalize(self):
        self._notes = {x % 12 for x in self._notes}
    
    def contains_note(self, note):
        """Tests, wheather the Chord contains the Note"""
        return note in self._notes

    def get_notes(self):
        self._normalize()
        notes = list(self._notes)
        notes.sort()
        return notes
