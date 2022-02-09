# Swahili Keyword Spotting

The aim of this project is to write a simple Keyword Spotting (KWS) system for
Swahili. This involves detection of a particular word, or phrase, in a stream of
Swahili audio.

The KWS system will be based on the 1-best output with posterior
scores (derived from confusion networks) from a speech recognition system. We
will also investigate score-normalisation and system combination.

## Prerequisites

* Python version >= 3.9
* Add appropriate folders to the `PYTHONPATH` environment variable to allow for relative imports by running: `source scripts/set-pythonpath.sh`
## Usage

### Running KWS on a single CTM file

To run KWS on a CTM file, place the CTM file (e.g. `example.ctm`) in the `lib/ctms` folder and the appropriate queries XML file in the `lib/queries` folder, then run:
```
python3.9 src/kws/main.py --ctm example.ctm --queries queries.xml --output example-output.xml
```

This will output the XML hits output file to `outputs/example-output.xml`

### Running KWS on a chosen set of predefined CTM files

Run:
```
scripts/run-kws-on-all-ctms.sh
```

Look closer at the script to see which systems this entails. This will output the XML hits output files to the `outputs` folder.

### Scoring the KWS output and getting the MTWV

```
scripts/score.sh output/example.xml scoring
scripts/termselect.sh lib/queries/ivoov.map output/example.xml scoring [all|iv|oov]
```

### Morphological Decomposition

Decomposing `queries-word.xml` into `queries-morph.xml`
```
python3.9 src/morph-decomposition/queries_to_morphs.py
```

Decomposing `onebest-word.ctm` into `onebest-word-to-morphs.ctm`
```
python3.9 src/morph-decomposition/ctm_to_morphs.py
```

### Running the unit tests:
```
python3.9 -m unittest discover -v -s ./src -p "*test*.py"
```
