"""Evaluation helpers for the Markov text generator.

Generation quality is easy to judge informally by reading samples, but that is
not enough if you want to compare changes honestly. This module provides a
small quantitative evaluation pass over held-out tokens.
"""

from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass
from typing import Sequence

from .model import MarkovTextGenerator


@dataclass(frozen=True)
class EvaluationResult:
    """Compact evaluation report.

    `context_usage` records how often each backoff order was used. That makes it
    easier to see whether a model is really benefiting from its requested order
    or spending most of its time falling back to shorter contexts.
    """

    token_count: int
    average_log_probability: float
    perplexity: float
    context_usage: Counter[int]


def evaluate_model(model: MarkovTextGenerator, tokens: Sequence[str]) -> EvaluationResult:
    """Evaluate a model on a held-out token sequence.

    The model is unsmoothed, so completely unseen transitions yield infinite
    perplexity. That is expected and still useful feedback for a simple Markov
    generator.
    """

    if len(tokens) < 2:
        raise ValueError("Need at least two tokens to evaluate the model.")

    # We accumulate log-probability one transition at a time for the same
    # numerical-stability reason described in the model module.
    total_log_probability = 0.0
    context_usage: Counter[int] = Counter()
    steps = 0

    for index in range(len(tokens) - 1):
        # Build the widest available context ending at the current token.
        context = tokens[max(0, index - model.order + 1) : index + 1]
        used_order, distribution = model.next_token_distribution(context)
        context_usage[used_order] += 1

        next_token = tokens[index + 1]
        count = distribution.get(next_token, 0)
        if count == 0:
            # With no smoothing, an unseen transition has zero probability.
            # That translates to infinite perplexity, which is expected here.
            return EvaluationResult(
                token_count=len(tokens),
                average_log_probability=float("-inf"),
                perplexity=float("inf"),
                context_usage=context_usage,
            )

        total = sum(distribution.values())
        total_log_probability += math.log(count / total)
        steps += 1

    # Average log-probability per step is converted into perplexity, the common
    # language-model metric that can be read as "effective branching factor."
    average_log_probability = total_log_probability / max(steps, 1)
    perplexity = math.exp(-average_log_probability)
    return EvaluationResult(
        token_count=len(tokens),
        average_log_probability=average_log_probability,
        perplexity=perplexity,
        context_usage=context_usage,
    )
