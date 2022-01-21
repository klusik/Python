# Generate words from given letters
#
# rspopta

import itertools
def combine_characters(characters, number_of_letters):
    yield from itertools.product(*[characters] * number_of_letters)

def main():

    letters = str(input("Zadejte znaky: "))
    final_word_length = int(input("Zadejte délku finálního slova: "))


    max_word_length = len(letters)

    all_found_words = set()

    print(f"Slova dlouha {final_word_length} znaků: ")
    all_found_words.clear()

    # generating words

    for word in combine_characters(letters, final_word_length):
        # clearing words not containing the right number of characters
        right_word = True
        word_joined = "".join(word)
        for letter in letters:
            if word_joined.count(letter) > letters.count(letter):
                # print(f"{word_joined} and {letters} neobsahují stejný počet znaků.")
                # not the right word
                right_word = False
                break

        if not right_word:
            continue

        # add word to set
        if right_word:
            all_found_words.add(word_joined)

    all_found_words_sorted = sorted(all_found_words)
    for word in all_found_words_sorted:
        print(word)
        # rspopta


if __name__ == "__main__":
    main()