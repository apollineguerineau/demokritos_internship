from model.llm.template.abstract_template import AbstractTemplate
import config

class HydePromptBasedTemplate(AbstractTemplate):
    def __init__(self):
        super().__init__(name="hyde_prompt", template_script=config.HYDE_PROMPT)
        
    def complete(self, crawl_session):
        initial_query = crawl_session.seed_query
        prompt = crawl_session.prompt
        return(self.template_script.format(initial_query, prompt))