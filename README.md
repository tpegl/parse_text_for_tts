# Simple Text Parser Test

A little test to try and parse some text for use in TTS.

I realise that I likely only needed to use one approach and that Spacy or nltk would have achieved what was asked, however, this was a fun little thing to do and I wanted to see how it could be done manually.

## How to use
- Install [uv](https://docs.astral.sh/uv/)
- Get a venv going `uv venv`
- Activate your venv: `source .venv/bin/activate`
- There's no dependencies to install dependencies but it's always good practice to do: `uv sync`
- Then call `uv run main.py -t <some text you want to parse>`