#!/bin/sh

python3 develop.py dummy_style.json example_out.json SimpleCreativity
python3 harmonization.py dummy_style.json example_harm.json "[4,4,5,7,7,5,4,2,0,0,2,4,4,2,2,4,4,5,7,7,5,4,2,0,0,2,4,2,0,0]"
