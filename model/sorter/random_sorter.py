from sorter.abstract_sorter import AbstractSorter
import random

class RandomSorter(AbstractSorter):

    def __init__(self):
        self.name = "Random sorter"
        
    def sort(self, candidate_pages):
        random.shuffle(candidate_pages)
        return(candidate_pages)