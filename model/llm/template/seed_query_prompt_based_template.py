from model.llm.template.abstract_template import AbstractTemplate
import config

class SeedQueryPromptBasedTemplate(AbstractTemplate):
    def __init__(self):
        super().__init__(name="seed query prompt based", template_script=config.QUERY_PROMPT_BASED)

    def complete(self, crawl_session):
        initial_query = crawl_session.seed_query
        prompt = crawl_session.prompt
        return(self.template_script.format(initial_query, prompt))