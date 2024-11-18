from model.query_expansion.abstract_query_expander import AbstractQueryExpander

class LLMQueryExpander(AbstractQueryExpander):
    def __init__(self, llm, template):
        self.name = f"LLM query expander with {llm.model}, using template {template.name} : {template.template_script}"
        self.llm = llm
        self.template = template
    
    def expand_query(self, crawl_session):
        prompt = self.template.complete(crawl_session)
        print(prompt)
        try : 
            response = self.llm.generate_expanded_query(prompt)
        except Exception as e:
            print(f"Erreur lors de l'appel au LLM : {e}")
            response = crawl_session.current_query
        print(response)
        return(response)