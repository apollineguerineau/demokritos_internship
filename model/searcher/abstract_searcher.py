from abc import ABC, abstractmethod

class AbstractSearcher(ABC) : 
    
    @abstractmethod
    def get_max_results():
        pass
    
    @abstractmethod
    def get_page():
        pass

    @abstractmethod
    def get_all_pages():
        pass

    
