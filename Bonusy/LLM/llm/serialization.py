"""Model persistence helpers.

The model can be trained on large local text files, so re-training every time
would be unnecessarily slow. This module keeps save/load concerns separate from
the training logic and stores enough metadata to understand what produced a
given model file later.
"""

from __future__ import annotations

import pickle
from pathlib import Path
from typing import Any, Dict, Mapping

from .model import MarkovTextGenerator

SAVE_FORMAT_VERSION = 1
# A version number is included from the start so future structural changes can
# reject or migrate old save files explicitly instead of failing ambiguously.


def build_save_payload(
    model: MarkovTextGenerator,
    preserve_case: bool,
    training_files: list[str],
) -> Dict[str, Any]:
    """Build a versioned save payload.

    Pickle is still used for convenience, but only around plain Python
    containers. This keeps the format easier to inspect and migrate later.
    """

    # The payload is intentionally plain and explicit. Even though pickle is
    # used to write it to disk, the content itself is just standard containers.
    return {
        "version": SAVE_FORMAT_VERSION,
        "model_type": "word_markov",
        "model": model.to_dict(),
        "metadata": {
            "preserve_case": preserve_case,
            "training_files": training_files,
        },
    }


def save_model(
    path: str | Path,
    model: MarkovTextGenerator,
    preserve_case: bool,
    training_files: list[str],
) -> None:
    """Save a model and metadata to disk.

    The path is written in one shot from the serialized payload. For this small
    local project that is sufficient and keeps the persistence logic simple.
    """

    payload = build_save_payload(
        model=model,
        preserve_case=preserve_case,
        training_files=training_files,
    )
    serialized_payload = pickle.dumps(payload, protocol=pickle.HIGHEST_PROTOCOL)
    Path(path).write_bytes(serialized_payload)


def load_model(path: str | Path) -> tuple[MarkovTextGenerator, Mapping[str, Any]]:
    """Load a trusted local model file from disk.

    This function intentionally validates the top-level shape before rebuilding
    the model so incompatible or corrupted save files fail early with clear
    errors.
    """

    raw_bytes = Path(path).read_bytes()
    payload = pickle.loads(raw_bytes)
    if payload.get("version") != SAVE_FORMAT_VERSION:
        raise ValueError("Unsupported save file version.")
    if payload.get("model_type") != "word_markov":
        raise ValueError("Unsupported model type.")

    model = MarkovTextGenerator.from_dict(payload["model"])
    metadata = payload.get("metadata", {})
    return model, metadata
