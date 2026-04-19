"""Command-line interface for the Markov text generator.

The CLI is intentionally kept separate from the model itself. That way the core
Markov logic stays reusable from tests or future scripts, while this module
focuses only on translating command-line arguments into project actions.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from .corpus import documents_to_tokens, load_documents, resolve_files, split_tokens
from .evaluation import evaluate_model
from .model import MarkovTextGenerator
from .serialization import load_model, save_model
from .tokenizer import tokenize


def build_parser() -> argparse.ArgumentParser:
    """Build the top-level CLI parser.

    The CLI exposes four main workflows:
    - train a model from local text files
    - generate text from a saved model
    - evaluate a saved model on text files
    - inspect saved model statistics
    """

    parser = argparse.ArgumentParser(
        description="Word-level Markov text generator trained on local txt files."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    train_parser = subparsers.add_parser("train", help="Train a model from txt files.")
    train_parser.add_argument("patterns", nargs="+", help="File paths or glob patterns.")
    train_parser.add_argument("--order", type=int, default=2, help="Markov order.")
    train_parser.add_argument(
        "--validation-ratio",
        type=float,
        default=0.1,
        help="Fraction of tokens reserved for evaluation.",
    )
    train_parser.add_argument(
        "--preserve-case",
        action="store_true",
        help="Keep original casing instead of lowercasing everything.",
    )
    train_parser.add_argument(
        "--save",
        type=Path,
        default=Path("save.kls"),
        help="Output model file path.",
    )

    generate_parser = subparsers.add_parser("generate", help="Generate text from a saved model.")
    generate_parser.add_argument("--model", type=Path, default=Path("save.kls"), help="Saved model path.")
    generate_parser.add_argument("--prompt", default="", help="Optional prompt text.")
    generate_parser.add_argument("--max-tokens", type=int, default=50, help="Maximum generated tokens.")
    generate_parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducible output.")

    evaluate_parser = subparsers.add_parser("evaluate", help="Evaluate a saved model on txt files.")
    evaluate_parser.add_argument("patterns", nargs="+", help="File paths or glob patterns.")
    evaluate_parser.add_argument("--model", type=Path, default=Path("save.kls"), help="Saved model path.")

    stats_parser = subparsers.add_parser("stats", help="Print saved model statistics.")
    stats_parser.add_argument("--model", type=Path, default=Path("save.kls"), help="Saved model path.")

    return parser


def _train_command(args: argparse.Namespace) -> int:
    """Handle model training, saving, and optional validation reporting."""

    paths = resolve_files(args.patterns)
    documents = load_documents(paths)
    tokens = documents_to_tokens(documents, order=args.order, preserve_case=args.preserve_case)
    token_split = split_tokens(tokens, validation_ratio=args.validation_ratio)

    model = MarkovTextGenerator(order=args.order)
    model.train(token_split.train_tokens)
    save_model(
        path=args.save,
        model=model,
        preserve_case=args.preserve_case,
        training_files=[str(path) for path in paths],
    )

    print(f"Saved model to {args.save}")
    print(json.dumps(model.stats(), indent=2, sort_keys=True))

    if len(token_split.validation_tokens) >= 2:
        evaluation_tokens = token_split.validation_tokens
        if token_split.train_tokens:
            # Prepend a small amount of trailing training context so evaluation
            # does not begin with an artificially contextless boundary.
            evaluation_tokens = token_split.train_tokens[-model.order :] + evaluation_tokens
        evaluation = evaluate_model(model, evaluation_tokens)
        print(
            json.dumps(
                {
                    "validation_token_count": evaluation.token_count,
                    "validation_perplexity": evaluation.perplexity,
                    "context_usage": dict(sorted(evaluation.context_usage.items())),
                },
                indent=2,
                sort_keys=True,
            )
        )
    return 0


def _generate_command(args: argparse.Namespace) -> int:
    """Handle text generation from a saved model."""

    model, metadata = load_model(args.model)
    model.random.seed(args.seed)
    preserve_case = bool(metadata.get("preserve_case", True))

    # The prompt is tokenized with the same case policy that was used during
    # training so the prompt tokens line up with the model vocabulary.
    prompt_tokens = tokenize(args.prompt, preserve_case=preserve_case)
    result = model.generate(prompt_tokens=prompt_tokens, max_tokens=args.max_tokens)
    print(result.text)
    return 0


def _evaluate_command(args: argparse.Namespace) -> int:
    """Handle evaluation of a saved model on one or more text files."""

    model, metadata = load_model(args.model)
    preserve_case = bool(metadata.get("preserve_case", True))
    paths = resolve_files(args.patterns)
    documents = load_documents(paths)
    tokens = documents_to_tokens(documents, order=model.order, preserve_case=preserve_case)
    evaluation = evaluate_model(model, tokens)
    print(
        json.dumps(
            {
                "token_count": evaluation.token_count,
                "average_log_probability": evaluation.average_log_probability,
                "perplexity": evaluation.perplexity,
                "context_usage": dict(sorted(evaluation.context_usage.items())),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


def _stats_command(args: argparse.Namespace) -> int:
    """Print a compact summary of saved model statistics and metadata."""

    model, metadata = load_model(args.model)
    payload = {
        "model_stats": model.stats(),
        "metadata": dict(metadata),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point.

    A small manual dispatch is clear enough here and avoids over-engineering the
    command routing for a project with only a few subcommands.
    """

    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "train":
        return _train_command(args)
    if args.command == "generate":
        return _generate_command(args)
    if args.command == "evaluate":
        return _evaluate_command(args)
    if args.command == "stats":
        return _stats_command(args)

    parser.error(f"Unknown command: {args.command}")
    return 2
