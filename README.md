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
ln -s /usr/local/teach/MLSALT5/Practical/{lib,scoring,scripts} ~/MLMI14
```

Create and activate python 3.9 virtual environment (3.9.7):
```
python3.9 -m venv ~/MLMI14/.venv
source ~/MLMI14/.venv/bin/activate
```

## Usage

To run the unit tests, run:
```
python3.9 -m unittest discover -v -s ./src -p "*test*.py"
```
