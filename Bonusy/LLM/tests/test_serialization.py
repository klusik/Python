from pathlib import Path
import tempfile
import unittest

from llm.model import MarkovTextGenerator
from llm.serialization import load_model, save_model
from llm.tokenizer import END_TOKEN, START_TOKEN


class SerializationTests(unittest.TestCase):
    def test_model_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            model = MarkovTextGenerator(order=2)
            model.train([START_TOKEN, START_TOKEN, "alpha", END_TOKEN])

            model_path = tmp_path / "model.kls"
            save_model(model_path, model, preserve_case=True, training_files=["sample.txt"])

            restored, metadata = load_model(model_path)

            self.assertEqual(restored.order, model.order)
            self.assertEqual(restored.transition_counts[2][(START_TOKEN, START_TOKEN)]["alpha"], 1)
            self.assertEqual(metadata["training_files"], ["sample.txt"])


if __name__ == "__main__":
    unittest.main()
