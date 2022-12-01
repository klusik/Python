"""
    Simple file browser :-)

    It is not very user-friendly, but it is
    a good example in terms of object-oriented programming lessons.

    It's highly ineffective, because it reads & saves all files content
    into the memory right away.

    Goal: Load files from current folder

    Usage -- basic commands

        files   -- show files in current folder with full details
        file <filename>     -- show single file information
        print <filename>    -- print the content of the file
        help    -- print available commands
        exit    -- exit program

    Exmamples:

        file simple_file_browser.py
            (displays this file)

"""

# IMPORTS #
import os

# CLASSES #
class File(object):
    """ Information about a file """
    def __init__(self, file_name):
        self.file_name = file_name


class Folder(object):
    """ Folder contents (files in current folder) """
    def __init__(self):
        folder_content = os.listdir(".")

        # Create a list of files
        self.folder = []

        # Scan all object in the folder and save only files (not folders)
        for file_name in folder_content:
            if os.path.isfile(file_name):
                self.folder.append(File(file_name))


    def print_file(self, filename):
        with open(filename, 'r', encoding="utf-8") as file_link:
            print(file_link.read())

    def display_folder(self):
        """ Prints information about files in folder """
        for file in self.folder:
            print(file.file_name)

class Command:
    """ Commands which user can use """
    commands = {
        "files" : "Displays all files in current folder",
        "help" : "Displays help (available commands)",
        "exit" : "Exists program",
        "file"  : "Displays information about single file",
        "print" : "Displays file contents",
    }

    @classmethod
    def print_all_commands(cls):
        for command, description in cls.commands.items():
            print(f"{command} : {description}")

    @classmethod
    def available_commands(cls):
        return list(cls.commands.keys())

# RUNTIME #
def main():
    """ Main function """

    # Read contents of current folder
    folder = Folder()

    while True:
        # Main loop
        user_input = input("Enter command: ").split()

        if user_input[0] in Command.available_commands():
            # Switch between various commands
            if user_input[0] == "help":
                Command.print_all_commands()
                continue
            if user_input[0] == "exit":
                print("Bye")
                exit()
            if user_input[0] == "files":
                folder.display_folder()
                continue
            if user_input[0] == "file":
                # Next argument should be filename
                try:
                    folder.display_folder(user_input[1])
                except IndexError:
                    print(f"File name must be entered!")
            if user_input[0] == "print":
                try:
                    folder.print_file(user_input[1])
                except IndexError:
                    print("File name must be specified!")
                except FileNotFoundError:
                    print(f"File {user_input[1]} does not exist!")
                except UnicodeDecodeError:
                    print(f"File {user_input[1]} contains something rather nasty, let's better not display it.")
        else:
            print("Unrecognized command. Here are available commands: ")
            Command.print_all_commands()
            continue




if __name__ == "__main__":
    main()