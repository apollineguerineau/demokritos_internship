from model.classifier.abstract_classifier import AbstractClassifier
import numpy as np
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings

class SimilarityClassifier(AbstractClassifier):
        
    def __init__(self, name_embed_model):
            super().__init__(name='cosine similarity', require_hyde=False)
            model_kwargs = {'device': 'cpu'}
            encode_kwargs = {'normalize_embeddings': False}
            self.embed_model = HuggingFaceEmbeddings(
                model_name=name_embed_model,
                model_kwargs=model_kwargs,
                encode_kwargs=encode_kwargs)
            self.embed_queries = {}

    def embed_text(self, input_text):
        text = 'query: ' + input_text
        return(self.embed_model.embed_query(text))
    
    def cosine_similarity(self, vec1, vec2):
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        dot_product = np.dot(vec1, vec2)
        norm_vec1 = np.linalg.norm(vec1)
        norm_vec2 = np.linalg.norm(vec2)
        
        if norm_vec1 == 0 or norm_vec2 == 0:
            return 0.0
        else : 
            sim = dot_product / (norm_vec1 * norm_vec2)
            return sim

    def attribute_score(self, crawl_session, page) : 
        query = crawl_session.seed_query
        if query not in self.embed_queries.keys():
            embed_query = self.embed_text(query)
            self.embed_queries[query] = embed_query
        else : 
            embed_query = self.embed_queries[query]
        embed_page = self.embed_text(page.title + page.description)
        score = self.cosine_similarity(embed_query, embed_page)
        return(score)