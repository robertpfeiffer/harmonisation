# -*- coding: utf-8 -*-
from harmstyle import HarmonicStyle, ChordProgression, Chord
import json
from pprint import pprint

class IOUtils(object):
    
    @staticmethod
    def harmonic_style_from_JSON(data):
        progressions = []
        for progression in data['progressions']:
            chords = []
            for chord in progression['chords']:
                chords.append(Chord(chord))
            
            progressions.append(ChordProgression(progression['weight'], chords))
        
        return HarmonicStyle(data['name'], data['description'], progressions)

    @staticmethod
    def harmonic_style_from_JSON_file(filepath):
        with open(filepath) as data_file:    
            data = json.load(data_file)
        
        pprint(data)
        return IOUtils().harmonic_style_from_JSON(data)