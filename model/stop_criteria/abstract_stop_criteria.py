from abc import ABC, abstractmethod

class AbstractStopCriteria :
    
    def __init__(self, name) : 
        self.name = name

    @abstractmethod
    def is_reached():
        pass