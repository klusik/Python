import random
from collections import defaultdict, Counter
import os
import sys
import glob
import pickle
import gc  # For explicit garbage collection
import re  # For cleaning text


def clean_text(text):
    """
    Cleans the input text by removing unnecessary newlines and spaces.
    :param text: The input text to clean.
    :return: Cleaned text.
    """
    # Replace multiple newlines or spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    # Strip leading/trailing whitespace
    return text.strip()


def wrap_text(text, width=80):
    """
    Wrap the text so that each line is no longer than 'width' characters.
    :param text: The input text to wrap.
    :param width: The maximum number of characters per line.
    :return: Wrapped text with newlines after every 'width' characters.
    """
    return '\n'.join([text[i:i + width] for i in range(0, len(text), width)])


class LanguageModel:
    def __init__(self, max_n=1):
        """
        Initialize the Language Model with a specified max n-gram size.
        The model will learn n-grams for all values from 2 to max_n.
        :param max_n: The maximum size of the n-gram (number of characters in the sequence).
        """
        self.max_n = max_n
        self.models = {n: defaultdict(Counter) for n in range(2, max_n + 1)}

    def train(self, training_text_chunk):
        """
        Train the language model on a chunk of text for all n-grams from 2 to max_n.
        :param training_text_chunk: The text data chunk used for training the model.
        :return: The number of words processed during training.
        """
        training_text_chunk = clean_text(training_text_chunk.lower())  # Clean the input text
        words = training_text_chunk.split()  # Split text to count words
        text_length = len(training_text_chunk)

        # Train for all n-grams from n=2 to n=max_n
        for n in range(2, self.max_n + 1):
            for i in range(text_length - n):
                sequence = training_text_chunk[i:i + n]
                next_character = training_text_chunk[i + n]
                self.models[n][sequence][next_character] += 1

        return len(words)

    def predict(self, sequence):
        """
        Predict the next character for a given sequence using all available n-gram models.
        :param sequence: The input sequence of characters.
        :return: The predicted next character.
        """
        sequence = sequence.lower()
        sequence_length = len(sequence)

        # Try to predict using the largest n-gram possible (based on the input sequence length)
        for n in range(min(sequence_length, self.max_n), 1, -1):
            sub_sequence = sequence[-n:]  # Get the last n characters
            if sub_sequence in self.models[n]:
                next_characters = self.models[n][sub_sequence]
                total_occurrences = sum(next_characters.values())
                choices, weights = zip(*next_characters.items())
                probabilities = [weight / total_occurrences for weight in weights]
                return random.choices(choices, probabilities)[0]

        # Fall back to random character if no match found
        return random.choice('abcdefghijklmnopqrstuvwxyz ')

    def generate_text(self, start_sequence, generating_length=100):
        """
        Generate text based on the trained model starting from a given sequence.
        :param start_sequence: The initial sequence of characters to start generation.
        :param generating_length: The number of characters to generate.
        :return: The cleaned and wrapped generated text string.
        """
        current_sequence = start_sequence.lower()
        generated_text = current_sequence
        for _ in range(generating_length):
            next_character = self.predict(current_sequence)
            generated_text += next_character
            current_sequence = generated_text[-self.max_n:]  # Use max_n characters as context

        # Clean the generated text to remove extra spaces/newlines
        cleaned_text = clean_text(generated_text)
        # Wrap the text to 80 characters per line
        return wrap_text(cleaned_text)

    def get_model_memory_usage(self):
        """
        Calculate and return the memory usage of the model in kilobytes (KB).
        :return: The memory usage of the model in kilobytes.
        """
        total_size = 0
        for n, model in self.models.items():
            total_size += sys.getsizeof(model)
            for sequence, counter in model.items():
                total_size += sys.getsizeof(sequence) + sys.getsizeof(counter)
                for char, count in counter.items():
                    total_size += sys.getsizeof(char) + sys.getsizeof(count)
        return total_size / 1024  # Convert bytes to kilobytes


class LanguageModelApp:
    def __init__(self, max_n=3):
        """
        Initialize the Language Model Application.
        :param max_n: The size of the maximum n-gram for the language model.
        """
        self.language_model = LanguageModel(max_n=max_n)

    def display_help(self):
        """
        Display the list of available commands to the user.
        """
        print("Commands:")
        print("  exit                -- Exit the application")
        print("  prompt: your text   -- Generate text using your prompt")
        print("  load [filename]     -- Load and learn from the specified text file(s), or load from 'save.kls'")
        print("  save                -- Save the current language model to 'save.kls'")
        print("  help                -- Display this help")
        print()

    def display_memory_usage(self):
        """
        Display the memory usage of the language model.
        """
        memory_usage = self.language_model.get_model_memory_usage()
        print(f"Your language model uses {memory_usage:.2f} KB of memory.")
        print()

    def handle_exit(self):
        """
        Handle the 'exit' command to terminate the application.
        """
        print("Exiting the application.")

    def handle_prompt(self, user_input_text):
        """
        Handle the 'prompt:' command to generate text based on user input.
        :param user_input_text: The entire user input string containing the prompt.
        """
        prompt_text = clean_text(user_input_text[7:].strip())  # Clean the input prompt
        if not prompt_text:
            print("Please provide a prompt after 'prompt:'.")
            return
        generating_length_input = input("Enter the length of text to generate: ").strip()
        if generating_length_input.isdigit():
            generating_length = int(generating_length_input)
        else:
            print("Invalid length. Using default length of 100.")
            generating_length = 100
        generated_text = self.language_model.generate_text(prompt_text, generating_length=generating_length)
        print("Generated Text:")
        print(generated_text)
        self.display_memory_usage()  # Display memory usage after generating text

    def handle_load(self, user_input_text):
        """
        Handle the 'load' command to load and train on specified text file(s) or load 'save.kls'.
        Supports wildcards (e.g., '*.txt').
        :param user_input_text: The entire user input string containing the filename or pattern.
        """
        pattern = user_input_text[5:].strip()  # Extract the filename or pattern after 'load '

        # If no pattern is provided, load from the 'save.kls' file
        if not pattern:
            if os.path.exists("save.kls"):
                try:
                    # Explicitly reinitialize the model to free up memory before loading the new one
                    del self.language_model  # Delete the current model to free memory
                    gc.collect()  # Force garbage collection to release memory

                    with open("save.kls", "rb") as f:
                        self.language_model = pickle.load(f)  # Load the saved model
                    print("Successfully loaded the language model from 'save.kls'.")
                    self.display_memory_usage()  # Display memory usage after loading
                except Exception as e:
                    print(f"Error loading 'save.kls': {e}")
            else:
                print("No save.kls file found. Please train the model or load a file.")
            return

        # If a pattern is provided, load text files
        files_to_load = glob.glob(pattern)

        if not files_to_load:
            print(f"No files matched the pattern '{pattern}'.")
            return

        total_words_processed = 0
        for filename in files_to_load:
            if os.path.isfile(filename):
                try:
                    # Read file in chunks to save memory
                    with open(filename, 'r', encoding='utf-8') as file:
                        for chunk in iter(lambda: file.read(1024 * 1024), ''):  # Read in 1MB chunks
                            num_words = self.language_model.train(chunk)
                            total_words_processed += num_words
                            del chunk  # Explicitly delete the chunk to free memory
                            gc.collect()  # Force garbage collection to ensure memory is freed
                    print(f"Successfully loaded and trained on '{filename}'.")
                    print(f"Number of words processed from '{filename}': {total_words_processed}")
                except Exception as e:
                    print(f"Error reading '{filename}': {e}")
            else:
                print(f"File '{filename}' does not exist.")

        # Display the total number of words processed from all files
        print(f"Total number of words processed from all files: {total_words_processed}")
        self.display_memory_usage()  # Display memory usage after loading files

    def handle_save(self):
        """
        Handle the 'save' command to save the current language model to 'save.kls'.
        """
        try:
            with open("save.kls", "wb") as f:
                pickle.dump(self.language_model, f,
                            protocol=pickle.HIGHEST_PROTOCOL)  # Use highest protocol for efficiency
            print("Successfully saved the language model to 'save.kls'.")
        except Exception as e:
            print(f"Error saving the language model: {e}")

    def run(self):
        """
        Run the main command loop of the application.
        """
        print("Welcome to the Language Model App!")
        self.display_help()
        while True:
            user_command = input("Enter command: ").strip()
            if user_command.lower() == "exit":
                self.handle_exit()
                break
            elif user_command.lower() == "help":
                self.display_help()
            elif user_command.lower().startswith("prompt:"):
                self.handle_prompt(user_command)
            elif user_command.lower().startswith("load"):
                self.handle_load(user_command)
            elif user_command.lower() == "save":
                self.handle_save()
            else:
                print("Invalid command. Please try again.")
                print("Type 'help' to see the list of available commands.")
                print()


if __name__ == "__main__":
    app = LanguageModelApp(max_n=6)  # Learn with all n's from 2 to 6
    app.run()
