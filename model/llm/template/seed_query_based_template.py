from model.llm.template.abstract_template import AbstractTemplate

class SeedQueryBasedTemplate(AbstractTemplate):
    def __init__(self,template_script):
        super().__init__(name="seed query based", template_script=template_script)

    def complete(self, crawl_session):
        initial_query = crawl_session.seed_query
        return(self.template_script.format(initial_query))