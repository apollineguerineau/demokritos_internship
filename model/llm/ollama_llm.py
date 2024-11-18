from model.llm.abstract_llm import AbstractLLM
import ollama
import ast
import re
import json

class OllamaLLM(AbstractLLM):
    def __init__(self, model):
        super().__init__(model)

    def generate_hyde(self, prompt):
        resp = ollama.chat(model=self.model, messages=[{'role': 'user', 'content': prompt}])
        response_str = resp['message']['content']
        response_str = response_str.split('{')[1]
        response_str = response_str.split('}')[0]
        title, abstract = response_str.split('"abstract": ')
        title = title.split('"title": ')[1]
        title = title.split(',\n')[0]
        title = title.replace('"', "")
        abstract = abstract.replace('"', "")
        abstract = abstract.replace('\n', "")
        hyde_page = {'title':title, 'abstract':abstract}
        print(hyde_page)
        return(hyde_page)
    
    def generate_expanded_query(self, prompt):
        response_str = ollama.chat(model=self.model, messages=[{'role': 'user', 'content': prompt}])
        print(response_str['message']['content'])
        response_dict = ast.literal_eval(response_str['message']['content'])
        return(response_dict['expanded_query'])
