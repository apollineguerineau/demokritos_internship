import pandas as pd
from model.business_object.page import Page

class GetSeedPagesFromCsv : 
    def __init__(self, csv_path) : 
        self.dataframe = pd.read_csv(csv_path, header=0, sep=';')

    def get_pages(self):
        pages = []
        for index, row in self.dataframe.iterrows():
            url = row['url']
            title = row['title']
            description = row['description']
            links = row['links']
            publication_date = row['publication_date']
            authors = row['authors']
            language = row['language']
            notes = row['notes']
            page = Page(url, title, description, links, publication_date, authors, language, notes)
            pages.append(page)
        return pages
