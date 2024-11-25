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


initial_query = '"Machine_Learning"_AND_(diffusion_OR_diffusivity)_AND_(MOFs_OR_ZIFs_OR_"metal-organic_frameworks"_OR_COFs_OR_"covalent-organic_frameworks)/'
base_path = f'/Users/apollineguerineau/Documents/ENSAI/3A/Greece/internship/eval/results/{initial_query}'
path_seed_query_expand = base_path + 'SeedQueryBasedTemplate__/'
fetched_pages = pd.read_csv(path_seed_query_expand + 'fetched_pages.csv')

#######################################################################################
###################################   SIM CLASSIFIER  #################################
#######################################################################################

classifier = SimilarityClassifier(name_embed_model='intfloat/multilingual-e5-base')
crawl_session = CrawlSession(session_name='test', query='')
scores = []
for index, row in fetched_pages.iterrows():
        print(f'Line {index+1} sur {len(fetched_pages)}')
        page = Page(row['url'], row['title'], row['description'])
        score = classifier.attribute_score(crawl_session, page)
        scores.append(score)

fetched_pages['score'] = scores
classified_data_path = path_seed_query_expand + '/sim_cos/fetched_pages.csv'
fetched_pages.to_csv(classified_data_path, index=False)

#######################################################################################
###################################   HYDE CLASSIFIER  ################################
#######################################################################################

classifier2 = HydeSimilarityClassifier(name_embed_model='intfloat/multilingual-e5-base')
crawl_session2 = CrawlSession(session_name='test', query='"Machine_Learning"_AND_(diffusion_OR_diffusivity)_AND_(MOFs_OR_ZIFs_OR_"metal-organic_frameworks"_OR_COFs_OR_"covalent-organic_frameworks)')
template_hyde = HydeBasedTemplate()
llm = OllamaLLM(model='llama3.2')
hyde_generator = LLMHydeGenerator(llm=llm, template=template_hyde)
hyde = hyde_generator.generate_hyde(crawl_session2)
print(hyde)
crawl_session2.hyde = hyde

scores = []
for index, row in fetched_pages.iterrows():
        print(f'Line {index+1} sur {len(fetched_pages)}')
        page = Page(row['url'], row['title'], row['description'])
        score = classifier2.attribute_score(crawl_session2, page)
        scores.append(score)

fetched_pages['score'] = scores
classified_data_path_hyde = path_seed_query_expand + '/hyde_sim_cos/fetched_pages.csv'
fetched_pages.to_csv(classified_data_path_hyde, index=False)

print(hyde)




