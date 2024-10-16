from abc import ABC, abstractmethod

class AbstractSorter(ABC) : 
    def __init__(self, name):
        self.name = name
    
    @abstractmethod
    def sort(self, fetched_pages, new_pagess):
        pass
