from abc import ABC, abstractmethod

class AbstractLLM(ABC) : 
    def __init__(self, model) : 
        self.model = model

    @abstractmethod
    def generate_hyde(self, prompt) : 
        pass
    
    @abstractmethod
    def generate_expanded_query(self, prompt) : 
        pass
    
