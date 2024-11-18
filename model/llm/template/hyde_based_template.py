from model.llm.template.abstract_template import AbstractTemplate
import config

class HydeBasedTemplate(AbstractTemplate):
    def __init__(self):
        super().__init__(name="hyde", template_script=config.HYDE)
        
    def complete(self, crawl_session):
        initial_query = crawl_session.seed_query
        return(self.template_script.format(initial_query))