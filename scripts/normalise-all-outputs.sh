#!/bin/bash

python3 score-normalization/score-norm.py --xml lattice-morph.xml
python3 score-normalization/score-norm.py --xml lattice-word-sys2.xml
python3 score-normalization/score-norm.py --xml lattice-word.xml
python3 score-normalization/score-norm.py --xml onebest-morph.xml
python3 score-normalization/score-norm.py --xml onebest-word-to-morph.xml
python3 score-normalization/score-norm.py --xml onebest-word.xml
python3 score-normalization/score-norm.py --xml reference.xml
