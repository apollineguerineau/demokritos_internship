from datetime import datetime
import csv

class CrawlSession:
    def __init__(self, session_name, query):

        self.session_name = session_name
        self.start_time = datetime.now()

        self.all_queries = query
        self.current_query = query
        self.seed_query = query

        self.seed_pages = []
        self.fetched_pages = []
        self.rejected_pages = []

        self.hyde = None

    def add_fetched_page(self, page):
        self.fetched_pages.append(page)

    def add_rejected_page(self, page):
        self.rejected_pages.append(page)

        