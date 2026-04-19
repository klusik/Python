"""Corpus loading and preparation utilities.

This module is responsible for turning local `.txt` files into a clean token
stream that the Markov model can train on. Keeping this logic separate from the
model matters because corpus concerns and model concerns evolve differently.

For example:
- file discovery is a CLI/data-loading concern
- text reading and decoding are I/O concerns
- train/validation splitting is an evaluation concern
- token transition counting is the model's job, not the corpus module's job
"""

from __future__ import annotations

from dataclasses import dataclass
from glob import glob
from pathlib import Path
from typing import Iterable, List, Sequence

from .tokenizer import add_sentence_markers, tokenize


@dataclass(frozen=True)
class CorpusDocument:
    """Single training document with source metadata.

    Keeping the file path alongside the text makes it easy to report which
    files were used to build a model and later save that metadata.
    """

    path: Path
    text: str


@dataclass(frozen=True)
class CorpusSplit:
    """Train/validation token split.

    This stays intentionally small. We only need the token sequences themselves
    for now, not a more elaborate dataset object.
    """

    train_tokens: List[str]
    validation_tokens: List[str]


def resolve_files(patterns: Sequence[str]) -> List[Path]:
    """Resolve one or more file patterns into sorted concrete files.

    Sorting and de-duplicating the result keeps training deterministic. If the
    same glob is passed twice, or two patterns match the same file, the model
    should still see each file exactly once.
    """

    resolved: List[Path] = []
    for pattern in patterns:
        # `glob` expands wildcards like `*.txt` into actual paths.
        matches = sorted(Path(match) for match in glob(pattern))
        resolved.extend(path for path in matches if path.is_file())

    unique_paths = sorted(dict.fromkeys(resolved))
    if not unique_paths:
        raise FileNotFoundError(f"No files matched the provided patterns: {patterns}")
    return unique_paths


def load_documents(paths: Iterable[Path], encoding: str = "utf-8") -> List[CorpusDocument]:
    """Read corpus files into memory.

    The current corpus fits comfortably in memory and this keeps training logic
    simpler and less error-prone than chunking with broken context boundaries.
    """

    documents: List[CorpusDocument] = []
    for path in paths:
        # Reading each full file avoids the context-loss bug from the original
        # chunked trainer, where sentence/token transitions were broken at chunk
        # boundaries.
        text = path.read_text(encoding=encoding)
        documents.append(CorpusDocument(path=path, text=text))
    return documents


def documents_to_tokens(
    documents: Sequence[CorpusDocument],
    order: int,
    preserve_case: bool = True,
) -> List[str]:
    """Tokenize a set of documents into one continuous training stream.

    Each document is tokenized separately and receives its own sentence markers.
    That prevents the end of one source file from blending directly into the
    beginning of the next as if they were one literal sentence.
    """

    all_tokens: List[str] = []
    for document in documents:
        tokens = tokenize(document.text, preserve_case=preserve_case)
        all_tokens.extend(add_sentence_markers(tokens, order=order))
    return all_tokens


def split_tokens(tokens: Sequence[str], validation_ratio: float = 0.1) -> CorpusSplit:
    """Split tokens into train and validation segments.

    A contiguous split is sufficient here because this is a small educational
    project and we want deterministic behavior without adding shuffle state.
    """

    if not 0.0 <= validation_ratio < 1.0:
        raise ValueError("validation_ratio must be between 0.0 and 1.0.")

    if not tokens:
        return CorpusSplit(train_tokens=[], validation_tokens=[])

    # A deterministic contiguous split is enough for this project and makes it
    # easier to reproduce experiments exactly.
    split_index = max(1, int(len(tokens) * (1.0 - validation_ratio)))
    split_index = min(split_index, len(tokens))
    return CorpusSplit(
        train_tokens=list(tokens[:split_index]),
        validation_tokens=list(tokens[split_index:]),
    )
