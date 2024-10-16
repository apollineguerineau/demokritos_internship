from model.sorter.classifier.abstract_classifier import AbstractClassifier
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F

class TransformerBasedClassifier(AbstractClassifier):

    def __init__(self, name, path_to_model, path_to_tokenizer):
        super().__init__(name=name)
        self.model = AutoModelForSequenceClassification.from_pretrained(path_to_model)
        self.model.eval()
        self.tokenizer = AutoTokenizer.from_pretrained(path_to_tokenizer)
        
    def classify(self, page):
        text = page.title + '\n' + page.description
        encoding = self.tokenizer.encode_plus(text,
                                            add_special_tokens=True,
                                            max_length=128,
                                            return_token_type_ids=False,
                                            padding='max_length',
                                            return_attention_mask=True,
                                            return_tensors='pt',
                                            truncation=True)

        input_ids = encoding['input_ids']
        attention_mask = encoding['attention_mask']

        # Déplacer les tenseurs vers le GPU si disponible
        with torch.no_grad():
            outputs = self.model(input_ids, attention_mask=attention_mask)

        # Obtenir les logits et appliquer softmax pour obtenir les probabilités
        logits = outputs.logits
        probabilities = F.softmax(logits, dim=-1).numpy()
        return(probabilities[0][0])