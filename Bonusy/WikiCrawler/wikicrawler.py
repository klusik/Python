"""
    Author:         Rudolf Klusal (python@klusik.cz)

    Descritpion:    Create a web crawler which goes through Wikipedia
                    into given depth (default value would be set)

    Details:        Using only TEXT field on the Wiki, not adverts, menus, refferences etc.
                    Using only links to wikipedia itself.
                    If the same link is used multiple times, creates it only once.
                    Pages on wikipedia could (and frequently it's true) link to each other. If some page is used previously, don't use it again.
"""

# IMPORTS #
import wikipediaapi

# CLASSES #
class Config:
    """ Configuration values """

    # Depth of a search
    depth = 2

    # Default search language
    language = 'en'

    # Limit number of pages downloaded
    limit = 10

    # Use that limit
    use_limit = True




class WikiPage:
    def __init__(self,
                 wiki_name, # Name of the page
                 depth=Config.depth, # Depth of a search
                 root=True, # If this node is the root node
                 ):
        self.wiki = wikipediaapi.Wikipedia(Config.language)
        self.wiki_page = self.wiki.page(wiki_name)
        self.wiki_text = self.wiki_page.text
        self.wiki_links = self.wiki_page.links

        # If there's a limit, use it
        if Config.use_limit:
            Config.limit -= 1


        # Inform user about reading a node
        print(f"Reading:\t{wiki_name} (depth: {depth}, limit: {Config.limit})")

        # Links for the search
        self.wiki_links_list = []

        # Final dictionary
        self.wiki_structure = dict()

        # Download links from Wikipedia links
        self.prepare_links()



        # Go through all the links and download pages
        # Go only of depth > 1
        if depth > 1:
            for wiki_link in self.wiki_links:
                # Create a node for every link
                node = WikiPage(wiki_link, root=False, depth=depth-1)

                # Add node to dictionary
                self.wiki_structure[wiki_link] = (
                    node.get_text(),
                    node.get_links(),
                )

                # If limit is used
                if Config.use_limit:
                    if Config.limit == 0:
                        return


    def prepare_links(self):
        for link in self.wiki_links:
            self.wiki_links_list.append(link)

    def get_text(self):
        return self.wiki_text

    def get_links(self):
        return self.wiki_links_list


# RUNTIME #
def wiki_crawler():
    wiki = WikiPage("Python (Programming Language)")

if __name__ == "__main__":
    wiki_crawler()