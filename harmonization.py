# -*- coding: utf-8 -*-
import networkx as nx

class Harmonization(object):

    def harmonize(self, harm_style, melody, keynote, octave):
        """
        Harmonization method, takes an harmonic style, the melody wrt. the keynote, the keynote and the octave (0-7 on a piano)
        uses http://networkx.github.io/documentation/networkx-1.9.1/
        """
        
        fitting_progressions = []
        
        """ Collect all correct progressions for each note """
        for i, note in enumerate(melody):
            fitting_progressions.append([])
            for progression in harm_style.progressions:
                if len(progression.chords) > len(melody)-i:
                    continue
                
                for j, chord in enumerate(progression.chords):
                    if melody[i+j] not in chord.get_notes():
                        break
                else:
                    fitting_progressions[i].append(progression)
                    
        """ Debugging stuff """
#        for ix, x in enumerate(fitting_progressions):
#            print ('\n')
#            for iy, y in enumerate(fitting_progressions[ix]):
#                for c in y.chords:
#                    print(c.get_notes())
                    
#       Probably need: http://networkx.github.io/documentation/networkx-1.9.1/reference/classes.multidigraph.html#networkx.MultiDiGraph
#       TODO use MultiDiGraph = multiple edges can connect two nodes to prevent jumping between progressions, but not many algorithms well defined
        G = nx.DiGraph()
        
        """ Build graph from progressions """
        for ix, x in enumerate(fitting_progressions):
            for iy, y in enumerate(fitting_progressions[ix]):
                progression = fitting_progressions[ix][iy]
                first_chord = progression.chords[0]
                last_chord = progression.chords[-1]
                if ix is len(melody):
#                    G.add_edge("START", "END")
#                    TODO connect to end node
                    pass
                else:
                    t1 = (tuple(first_chord.get_notes()), ix)
                    t2 = (tuple(last_chord.get_notes()), ix+len(progression.chords)-1)
                    
                    if ix is 0:
                        G.add_edge("START", t1)
                    
                    G.add_edge(t1, t2, weight=progression.weight, object=progression)
                    
#       TODO remove too long paths
#       TODO prune graph
#       TODO find path of maximum weights -> implement viterbi? http://en.wikipedia.org/wiki/Viterbi_algorithm 
        nx.draw_networkx(G)
