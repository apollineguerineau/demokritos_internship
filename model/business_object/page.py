class Page:
    def __init__(self, url, title, description):
        self.url = url  # The URL of the page
        self.title = title  # The title of the page
        self.description = description  # A brief description of the page
        self.score = 'na'
        self.get_with_query = ''
        self.is_seed = False

    def __eq__(self, other):
        # Compare only if the other object is an instance of Page
        if isinstance(other, Page):
            return (self.url == other.url)
        return False
    
    def __str__(self):
        # links_str = '\n'.join(self.links)
        links_str = ''
        return (
            f"Title: {self.title}\n"
            f"URL: {self.url}\n"
            f"Description: {self.description}\n"
            f"Score: {self.score}\n"
            f"Query: {self.get_with_query}\n"
        )