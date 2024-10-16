from abc import ABC, abstractmethod

class AbstractLLM(ABC) : 
    def __init__(self, model) : 
        self.model = model
    
    @abstractmethod
    def generate(self, prompt) : 
        pass
    
