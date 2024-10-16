from model.llm.abstract_llm import AbstractLLM
import ollama
import ast

class OllamaLLM(AbstractLLM):
    def __init__(self, model):
        super().__init__(model)

    def generate(self, prompt):
        response_str = ollama.chat(model=self.model, messages=[{'role': 'user', 'content': prompt}])
        response_dict = ast.literal_eval(response_str['message']['content'])
        return(response_dict['related_term'])
