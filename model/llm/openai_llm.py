from model.llm.abstract_llm import AbstractLLM
from openai import OpenAI

class OpenAILLM(AbstractLLM):
    def __init__(self, model,token) :
        super().__init__(model)
        self.token = token

    def generate(self, prompt):
        client = OpenAI(api_key=self.token)

        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", 
                "content": prompt}]
        )

        return(chat_completion)






    
