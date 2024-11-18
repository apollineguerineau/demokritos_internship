class LLMHydeGenerator:
    def __init__(self, llm, template):
        self.name = f"LLM hyde generator with {llm.model}, using template {template.name} : {template.template_script}"
        self.llm = llm
        self.template = template
    
    def generate_hyde(self, crawl_session):
        prompt = self.template.complete(crawl_session)
        response = self.llm.generate_hyde(prompt)
        try : 
            response = self.llm.generate_hyde(prompt)
        except Exception as e:
            response = ''
        return(response)