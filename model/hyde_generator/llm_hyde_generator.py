class LLMHydeGenerator:
    def __init__(self, llm, template):
        self.name = f"LLM hyde generator with {llm.model}, using template {template.name} : {template.template_script}"
        self.llm = llm
        self.template = template
    
    def generate_hyde(self, crawl_session):
        prompt = self.template.complete(crawl_session)
        print(prompt)
        try : 
            response = self.llm.generate_hyde(prompt)
        except Exception as e:
            print(f"Erreur lors de l'appel au LLM : {e}")
            response = ''
        print(response)
        return(response)