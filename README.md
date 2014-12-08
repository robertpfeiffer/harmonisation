# Harmonisation

This repository contains the code for the seminar "Computational Accounts for Melodic Harmonisation".

In short, the idea is the following:

1. A *harmonic style* is used to express allowed preferred chord progressions. These are the building blocks for a harmonization.
2. A *creativity* takes a basic harmonic style and "creatively" builds a new harmonic style from it.
3. A *harmonizer* takes a melody and a style definition and harmonizes the melody according to the style.

In the prototype phase, all of this is implemented in Python.

## Harmonic Styles

A harmonic style for the purpose of this project is a set of chord progressions with weights.
A chord progression is a simple list of chords.
Its weight indicates how much it is preferred over other chord progressions.
Chords are represented as a list of chromatic notes in one octave relative to an unknown reference note (e.g. the root of the melody's key).
For example, the simple tonic could be expressed as

    [0,4,7]

A perfect cadence could then be expressed as

    [[0,4,7], [2,7,11], [0,4,7]]

Actual chords can be obtained from these descriptions by defining a reference note, e.g., for the reference note c the former progression would be equivalent to C G C.
Note that the given numbers do not indicate the octave or order of the given note.
While `[2,7,11]` stands for d, g, and b (for reference note c), the g could also be realized as the bass note.

This kind of style definition has not much to do with the usual notion of a musical style, it reduces it to a preference of chord progressions.

Style files are encoded in JSON, as can be seen in [dummy_style.json](dummy_style.json).
The class hierarchy for styles can be found in [harmstyle.py](harmstyle.py), JSON loading/saving is implemented in [harmstyleio.py](harmstyleio.py).

## Harmonizer

The harmonizer applies a harmonic style to a melody in a deterministic way.
It simply chooses the sequence of chord progressions fitting to the melody with the maximal overall weight.

## Creativity

Since the harmonizer simply applies the style definition to a melody, it cannot be called creative.
Instead the creative part is realized by developing new harmonic styles out of existing styles in a (possibly) creative way.
This is inspired by the development of new music styles from existing ones in the history of music.

The goal is to explore the possibilities of developing new ideas in a creative way, e.g., using concept blending.
The "idea space" is, of course, limited to what can be expressed in harmonic styles in this case.
"Creativities" are then implemented as functions mapping existing styles to new ones.

An example of a (not really creative) creativity is the [RandomCreativity](plugins/random_creativity.py).

## Running Stuff

Creativities can be run using [develop.py](develop.py).

    python3 develop.py basic_style.json output_style.json CreativityClass

`CreativityClass` stands for the actual class the creativity is implemented in, e.g., `RandomCreativity` (cf. the respective files in the plugin folder).

TODO add more here:

- Vizualizer
- Harmonizer
