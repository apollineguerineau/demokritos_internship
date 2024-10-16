from model.sorter.abstract_sorter import AbstractSorter
import random

class ClassifierSorter(AbstractSorter):

    def __init__(self, classifier_model):
        super().__init__(name= f"Classifier sorter with {classifier_model}")
        self.classifier_model = classifier_model
        
    def sort(self, fetched_pages, new_pages):
        for page in new_pages : 
            page.score = self.classifier_model.classify(page)
            print(page.score)
            i = 0
            while i < len(fetched_pages) and fetched_pages[i].score < page.score:
                i += 1
            fetched_pages.insert(i, page)
        return(fetched_pages)