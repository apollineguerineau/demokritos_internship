from model.query_expansion.abstract_query_expander import AbstractQueryExpander

class NoQueryExpander(AbstractQueryExpander):
    def __init__(self):
        self.name = "No expansion"
        
    def expand_query(self, crawl_session):
        return(crawl_session.current_query)
        