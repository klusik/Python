"""
    Read CSV data from GPUz
"""

# IMPORTS #
import csv


# CLASSES #
class Config:
    default_file_name = r"GPU-Z Sensor Log.txt"
    default_file_encoding = 'cp1250'


class Data:
    def __init__(self,
                 filename,  # Name of the file
                 ):

        # Instnance variables #

        # Raw data from a file
        self.raw_data = str()

        # All data categorized
        self.data = list()

        # Unig mapping dictionary
        self.unit_mapping = dict()

        # Reading a file
        try:
            with open(filename, 'r', encoding=Config.default_file_encoding) as csv_file:
                csv_file_content = csv.DictReader(csv_file)
                for csv_line in csv_file_content:
                    trimmed_line = {
                        key.strip(): value for key, value in csv_line.items()
                    }
                    self.data.append(trimmed_line)

                    # Extract units and create unit_mapping
                    if not self.unit_mapping:
                        self.unit_mapping = {
                            key.strip().split('[')[0].strip(): key.split('[')[-1].rstrip(']')
                            for key in trimmed_line.keys()
                        }

        except FileNotFoundError as e_file_not_found:
            print(f"A file {filename} couldn't be found.")

        self.get_data()

    def get_data(self, column_name=None):
        for line in self.data:
            for key in line.keys():
                stripped_key = key.strip()
                if stripped_key in self.unit_mapping:
                    unit = self.unit_mapping[stripped_key]
                elif stripped_key:
                    if '[' in stripped_key:
                        stripped_key = stripped_key[:stripped_key.index('[')].strip()
                    print(stripped_key)


# RUNTIME #
def main():
    data = Data(Config.default_file_name)


if __name__ == "__main__":
    main()
