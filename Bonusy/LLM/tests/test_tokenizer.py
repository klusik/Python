import unittest

from llm.tokenizer import END_TOKEN, START_TOKEN, add_sentence_markers, detokenize, tokenize


class TokenizerTests(unittest.TestCase):
    def test_tokenize_preserves_punctuation_as_tokens(self):
        tokens = tokenize("Hello, world!")
        self.assertEqual(tokens, ["Hello", ",", "world", "!"])

    def test_add_sentence_markers_wraps_sentence_boundaries(self):
        marked = add_sentence_markers(["Hello", "."], order=2)
        self.assertEqual(
            marked,
            [START_TOKEN, START_TOKEN, "Hello", ".", END_TOKEN, START_TOKEN, START_TOKEN],
        )

    def test_detokenize_reconstructs_basic_spacing(self):
        text = detokenize(["Hello", ",", "world", "!"])
        self.assertEqual(text, "Hello, world!")


if __name__ == "__main__":
    unittest.main()
