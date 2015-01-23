# -*- coding: utf-8 -*-
from harmstyleio import HarmonicStyleIO
from style_visualizer import Visualizer
import sys

if __name__=="__main__":
    style=HarmonicStyleIO.harmonic_style_from_JSON_file(sys.argv[1])
    outpath = sys.argv[2]

vis = Visualizer('C')

#get chord list out of style
chordlist = []
for prog in style.progressions:
    for c in prog.chords:
        chordlist.append(c.get_notes())
    chordlist.append([])
print chordlist
#open file the xml in wrote to
outfile = open(outpath, "w")
xml = vis.write_musicxml(chordlist)
outfile.write(xml)
outfile.close()
