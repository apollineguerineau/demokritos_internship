class Page:
    def __init__(self, url, title, description, links, publication_date, authors, language, notes, score=0):
        self.url = url  # The URL of the page
        self.title = title  # The title of the page
        self.description = description  # A brief description of the page
        self.links = links  # The links contained on the page 
        self.publication_date = publication_date  # The publication date of the page
        self.authors = authors  # A list of authors of the page
        self.language = language  # The language the page is written in
        self.notes = notes  # notes
        self.score = score

    def __eq__(self, other):
        # Compare only if the other object is an instance of Page
        if isinstance(other, Page):
            return (self.url == other.url)
        return False