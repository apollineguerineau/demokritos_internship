from abc import ABC, abstractmethod

class AbstractClassifier(ABC) : 
    def __init__(self, name, require_hyde):
        self.name = name
        self.require_hyde = require_hyde
    
    @abstractmethod
    def attribute_score(self, crawl_session, new_fetched_pages):
        pass
