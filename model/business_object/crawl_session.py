from datetime import datetime

class CrawlSession:
    def __init__(self, session_name, sorter, query_expander, searcher, query, seed_pages):
        self.session_name = session_name
        self.start_time = datetime.now()
        self.sorter = sorter
        self.query_expander = query_expander
        self.searcher = searcher
        self.seed_pages = seed_pages

        self.fetched_pages = []
        for page in self.seed_pages : 
            self.fetched_pages.append(page)
        self.all_queries = query
        self.current_query = query