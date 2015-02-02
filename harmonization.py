# -*- coding: utf-8 -*-

# http://networkx.github.io/documentation/networkx-1.9.1/
import networkx as nx
import pprint, sys, json
from harmstyleio import HarmonicStyleIO

class Harmonization(object):

    # TODO: implement all_paths = True
    def harmonize(self, harm_style, melody, keynote, octave, all_paths=False):
        """
        Harmonization method, takes an harmonic style, the melody wrt. the keynote, the keynote and the octave (0-7 on a piano)
        Returns a list of Chords.
        """
        
        fitting_progressions = []
        max_weight = 0
        
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
                    if progression.weight > max_weight:
                        max_weight = progression.weight
                    
        """ Debugging stuff """
#        for ix, x in enumerate(fitting_progressions):
#            print ('\n')
#            for iy, y in enumerate(fitting_progressions[ix]):
#                for c in y.chords:
#                    print(c.get_notes())
        
        G = nx.DiGraph() if not all_paths else nx.MultiDiGraph()
        
        """ Build graph from progressions """
        for ix, x in enumerate(fitting_progressions):
            for iy, y in enumerate(fitting_progressions[ix]):
                progression = fitting_progressions[ix][iy]
                first_chord = progression.chords[0]
                last_chord = progression.chords[-1]

                t1 = (tuple(first_chord.get_notes()), ix)
                t2 = (tuple(last_chord.get_notes()), ix+len(progression.chords)-1)
                
                if ix is 0:
                    G.add_edge("START", t1)

                # Add edge if we have a multigraph, the nodes or the edge don't exist yet or the existing edge has a higher weight
                if (all_paths or \
                    not G.has_node(t1) or \
                    not G.has_node(t2) or \
                    not G.has_edge(t1,t2) or \
                    G[t1][t2]['weight'] > max_weight-progression.weight):
                        G.add_edge(t1, t2, weight=max_weight-progression.weight, prog=progression)    
                
                
                if ix+len(progression.chords) is len(melody):
                    G.add_edge(t2, "END")
                    
        # Drawing the graph
        # nx.draw_networkx(G)
        
        # This is where the magic happens    
        length,path = nx.bidirectional_dijkstra(G,"START","END")
        
        # Get edges from node path
        last_node = path[1]
        path_trimmed = path[2:-1]
        harmonies = []
        for ix, x in enumerate(path_trimmed):
            current_node = path_trimmed[ix]
            chords = G[last_node][current_node]['prog'].chords
            
            if ix is 0:
                harmonies.extend(chords)
            else:
                harmonies.extend(chords[1:])
            
            last_node = path_trimmed[ix]
        
        pprint.pprint(harmonies)
        return harmonies

# currently simplified for testing:
# $ python3 harmonization.py style.json harmonization.json [7,4,4,5,2,2,0,2,4,5,7,7,7]
if __name__ == "__main__":
    style = HarmonicStyleIO.harmonic_style_from_JSON_file(sys.argv[1])
    melody = json.loads(sys.argv[3])
    h = Harmonization()
    chords = h.harmonize(style, melody, 0, 0)
    harm = {"melody": melody, "chords": [c.get_notes() for c in chords]}
    with open(sys.argv[2], "w") as out_file:
        json.dump(harm, out_file)
