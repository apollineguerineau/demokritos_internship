from model.llm.template.abstract_template import AbstractTemplate

class CurrentQueryBasedTemplate(AbstractTemplate):
    def __init__(self,template_script):
        super().__init__(name = "current query based", template_script = template_script)

    def complete(self, crawl_session):
        initial_query = crawl_session.current_query
        return(self.template_script.format(initial_query))