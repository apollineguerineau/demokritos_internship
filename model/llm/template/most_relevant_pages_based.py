from model.llm.template.abstract_template import AbstractTemplate
import config

class MostRelevantPagesBasedTemplate(AbstractTemplate):
    def __init__(self, nb_pages):
        super().__init__(name=f" {nb_pages} most relevant pages based", template_script=config.MOSTRELEVANTBASED)
        self.nb_pages = nb_pages

    def get_most_relevant_pages(self, crawl_session):
        sorted_pages = []
        for page in crawl_session.fetched_pages:
            i = 0
            while i < len(sorted_pages) and sorted_pages[i].score < page.score:
                i += 1
            sorted_pages.insert(i, page)
        return(sorted_pages[:self.nb_pages])

    def complete(self, crawl_session):
        initial_query = crawl_session.seed_query
        most_relevant_pages = self.get_most_relevant_pages(crawl_session)
        return(self.template_script.format(initial_query, most_relevant_pages))