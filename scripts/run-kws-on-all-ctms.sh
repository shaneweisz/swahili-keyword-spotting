#!/bin/bash

# Reference
python3 src/kws/main.py --ctm reference.ctm --queries queries-word.xml --output reference.xml

# One-best word ASR output
python3 src/kws/main.py --ctm onebest-word.ctm --queries queries-word.xml --output onebest-word.xml

# One-best morph ASR output
python3 src/kws/main.py --ctm onebest-morph.ctm --queries queries-morph.xml --output onebest-morph.xml

# One-best word ASR output decomposed into morphs
python3 src/kws/main.py --ctm onebest-word-to-morph.ctm --queries queries-morph.xml --output onebest-word-to-morph.xml

# One-best word ASR output with grapheme confusions for oov words
python3 src/kws/main.py --ctm onebest-word.ctm --queries queries-word.xml --output onebest-word-plus-grapheme-confusions.xml --use_oov_proxies True
