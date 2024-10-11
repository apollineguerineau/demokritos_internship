from abc import ABC, abstractmethod

class AbstractStopCriteria :
    
    def __init__(self, crawl_session, name) : 
        self.crawl_session = crawl_session
        self.name = name

    @abstractmethod
    def is_reached():
        pass