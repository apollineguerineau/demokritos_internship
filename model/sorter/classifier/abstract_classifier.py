from abc import ABC, abstractmethod

class AbstractClassifier(ABC):

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def classify(page):
        pass
