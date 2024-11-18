from model.classifier.similarity_classifier import SimilarityClassifier
from model.classifier.hyde_similarity_classifier import HydeSimilarityClassifier
from model.business_object.page import Page
from model.business_object.crawl_session import CrawlSession
from model.llm.template.hyde_based_template import HydeBasedTemplate
from model.hyde_generator.llm_hyde_generator import LLMHydeGenerator
from model.llm.ollama_llm import OllamaLLM
import pandas as pd 
import os
import csv

query = '''"Machine Learning" AND (diffusion OR diffusivity) AND (MOFs OR ZIFs OR "metal-organic frameworks" OR COFs OR "covalent-organic frameworks)'''
domain = "ML_MOF_Diffusion"
labelled_data_filename = "dataset_ML_MOF_Diffusion.csv"

# query = '''RAG AND "code generation"'''
# domain = "RAG_code_generation"
# labelled_data_filename = "dataset_rag.csv"

labelled_data = pd.read_csv(f'/Users/apollineguerineau/Documents/ENSAI/3A/Greece/internship/eval/{domain}/{labelled_data_filename}')

#######################################################################################
###################################   SIM CLASSIFIER  #################################
#######################################################################################

# classifier = SimilarityClassifier(name_embed_model='intfloat/multilingual-e5-base')
# crawl_session = CrawlSession(session_name='test', query=query)
# scores = []
# for index, row in labelled_data.iterrows():
#         print(f'Line {index+1} sur {len(labelled_data)}')
#         page = Page(row['url'], row['title'], row['description'])
#         score = classifier.attribute_score(crawl_session, page)
#         scores.append(score)

# labelled_data['score'] = scores
#classified_data_path = f'/Users/apollineguerineau/Documents/ENSAI/3A/Greece/internship/eval/{domain}/threshold/cos_sim.csv'
# labelled_data.to_csv(classified_data_path, index=False)

#######################################################################################
###################################   HYDE CLASSIFIER  ################################
#######################################################################################

classifier = HydeSimilarityClassifier(name_embed_model='intfloat/multilingual-e5-base')
crawl_session = CrawlSession(session_name='test', query=query)
template_hyde = HydeBasedTemplate()
llm = OllamaLLM(model='llama3.2')
hyde_generator = LLMHydeGenerator(llm=llm, template=template_hyde)

hyde_path = f'/Users/apollineguerineau/Documents/ENSAI/3A/Greece/internship/eval/{domain}/threshold/hyde/hydes_info.csv'

with open(hyde_path, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
                'filename', 'hyde'
        ]
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)

for i in range(10):
        hyde = hyde_generator.generate_hyde(crawl_session)
        crawl_session.hyde = hyde

        with open(hyde_path, mode='a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([f'hyde{i+1}',hyde])

        scores = []
        for index, row in labelled_data.iterrows():
                print(f'Line {index+1} sur {len(labelled_data)}')
                page = Page(row['url'], row['title'], row['description'])
                score = classifier.attribute_score(crawl_session, page)
                scores.append(score)

        labelled_data['score'] = scores
        classified_data_path = f'/Users/apollineguerineau/Documents/ENSAI/3A/Greece/internship/eval/{domain}/threshold/hyde/hyde{i+1}.csv'
        labelled_data.to_csv(classified_data_path, index=False)





