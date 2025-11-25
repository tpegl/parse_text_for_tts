import argparse
from pydoc import text
from typing import Any, Callable

import re
"""
Instructions:

1. Chunking:
Divide the text into logical, meaningful pieces that do not exceed 200 characters each. Ensure each chunk maintains natural phrasing suitable for speech synthesis.

2. Redundancy Removal:
As well as the text chunking, remove any characters or elements that are redundant or unnecessary for speech generation.

3. Explain your reasoning:
    Alongside your output, explain:
    - How you chose the chunk boundaries (e.g., sentence ends, phrase cadence)
    - What specific characters or elements you removed and why
    - How your changes improve the result for TTS

4. What would you have to think about to make this work for other languages than english?```
"""

# --------------------------------------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------------------------------------
def replace_potentially_helpful_symbols(text: str):
    """
    Replace some symbols that CAN be useful for describing text
    """
    replacements = {
        "&": " and ",
        "%": " percent ",
        "+": " plus ",
        "=": " equals ",
        "@": " at ",
        "#": " number ",
        "$": " dollars ",
        "£": " pounds ",
        "€": " euros "
    }

    for symbol, replacement in replacements.items():
        text = text.replace(symbol, replacement)

    return text

# Remove fillers and vocalisations as they aren't needed for TTS unless
# you want a more "natural" sounding speech
fillers_and_vocalisations = [
    'um', 'uh', 'hm', 'ah'
]

def remove_unnecessary_words_or_characters(text: str):
    for filler in fillers_and_vocalisations:
        text = text.replace(filler, "")

    return text

def preprocess_text(text: str):
    while '  ' in text:
        text = text.replace('  ', ' ')
    text = text.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ')

    text = replace_potentially_helpful_symbols(text)
    text = remove_unnecessary_words_or_characters(text)

    # Regex pattern for matching many non-speech characters and remove them.
    # Even if they might be used in text like hashtags or usernames from
    # social platforms they shouldn't be vocalised in TTS and don't impart
    # any extra meaning for form or structure i.e. #, @.
    symbols_pattern = re.compile(r'[^a-zA-Z0-9.!?,;:\'"£$%&—\-\s]')

    # Removes non-unicode strings.
    non_unicode_pattern = re.compile(r"[^\x00-\x7F]+")

    text = re.sub(non_unicode_pattern, "", text)
    return re.sub(symbols_pattern, '', text)


# --------------------------------------------------------------------------------
"""
I know it's possible to just use something like Spacy or nltk to accomplish this but
the task intrigued me enough that I ended up spending more time looking up NLP 
techniques and wanted to try doing it manually.
"""

conjunctions_and_connectors = [
    ' and ', ' or ', ' but ', ' so ', ' yet ', ' nor ',
    ' because ', ' however ', ' therefore ', ' moreover ',
    ' furthermore ', ' nevertheless '
]

prepositions = [
    ' after ', ' before ', ' during ', ' until ',
    ' with ', ' without ', ' under ', ' over ',
    ' through ', ' between ', ' among '
]

relative_pronouns = [
    ' that ', ' which ', ' who ', ' whom ', ' whose ',
    ' when ', ' where ', ' why ', ' how '
]

def chunk(text: str, chunk_size: int = 200) -> list[str]:
    text = text.strip()

    # Remove whitespace and control characters
    while '  ' in text:
        text = text.replace('  ', ' ')
    text = text.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ')

    chunks: list[str] = []

    while text:
        if len(text) <= chunk_size:
            chunks.append(text.strip())
            break

        chunk = text[:chunk_size]
        split_point = None


        # Let's create a series of functions that we'll use to look for various potential stopping points 
        # for chunks within a given blob of text. Following from top priority to lowest priority:
        #   - sentences
        #   - obvious separators
        #   - conjunctions or connectors (usually convery a new clause)
        #   - prepositions (often begin a new, separate chunk of text related to the previous)
        #   - relative pronouns (similar to prepositions, often a new chunk related to the previos)
        #   - finally, spaces. If nothing else works, break it on the nearest space character
        approaches: list[tuple[Callable[..., Any], int, float]] = [
            (lambda txt: max(txt.rfind('. '), txt.rfind('! '), txt.rfind('? ')), 2, 0.4),
            (lambda txt: max(txt.rfind(', '), txt.rfind('; '), txt.rfind(': ')), 2, 0.4),
            (lambda txt: max([txt.rfind(w) for w in conjunctions_and_connectors]), 1, 0.3),
            (lambda txt: max([txt.rfind(w) for w in prepositions]), 0, 0.3),
            (lambda txt: max([txt.rfind(w) for w in relative_pronouns]), 0, 0.3),
            (lambda txt: txt.rfind(' '), 1, 0.3),
        ]

        for approach_func, offset, min_ratio in approaches:
            pos = approach_func(chunk)
            if pos > chunk_size * min_ratio:
                # Calculate actual split point
                if offset > 0:
                    split_point = pos + offset
                else:
                    # For word matches, find end of the word
                    end_of_word = chunk.find(' ', pos + 1)
                    split_point = end_of_word + 1 if end_of_word > 0 else pos + 1
                break

        # Fallback to hard split if nothing worked
        if split_point is None or split_point <= 0:
            split_point = chunk_size

        chunks.append(text[:split_point].strip())
        text = text[split_point:].strip()

    return chunks


def manual(text: str):
    chunks = chunk(text)
    print([chunk for chunk in chunks])

"""
4. In order for this to work with any other language we'd need to either use specific corpuses 
with that language in the case of Spacy, or for the manual process, have a greater understanding 
of the language and how sentences and phrases are structured in order to split it on specific 
terms as well as the flow of the text (i.e. Arabic and Japanese are entirely different structures
as well as different ways of constructing phrases which themselves vary by their context)
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description ='Process some text for TTS.')
    _ = parser.add_argument(
        '-t',
        type=str,
        help='text to parse and clean',
        required=False
    )

    args = parser.parse_args()

    text = ''

    if not args.t:
        with open('./text1.txt') as f1, open('./text2.txt') as f2:
            text = preprocess_text(f1.read())
            manual(text)

            text = preprocess_text(f2.read())

            print("\n\n")
            manual(text)
    else:
        text = preprocess_text(args.t)
        manual(text)
