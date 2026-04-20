import unittest

from llm.model import MarkovTextGenerator
from llm.tokenizer import END_TOKEN, START_TOKEN


class ModelTests(unittest.TestCase):
    def test_train_counts_include_all_transitions(self):
        model = MarkovTextGenerator(order=2)
        tokens = [START_TOKEN, START_TOKEN, "alpha", "beta", END_TOKEN]
        model.train(tokens)

        self.assertEqual(model.transition_counts[2][(START_TOKEN, START_TOKEN)]["alpha"], 1)
        self.assertEqual(model.transition_counts[2][(START_TOKEN, "alpha")]["beta"], 1)
        self.assertEqual(model.transition_counts[2][("alpha", "beta")][END_TOKEN], 1)

    def test_model_backs_off_to_lower_order_context(self):
        model = MarkovTextGenerator(order=2)
        model.train([START_TOKEN, START_TOKEN, "hello", "world", END_TOKEN])

        used_order, distribution = model.next_token_distribution(["missing", "hello"])
        self.assertEqual(used_order, 1)
        self.assertEqual(distribution["world"], 1)

    def test_generation_uses_prompt_context(self):
        model = MarkovTextGenerator(order=1, rng_seed=7)
        model.train([START_TOKEN, "hello", "world", END_TOKEN])

        result = model.generate(prompt_tokens=["hello"], max_tokens=3)
        self.assertEqual(result.generated_tokens[:2], ["hello", "world"])


if __name__ == "__main__":
    unittest.main()
