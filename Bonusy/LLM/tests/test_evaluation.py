import math
import unittest

from llm.evaluation import evaluate_model
from llm.model import MarkovTextGenerator
from llm.tokenizer import END_TOKEN, START_TOKEN


class EvaluationTests(unittest.TestCase):
    def test_evaluation_returns_finite_perplexity_for_seen_sequence(self):
        model = MarkovTextGenerator(order=1)
        tokens = [START_TOKEN, "hello", "world", END_TOKEN]
        model.train(tokens)

        result = evaluate_model(model, tokens)

        self.assertTrue(math.isfinite(result.perplexity))
        self.assertGreaterEqual(result.context_usage[1], 1)


if __name__ == "__main__":
    unittest.main()
