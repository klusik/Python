"""
    It won't be as great as Mr. Smallcastle's vision,
    but for default distribution, it should work.
"""
# IMPORTS #

# CLASSES #
class Config:
    """ This class just handles configuration """
    
    # Configuration
    config_file = "config.ini"

    def __init__(self):
        pass

    def get_config_file(self):
        return self.config_file

# RUNTIME #
def main():
    pass

if __name__ == "__main__":
    main()