from abc import ABC, abstractmethod

class AbstractTemplate(ABC):
    def __init__(self, name, template_script) :
        self.name = name
        self.template_script = template_script
    
    @abstractmethod
    def complete(self, crawl_session):
        pass