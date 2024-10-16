from model.llm.abstract_llm import AbstractLLM
from transformers import pipeline
import torch

from huggingface_hub import InferenceClient

class HuggingFaceLLM(AbstractLLM):
    def __init__(self, model, token):
        super().__init__(model)
        self.token = token
        # Check if GPU is available
        device = 0 if torch.cuda.is_available() else -1
        self.chatbot = pipeline("text-generation", model="mistralai/Mistral-7B-Instruct-v0.3", do_sample=True, temperature=1, max_new_tokens = 1000, token=token, device=device)

    def generate(self, prompt):

        messages = [
            {"role": "user", "content": prompt},
        ]
        
        return(self.chatbot(messages))
        # client = InferenceClient(api_key=self.token)
        # print(prompt)

        # response = ''
        # for message in client.chat_completion(
        #     model=self.model,
        #     messages=[{"role": "user", "content": prompt}],
        #     max_tokens=500,
        #     stream=True,
        #     ):
        #     response+=message.choices[0].delta.content
        # return(response)




