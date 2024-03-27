"""
    Config file for personal finances app
"""

import os
from pathlib import Path


class Config:
    # Data file name for finances
    _data_file_name = r'finances.json'

    # Path to data file
    _data_file_path = r'data/'

    # Default encoding
    _default_enc = 'utf-8'

    # Json indent size
    _default_json_indent = 4

    @classmethod
    def data_file(cls) -> str:
        """
        Creates a data file path

        :return: string with a file path
        :rtype: src
        """
        return os.path.join(cls._data_file_path, cls._data_file_name)

    @classmethod
    def default_encoding(cls) -> str:
        """
        Prepares a default encoding stub
        :return: string with encoding
        :rtype: str
        """
        return cls._default_enc

    @classmethod
    def json_indent(cls) -> int:
        """
        Returns the indent size for JSON files
        :return: Indent size
        :rtype: int
        """
        return int(cls._default_json_indent)