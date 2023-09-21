""" Format BTC text into something more readable """

# Input file
input_file = "bitcoinovy_standard_altcoiny.txt"
output_file = 'bitcoinovy_standard_altcoiny_čitelný.txt'


def do_magic():
    file_contents = str()

    with open(input_file, 'r', encoding='utf-8') as f_btc:
        file_contents = f_btc.read()

    print(new_content := file_contents.replace('\n\n', '\n'))

    with open(output_file, 'w', encoding='utf-8') as fo_btc:
        fo_btc.write(new_content)


if __name__ == "__main__":
    do_magic()
