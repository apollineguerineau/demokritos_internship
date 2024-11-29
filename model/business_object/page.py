class Page:
    def __init__(self, url, title, description):
        self.url = url
        self.title = title
        self.description = description
        self.score = 'na'
        self.get_with_query = ''
        self.is_seed = False

    def __eq__(self, other):
        if isinstance(other, Page):
            return (self.url == other.url)
        return False
    
    def __str__(self):
        return (
            f"Title: {self.title}\n"
            f"URL: {self.url}\n"
            f"Description: {self.description}\n"
            f"Score: {self.score}\n"
            f"Query: {self.get_with_query}\n"
        )