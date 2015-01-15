from harmstyle import HarmonicStyle, ChordProgression, Chord
import random
import registry

class SimpleCreativity(object):
    """A simple creative style developer based on what sounds nice"""
    
    def __init__(self, sigma_factor=0.1, flip_chance=0.02, similarity_threshold=0.8, plausibility_threshold=0.5):
        self._sd_factor = sigma_factor
        self._flip_chance = flip_chance
        self._similarity_threshold = similarity_threshold
        self._plausibility_threshold = plausibility_threshold

    def develop(self, style, name="", description=""):
        """Takes a style and create a new one (now with creativity)"""
        
        ideas = self.brainstorm(style)
        new_progessions = self.select(style, ideas)
        return HarmonicStyle(name, description, new_progessions)

    def brainstorm(self, style):
        """Create new ideas with different techniques
        
        Returns a set of partial progressions (as tuples of chords)"""
        ideas = set()

        ## Single Chords
        
        # collect existing chords:
        old_chords = set()
        for p in style.progressions:
            for c in p.chords:
                old_chords.add(c)

        print("All chords:", old_chords)

        # create new chords by applying random basic operations
        r_chords = set()
        for c in old_chords:
            for i in range(5):
                r_chords.add((self.random_basic_operations(c),))
        ideas |= r_chords
        
        # stupid chord "blending"
        #b_chords = set()
        #for c1 in old_chords:
        #    for c2 in old_chords:
        #        for i in range(1,12):
        #            ns1 = c1.get_note_set()
        #            ns2 = c2.transpose(i).get_note_set()
        #            #if len(ns1 & ns2)/len(ns2)

        ## Progressions

        # collect extisting progressions
        old_progs = list(map(lambda prog: prog.chords, style.progressions))
        print("Old Progressions:", old_progs)

        # divide longer progessions, only include snippets longer than 1
        snippet_progs = []
        for oldp in [oldp for oldp in old_progs if len(oldp) > 2]:
            k = random.randrange(1,len(oldp)-1)
            if k > 1:
                snippet_progs.append(oldp[:k])
            if k < len(oldp)-1:
                snippet_progs.append(oldp[k:])
        ideas = ideas | {tuple(s) for s in snippet_progs}
        
        print("Ideas:", ideas)
        return ideas

    def select(self, old_style, ideas):
        """Creates a list of final chord progressions from the old style and new ideas"""
        new_progessions = []

        # collect existing chords:
        old_chords = set()
        for p in old_style.progressions:
            for chord in p.chords:
                old_chords.add(chord)

        # collect new chords:
        new_chords = set()
        for idea in ideas:
            for chord in idea:
                if chord not in old_chords:
                    new_chords.add(chord)
        new_chords -= old_chords # only chords that are really new
        print('New Chords:', new_chords)

        # find substitution candidates
        candidates = set()
        for old in old_chords:
            for new in new_chords:
                trans, sim = self.most_similar_transposition(old, new)
                if sim > self._similarity_threshold and sim < 1.0:
                    candidates.add((old, trans))
                else:
                    print('Rejecting candidate:', (old,trans), sim)
        print('Substitution candidates:', candidates)

        # try substituting chords
        for old_p in old_style.progressions:
            old_p_c = old_p.chords
            for cand_old, cand_new in candidates:
                if (cand_old in old_p_c):
                    # random substitution position
                    pos = random.choice([i for i, c in enumerate(old_p_c) if c == cand_old])
                    # calculate plausibility ...
                    plausibility = 0
                    old_plaus = 0
                    # with previous chord
                    if pos > 0:
                        plausibility += self.plausibility(old_p_c[pos-1], cand_new)
                        old_plaus += self.plausibility(old_p_c[pos-1], cand_old)
                    # with next chord
                    if pos < len(old_p_c) - 1:
                        plausibility += self.plausibility(cand_new, old_p_c[pos+1])
                        old_plaus += self.plausibility(cand_old, old_p_c[pos+1])
                    # scale for edge chords
                    if (pos == 0) or (pos == len(old_p_c) -1):
                        plausibility *= 2
                        old_plaus *= 2
                    if plausibility > self._plausibility_threshold*2:
                        print('Substituting', cand_old, 'with', cand_new)
                        new_p_c = old_p_c[:pos] + [cand_new] + old_p_c[pos+1:]
                        new_weight = old_p.weight-old_plaus+plausibility
                        new_p = ChordProgression(new_weight, new_p_c, old_p.description + " (substituted)")
                        new_progessions.append(new_p)
        
        #placeholder, turns every idea into one progression
        #return [ChordProgression(1, idea,"NA") for idea in ideas]
        #print("New Progressions:", new_progessions)
        return new_progessions

    def most_similar_transposition(self, base, to_transpose):
        """Finds the transposision of to_transpose most similar to base. Returns transposed, similarity"""
        max = to_transpose
        max_sim = self.chord_similarity(base, to_transpose)
        for i in range(1,11):
            transp = to_transpose.transpose(i)
            sim = self.chord_similarity(base, transp)
            if sim > max_sim:
                max = transp
                max_sim = sim
        return max, max_sim

    def chord_similarity(self, chord1, chord2):
        """Measures the similarity of chords from 0 (complementary) to 1 (equal)"""
        diff = 0
        for i in range(1, 12):
            if chord1.contains_note(i) != chord2.contains_note(i):
                diff += 1
        return 1 - (diff/12.0)

    def plausibility(self, chord1, chord2):
        """Measures the plausibility of the progressions from chord1 to chord2 between 0 (implausible) and 1 (perfectly plausible)"""
        # very simple first approach

        # fifth down?
        fifth_down = self.chord_similarity(chord1, chord2.transpose(5))

        # stepwise movement (0, +-1, +-2)
        step_movers = 0
        for n in chord1.get_note_set():
            if ({n-2, n-1, n, n+1, n+2} & chord2.get_note_set()):
                step_movers += 1
        step_movement = (len(chord2.get_notes()) / step_movers if chord2.get_notes() else 0.0)

        return (fifth_down + step_movement) / 2.0

    def random_basic_operations(self, chord):
        r_chord = self.randomize_chord(chord)
        #return r_chord.transpose((binom_transp() * 7) % 12)
        return r_chord

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

def binom_transp ():
    sum = 0
    for _ in range(6):
        if random.random() < 0.5:
            sum += 1
    return sum - 6


registry.register(SimpleCreativity)
