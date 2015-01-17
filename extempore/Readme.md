# Extempore scripts

This directory contains [Extempore](https://github.com/digego/extempore)
scripts that allow you to "listen" to a style.

## Setup

1. [Compile Extempore](http://benswift.me/extempore-docs/index.html#sec-2).
2. (optional) [Compile the standard library](http://benswift.me/2013-12-16-building-the-extempore-standard-library.html).
   Don't compile `core/instruments.xtm` and `external/instruments_ext.xtm` as this is currently broken.
   For this script you only need `core/std.xtm`, `core/math.xtm`, `core/audio_dsp.xtm`, and `external/sndfile.xtm`.
3. Download the sample collections used by the instruments.
   The files in `instruments/` define the instruments and contain links to the sample collections.
   Adapt the paths in the instrument files to point to the sample collections.
4. Copy `instruments/` and `json.xtm` to the `libs/` folder of your extempore directory.
5. Edit `jazztrio.xtm` so that `load-style` loads the style you want (at the bottom of the file).
6. Start and connect to Extempore (e.g. [using Emacs](http://benswift.me/2012-10-10-extempore-emacs-cheat-sheet.html) and load `jazztrio.xtm` completely (`C-c C-c` in Emacs).

The Jazz trio should now start playing. To controll some things, use the function calls at the bottom of `jazztrio.xtm` (`C-c C-c` in Emacs, again).

## What's going on?

The music that you hear is played by three sampled instruments: a drumset, a double bass, and a piano.
The drumset just plays a fixed typical swing rhythm, the bass and piano play corresponding to harmonics.

The harmonics are determined by randomly choosing a chord progression from the loaded style (wrt. the progressions' weights).
Each chord of a chose progression is then played for one bar.
If possible, the next progression starts with the same chord that the previous one ended on.
In this case, the overlapping chord is only played once.

The bass tries to mimic a walking bass by playing either quarter notes or occasionally swing eights.
The next note that is played is determined by choosing a note from the two octaves around the last note that belongs to the current chord.
The available notes are preferred according to their distance from the last note (the closer the better) but the last note is not repeated.

The piano chooses a random chord instantiation (i.e., real pitches) according to the given chord (given as pitch classes).
This chord is then played in a randomly generated rhythm resembling typical swing piano rhythms.
For each swing eighth beat it is determined randomly whether a note should start on that beat (p=0.2 by default).
Each of these notes can last 1/3 quarter (i.e., a shorter swing eighth) or until the next note, which is also chosen randomly (p=1.0 by default), except of the last note in each bar (which is always short) and a note on a beat directly followed by an off-beat (which is always long, i.e. a long swing eighth).
