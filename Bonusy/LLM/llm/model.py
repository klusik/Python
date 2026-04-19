"""Word-level Markov text generator implementation."""

from __future__ import annotations

import math
import random
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import DefaultDict, Dict, List, Mapping, Sequence, Tuple

from .tokenizer import END_TOKEN, START_TOKEN, detokenize

Context = Tuple[str, ...]


@dataclass(frozen=True)
class GenerationResult:
    """Structured generation output for CLI and tests.

    Returning a rich result object is more useful than returning plain text
    alone because tests can inspect the raw generated tokens while the CLI can
    still print the formatted text field directly.
    """

    prompt_tokens: List[str]
    generated_tokens: List[str]
    text: str


class MarkovTextGenerator:
    """Word-level Markov generator with explicit backoff across model orders.

    The model stores counts for every order from 0 through `order`. Order 0 is
    the unigram distribution and acts as the final fallback when no larger
    context has been observed in training.
    """

    def __init__(self, order: int = 2, rng_seed: int | None = None) -> None:
        """Create a Markov generator of a given order.

        `order=2` means the model tries to predict the next token from the
        previous two tokens, backing off to one token and then to the unigram
        distribution if needed.
        """

        if order < 1:
            raise ValueError("order must be at least 1")

        self.order = order
        self.random = random.Random(rng_seed)
        self.transition_counts: Dict[int, DefaultDict[Context, Counter[str]]] = {
            current_order: defaultdict(Counter) for current_order in range(order + 1)
        }
        self.total_tokens = 0

    def train(self, tokens: Sequence[str]) -> None:
        """Train the model from a token sequence.

        Each training step updates every backoff order. This costs more memory
        than keeping only the top order, but it makes generation and evaluation
        straightforward and predictable.
        """

        if len(tokens) < 2:
            return

        self.total_tokens += len(tokens)
        for index in range(len(tokens) - 1):
            next_token = tokens[index + 1]
            for current_order in range(self.order + 1):
                if current_order == 0:
                    # Order 0 ignores context entirely. It is the global token
                    # distribution and acts as the final fallback.
                    context: Context = ()
                else:
                    # For higher orders, take the last `current_order` tokens
                    # ending at the current position.
                    start = index - current_order + 1
                    if start < 0:
                        continue
                    context = tuple(tokens[start : index + 1])
                    if len(context) != current_order:
                        continue
                self.transition_counts[current_order][context][next_token] += 1

    def next_token_distribution(self, context_tokens: Sequence[str]) -> Tuple[int, Mapping[str, int]]:
        """Return the best available next-token distribution for a context.

        The returned integer is the order that actually matched. This is useful
        in evaluation because it shows how often the model used full context
        versus how often it had to back off.
        """

        usable_tokens = list(context_tokens)[-self.order :]
        for current_order in range(min(self.order, len(usable_tokens)), -1, -1):
            # Try the most specific context first, then progressively shorter
            # contexts until something has been seen in training.
            context = tuple(usable_tokens[-current_order:]) if current_order else ()
            distribution = self.transition_counts[current_order].get(context)
            if distribution:
                return current_order, distribution
        raise ValueError("Model has not been trained on any usable token transitions.")

    def sample_next_token(self, context_tokens: Sequence[str]) -> Tuple[str, int]:
        """Sample a token using the highest-order available distribution.

        Weighted sampling means common continuations appear more often, but rare
        continuations are still possible. That makes output less repetitive than
        always taking the single most frequent next token.
        """

        used_order, distribution = self.next_token_distribution(context_tokens)
        choices = list(distribution.keys())
        weights = list(distribution.values())
        return self.random.choices(choices, weights=weights, k=1)[0], used_order

    def generate(
        self,
        prompt_tokens: Sequence[str] | None = None,
        max_tokens: int = 50,
        stop_at_end: bool = True,
    ) -> GenerationResult:
        """Generate text from an optional prompt.

        The model uses the prompt as initial context if provided. Otherwise it
        starts from sentence-start markers so generation begins from a plausible
        sentence boundary.
        """

        if max_tokens < 1:
            raise ValueError("max_tokens must be at least 1")

        prompt = list(prompt_tokens or [])
        # The visible output should not contain internal sentence markers, so we
        # filter them out if they somehow arrive in the prompt.
        generated = [token for token in prompt if token not in {START_TOKEN, END_TOKEN}]

        # The state keeps model-only start markers before the prompt so a prompt
        # shorter than `order` still has a full context window.
        state = ([START_TOKEN] * self.order) + prompt

        for _ in range(max_tokens):
            token, _ = self.sample_next_token(state)
            if token == END_TOKEN and stop_at_end:
                # End cleanly at a sentence boundary when requested.
                break
            generated.append(token)
            state.append(token)

        return GenerationResult(
            prompt_tokens=prompt,
            generated_tokens=generated,
            text=detokenize(generated),
        )

    def sequence_log_probability(self, tokens: Sequence[str]) -> float:
        """Compute the log-probability of a token sequence under the model.

        Log-probabilities are used because multiplying many small probabilities
        quickly underflows in floating-point arithmetic. Summing logs is the
        standard numerically stable alternative.
        """

        if len(tokens) < 2:
            raise ValueError("Need at least two tokens to score a sequence.")

        log_probability = 0.0
        for index in range(len(tokens) - 1):
            context = tokens[max(0, index - self.order + 1) : index + 1]
            used_order, distribution = self.next_token_distribution(context)
            next_token = tokens[index + 1]
            count = distribution.get(next_token, 0)
            if count == 0:
                # A model without smoothing assigns zero probability to unseen
                # transitions. We represent that as negative infinity.
                return float("-inf")
            total = sum(distribution.values())
            log_probability += math.log(count / total)
        return log_probability

    def stats(self) -> Dict[str, int]:
        """Return a compact set of model statistics.

        These are intentionally high-signal stats that help you inspect whether
        the model shape is sensible without dumping huge internal structures.
        """

        unigram_distribution = self.transition_counts[0].get((), Counter())
        return {
            "order": self.order,
            "total_tokens": self.total_tokens,
            "vocabulary_size": len(unigram_distribution),
            "state_count": sum(len(level) for level in self.transition_counts.values()),
        }

    def to_dict(self) -> Dict[str, object]:
        """Serialize the model to plain Python containers.

        Converting nested `defaultdict` and `Counter` objects into normal dicts
        makes the saved payload more portable and less tied to Python internals.
        """

        transition_counts: Dict[int, Dict[Context, Dict[str, int]]] = {}
        for order, contexts in self.transition_counts.items():
            transition_counts[order] = {
                context: dict(counter)
                for context, counter in contexts.items()
            }
        return {
            "order": self.order,
            "total_tokens": self.total_tokens,
            "transition_counts": transition_counts,
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, object]) -> "MarkovTextGenerator":
        """Rebuild a model from serialized data.

        This reverses `to_dict()` and restores the nested counter structure that
        the generator expects at runtime.
        """

        order = int(payload["order"])
        model = cls(order=order)
        model.total_tokens = int(payload["total_tokens"])
        transition_counts = payload["transition_counts"]
        if not isinstance(transition_counts, Mapping):
            raise TypeError("transition_counts must be a mapping")

        rebuilt: Dict[int, DefaultDict[Context, Counter[str]]] = {
            current_order: defaultdict(Counter) for current_order in range(order + 1)
        }

        for order_key, contexts in transition_counts.items():
            current_order = int(order_key)
            if not isinstance(contexts, Mapping):
                raise TypeError("Serialized contexts must be a mapping")
            for context, counter_mapping in contexts.items():
                if not isinstance(counter_mapping, Mapping):
                    raise TypeError("Serialized counter must be a mapping")
                rebuilt[current_order][tuple(context)] = Counter(
                    {str(token): int(count) for token, count in counter_mapping.items()}
                )

        model.transition_counts = rebuilt
        return model
