# Simple Text Parser Test

A little test to try and parse some text for use in TTS.

I realise that I likely only needed to use Spacy or nltk to have achieved what was asked, however, this was a fun little thing to do and I wanted to see how it could be done manually.

## How to use
- Install [uv](https://docs.astral.sh/uv/)
- Get a venv going `uv venv`
- Activate your venv: `source .venv/bin/activate`
- There's no dependencies to install dependencies but it's always good practice to do: `uv sync`
- Then call `uv run main.py -t <some optional text you want to parse. Will use the local files otherwise>`
