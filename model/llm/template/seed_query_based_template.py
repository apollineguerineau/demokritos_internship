from model.llm.template.abstract_template import AbstractTemplate
import config

class SeedQueryBasedTemplate(AbstractTemplate):
    def __init__(self):
        super().__init__(name="seed query based", template_script=config.QUERYBASED)

    def complete(self, crawl_session):
        initial_query = crawl_session.seed_query
        return(self.template_script.format(initial_query))