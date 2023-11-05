"""
    Hláškoreader

    Author: hlaskoreader@klusik.cz, 2023
"""

# IMPORTS #
from config.config import Config

import requests
from bs4 import BeautifulSoup


# CLASSES #
class App():
    def __init__(self):
        # Scrape the web
        web_scraped = BeautifulSoup(requests.get(Config.WEB).content, 'html.parser')

        text = web_scraped.text
        print(text)


# RUNTIME #
if __name__ == "__main__":
    app = App()
