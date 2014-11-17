# -*- coding: utf-8 -*-
from harmstyle import HarmonicStyle, ChordProgression, Chord


class Visualizer(object):
    """Simple visualization tool"""

    @staticmethod
    def visualize(st_dat):
        print "==========================="
        print "==========================="
        print "Name: \t\t\t" + st_dat.name
        print "Description: \t"+ st_dat.description
        print ""


        #sort the list in place
        st_dat.progressions.sort(key=lambda x: x.weight, reverse=True)

        #print the list of progressions
        for i in st_dat.progressions:
            for chord in i.chords:
                print str(chord.get_notes()) + '\t',
            print '\t\t' + i.description + "\t w: " + str(i.weight)

        print "==========================="

        #create copy of the progression list to work with
        ls = st_dat.progressions[:]
        while len(ls)>0:
            start_chord = ls[0].description
            print ls[0].description,
            #remove used progression from list
            ls.pop(0)
            for j in ls:
                if start_chord[-1] == j.description[0]:
                    print "-> "+j.description[-1],
                    ls.remove(j)
                    break
            print ""
