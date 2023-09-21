"""
    Read IMDB export CSV file
"""

# IMPORTS #
import csv


# CLASSES #
class Movie:
    pass


class Movies:
    def __init__(self,
                 file_name: str):
        with open(file_name, 'r') as csv_file:
            pass


# RUNTIME #
def main():
    movies_list = Movies("ratings.csv")


if __name__ == "__main__":
    main()
