# -*- coding: utf-8 -*-

from music21 import *


class Visualizer(object):
    """Simple visualization tool"""

    def __init__(self, key='C'):
        self.scale = ['C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B']
        self.key = self.scale.index(key)

    def convert_to_literals(self, chord):
        """Takes a cohrd and converts it into list of literals with the key [0-11] = [C-B]"""
        literals = []
        for n in chord.get_notes():
            literals.append(self.scale[(n + self.key) % 12])
        return literals


    def print_visualization(self, st_dat):
        print "==========================="
        print "==========================="
        print "Name: \t\t\t" + st_dat.name
        print "Description: \t" + st_dat.description
        print ""

        #sort the list in place
        st_dat.progressions.sort(key=lambda x: x.weight, reverse=True)

        #print the list of progressions
        for i in st_dat.progressions:
            print "w: " + "%.2f" % i.weight + ' \t',
            for chord in i.chords:
                out = str(self.convert_to_literals(chord))
                print out,
                for tab in range(len(out), 24):
                    print '',

            print i.description

        print "==========================="

        #create copy of the progression list to work with
        ls = st_dat.progressions[:]
        while len(ls) > 0:
            start_progression = ls[0]
            for prog_chord in start_progression.chords:
                print self.convert_to_literals(prog_chord),
            #remove used progression from list
            ls.pop(0)
            print '->',
            for j in ls:
                if start_progression.chords[-1].get_notes() == j.chords[0].get_notes():
                    for print_chord in j.chords:
                        print self.convert_to_literals(print_chord),
                    ls.remove(j)
                    break
            print ""


    def write_musicxml(self,chordlist):
        s = stream.Stream()
        for c in chordlist:
            if c == []:
                s.append(note.Rest())
            else:
                s.append(chord.Chord(c))
        xml = musicxml.m21ToString.fromStream(s)
        return xml
