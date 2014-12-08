import sys
import registry
from plugins import *
from harmstyleio import HarmonicStyleIO

if __name__=="__main__":
    style=HarmonicStyleIO.harmonic_style_from_JSON_file(sys.argv[1])
    mutate=registry.get(sys.argv[3])
    new_style=mutate.develop(style)
    HarmonicStyleIO.JSON_file_from_harmonic_style(new_style, sys.argv[2])
