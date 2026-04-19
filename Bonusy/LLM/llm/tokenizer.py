"""Tokenization helpers for the Markov text generator.

This module is intentionally simple and heavily documented because tokenization
is one of the most important design choices in the whole project. A Markov
model can only learn from the token stream it sees, so decisions made here
directly shape generation quality, vocabulary size, and evaluation behavior.

The tokenizer keeps punctuation as separate tokens instead of discarding it.
That lets the model learn basic sentence rhythm such as commas, periods, and
question marks rather than seeing only a stream of words with structure erased.
"""

from __future__ import annotations

import re
from typing import Iterable, List

# The regular expression is deliberately conservative:
# - words such as "hello" become one token
# - contractions such as "don't" stay together
# - punctuation such as "," or "!" becomes its own token
#
# This is not a linguistically complete tokenizer. It is a practical tokenizer
# that keeps the model readable and easy to reason about.
TOKEN_PATTERN = re.compile(r"\w+(?:'\w+)?|[^\w\s]", re.UNICODE)

# These punctuation marks are treated as sentence boundaries. When one of them
# appears, we inject an explicit sentence end marker and a fresh sentence start
# context for the next sentence.
SENTENCE_ENDINGS = {".", "!", "?"}

# Special markers used only inside the model. They are not printed back to the
# user during generation.
START_TOKEN = "<s>"
END_TOKEN = "</s>"


def normalize_text(text: str, preserve_case: bool = True) -> str:
    """Normalize whitespace while optionally preserving the original casing.

    We collapse repeated whitespace because text files often contain line breaks,
    tabs, or spacing artifacts that are not meaningful for a simple word-level
    generator. We do not strip punctuation here because punctuation carries
    strong stylistic information that the model should learn.
    """

    normalized = re.sub(r"\s+", " ", text).strip()
    return normalized if preserve_case else normalized.lower()


def tokenize(text: str, preserve_case: bool = True) -> List[str]:
    """Split text into word and punctuation tokens.

    The regex is intentionally simple and transparent. It is not meant to be a
    full linguistic tokenizer, only a stable token stream for a Markov model.
    """

    # Normalization is separated from the regex so each step is individually
    # understandable and testable.
    normalized = normalize_text(text, preserve_case=preserve_case)
    if not normalized:
        return []
    return TOKEN_PATTERN.findall(normalized)


def add_sentence_markers(tokens: Iterable[str], order: int) -> List[str]:
    """Wrap sentence boundaries with explicit start and end markers.

    Repeating the start token `order` times makes it easy to train the model on
    the first word positions without special casing short contexts.
    """

    # Repeating the start token `order` times means a model of order 3 begins
    # each sentence with a context like ("<s>", "<s>", "<s>"). That avoids a
    # lot of awkward special cases around short sentence prefixes.
    marked_tokens: List[str] = [START_TOKEN] * order
    for token in tokens:
        marked_tokens.append(token)
        if token in SENTENCE_ENDINGS:
            # Close the current sentence and prime the next one immediately.
            marked_tokens.append(END_TOKEN)
            marked_tokens.extend([START_TOKEN] * order)

    if not marked_tokens:
        return [START_TOKEN] * order + [END_TOKEN]

    # If the token stream already ended with sentence punctuation we will be
    # sitting on fresh start markers for the next sentence. In that case the
    # previous `END_TOKEN` already closed the document cleanly.
    trailing_starts = marked_tokens[-order:] if order else []
    already_closed = order > 0 and trailing_starts == [START_TOKEN] * order

    # Ensure the final sentence terminates cleanly when the source text does
    # not end in explicit sentence punctuation.
    if marked_tokens[-1] != END_TOKEN and not already_closed:
        marked_tokens.append(END_TOKEN)

    return marked_tokens


def detokenize(tokens: Iterable[str]) -> str:
    """Turn generated tokens back into readable text.

    The spacing rules are intentionally conservative: punctuation attaches to
    the previous token while opening brackets and quotes keep the following word
    tight enough to avoid obviously broken output.
    """

    # The two spacing rule sets are small on purpose. A compact, predictable
    # detokenizer is better for this project than a large opaque formatting
    # system that is hard to debug.
    pieces: List[str] = []
    no_space_before = {".", ",", ";", ":", "!", "?", ")", "]", "}", "%"}
    no_space_after = {"(", "[", "{", '"', "'"}

    for token in tokens:
        if token in {START_TOKEN, END_TOKEN}:
            # Special markers are model-only scaffolding and should never appear
            # in the final human-readable text.
            continue

        if not pieces:
            pieces.append(token)
            continue

        if token in no_space_before or pieces[-1] in no_space_after:
            pieces[-1] = pieces[-1] + token
        else:
            pieces.append(token)

    return " ".join(pieces)
