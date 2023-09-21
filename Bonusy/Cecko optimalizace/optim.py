"""
    Trying to optimize C code.
"""

if __name__ == "__main__":
    with open('code.c', 'w') as c_code:
        # header
        c_code.write("#include <stdio.h>\n")
        c_code.write("int main() {\n")

        c_code.write("\tint number;\n")
        c_code.write("\tprintf(\"Enter a number: \");\n")
        c_code.write("\tscanf(\"%d\", &number);\n")

        # Big ifs
        output = ""
        for number in range(10000):
            if not (number % 1000):
                print(number)

            output += f"\tif (number == {number})"
            output += " {\n"
            output += f'\t\tprintf("You have entered {number}.");\n'
            output += "\t}\n"

        c_code.write(output)

        c_code.write(f'\tif (number > {number}) ')
        c_code.write('{\n')
        c_code.write(f"\t\tprintf(\"You have entered number greater than {number}\");\n")
        c_code.write("\t}\n")

        c_code.write("}\n")