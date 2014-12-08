# -*- coding: utf-8 -*-
from harmstyle import HarmonicStyle, ChordProgression, Chord
import json
from pprint import pprint

class HarmonicStyleIO(object):
    
    @staticmethod
    def harmonic_style_from_JSON(data):
        progressions = []
        for progression in data['progressions']:
            chords = []
            for chord in progression['chords']:
                chords.append(Chord(chord))
            
            progressions.append(ChordProgression(progression['weight'], chords,progression["description"]))
        
        return HarmonicStyle(data['name'], data['description'], progressions)

    @staticmethod
    def harmonic_style_from_JSON_file(filepath):
        with open(filepath) as data_file:    
            data = json.load(data_file)
        
        #pprint(data)
        return HarmonicStyleIO.harmonic_style_from_JSON(data)
        
    @staticmethod
    def JSON_file_from_harmonic_style(style, filepath):
        with open(filepath, "w") as data_file:
            json.dump(HarmonicStyleIO.JSON_from_harmonic_style(style), data_file)
    
    @staticmethod
    def JSON_from_harmonic_style(style):
        progressions = []
        for progression in style.progressions:
            chords = []
            for chord in progression.chords:
                chords.append(chord.get_notes())
            progressions.append({
                'weight': progression.weight,
                'description': progression.description,
                'chords': chords
            })
        data = {'name': style.name, 'description': style.description, 'progressions': progressions}
        return data
