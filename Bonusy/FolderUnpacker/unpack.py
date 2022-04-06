"""
    Unpack all folders, merge all the files inside,
    rename the files via wildcards

    Author: klusik@klusik.cz

    Default settings:
    -   Reads all file names in all subfolders
    -   Copies all files into another folder (default name "_unpacked")
    -   Renames files as "file_#####.<original extension>" where "#" number
        is dependent on how many files are there.
"""

# IMPORTS #
import os
import pprint


# CLASSES #

# RUNTIME #
def read_all_files(directory):
    """ Reads all files in directory and return their file names as a list """

    all_files = list()
    for path, current_directory, files in os.walk(directory):
        for file in files:
            # ignore files with '.' as first character,
            # which is character on index [2]

            file_path = f"{path}\{file}"

            if len(path) > 2:
                if path[2] == '.':
                    continue # next file

            if file[0] == '.':
                continue # next file

            all_files.append(file_path)

    return all_files


def move_files(files, destination_path):
    """ Moves files """


if __name__ == "__main__":
    all_files = read_all_files(".")

