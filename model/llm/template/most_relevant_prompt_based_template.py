from model.llm.template.abstract_template import AbstractTemplate
import config

class MostRelevantPagesPromptBasedTemplate(AbstractTemplate):
    def __init__(self, nb_pages):
        super().__init__(name=f" {nb_pages} most relevant pages and prompt based", template_script=config.MOSTRELEVANT_PROMPT_BASED)
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
        prompt = crawl_session.prompt
        most_relevant_pages = self.get_most_relevant_pages(crawl_session)
        return(self.template_script.format(initial_query, prompt, most_relevant_pages))