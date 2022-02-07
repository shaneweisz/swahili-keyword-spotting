# MLMI14: Keyword Spotting Coursework

The aim of this practical is to write a simple Keyword Spotting (KWS) system for
Swahili. This involves detection of a particular word, or phrase, in a stream of
Swahili audio.

The system will be based on the 1-best output with posterior
scores (derived from confusion networks) from a speech recognition system. We
will also investigate score-normalisation and system combination.

## Setup

Create sym links to supplied base files:
```
mkdir -p ~/MLMI14
ln -s /usr/local/teach/MLSALT5/Practical/{lib,scripts} ~/MLMI14
```

Create and activate python 3.9 virtual environment (3.9.7):
```
python3.9 -m venv ~/MLMI14/.venv
source ~/MLMI14/.venv/bin/activate
```

## Usage

### Running KWS on a CTM file

To run KWS on a CTM file, place the CTM file (e.g. `example.ctm`) in the `ctms` folder and the
queries XML file in the `queries` folder, then run:
```
python3.9 src/main.py --ctm example.ctm --queries queries.xml --output example-output.xml
```

This will output the XML hits output file to `outputs/example-output.xml`

### Scoring the KWS output

```
scripts/score.sh output/example.xml scoring
```

### Getting the TWV for the KWS output

```
scripts/termselect.sh lib/terms/ivoov.map output/reference.xml scoring [all|iv|oov]
```

### Decomposing `queries.xml` into morphs

```
python3.9 morph-decomposition/decompose_queries.py
```

### Running the unit tests:
```
python3.9 -m unittest discover -v -s ./src -p "*test*.py"
```
