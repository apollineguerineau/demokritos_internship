from model.sorter.abstract_sorter import AbstractSorter
import random

class RandomSorter(AbstractSorter):

    def __init__(self):
        super().__init__(name= "Random sorter")
        
    def sort(self, fetched_pages, new_pages):
        all_pages = fetched_pages + new_pages
        random.shuffle(all_pages)
        return(all_pages)