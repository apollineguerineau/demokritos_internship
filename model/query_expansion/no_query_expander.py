from query_expansion.abstract_query_expander import AbstractQueryExpander

class NoQueryExpander(AbstractQueryExpander):
    def __init__(self):
        self.name = "No expansion"
        
    def expand_query(self, old_query, fetched_pages):
        return(old_query)
        