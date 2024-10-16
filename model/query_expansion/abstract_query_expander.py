from abc import ABC, abstractmethod

class AbstractQueryExpander :
    
    @abstractmethod
    def expand_query(self, crawl_session):
        pass