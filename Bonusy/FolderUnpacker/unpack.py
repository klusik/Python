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
import shutil


# CLASSES #

# RUNTIME #
def read_all_files(directory):
    """ Reads all files in directory and return their file names as a dict """

    all_files = dict()
    for path, current_directory, files in os.walk(directory):
        for file in files:
            # ignore files with '.' as first character,
            # which is character on index [2]

            file_path = f"{path}\{file}"

            if len(path) > 2:
                if path[2] == '.':
                    continue  # next file

            if file[0] == '.':
                continue  # next file

            all_files[file_path] = file

    return all_files


def move_files(files, destination_path):
    """ Moves files """

    # Prepare output folder
    try:
        os.mkdir(destination_path)
    except FileExistsError:
        # Directory exists
        # Remove directory content
        shutil.rmtree(destination_path)
        os.mkdir(destination_path)

    # Determine number of files (later for formatting the name)
    file_count = len(files)
    count_length = len(str(file_count))
    print(count_length)

    # Copying & renaming
    for counter, file in enumerate(files):
        # shutil.copyfile(file, f"{destination_path}\{file}")
        pprint.pprint(f"{file} : {files[file]}")
        extension = files[file].split('.')[-1]
        shutil.copyfile(file, f"{destination_path}\\file_{str(counter).zfill(count_length)}.{extension}")


if __name__ == "__main__":
    all_files = read_all_files(".")

    move_files(all_files, 'test')
