from model.client_crawler import ClientCrawler

from model.business_object.crawl_session import CrawlSession
from model.business_object.page import Page

from model.classifier.similarity_classifier import SimilarityClassifier
from model.classifier.hyde_similarity_classifier import HydeSimilarityClassifier

from model.llm.template.seed_query_based_template import SeedQueryBasedTemplate
from model.llm.template.seed_query_prompt_based_template import SeedQueryPromptBasedTemplate
from model.llm.template.most_relevant_pages_based import MostRelevantPagesBasedTemplate
from model.llm.template.most_relevant_prompt_based_template import MostRelevantPagesPromptBasedTemplate

from model.llm.template.hyde_based_template import HydeBasedTemplate
from model.llm.template.hyde_prompt_based_template import HydePromptBasedTemplate

from model.llm.ollama_llm import OllamaLLM

from model.query_expansion.llm_query_expander import LLMQueryExpander

from model.hyde_generator.llm_hyde_generator import LLMHydeGenerator

from model.searcher.arxiv_searcher import ArxivSearcher
from model.searcher.chemrxiv_searcher import ChemRxivSearcher

import os

# Configuration de base
# base_output_dir = "/home/onyxia/work/demokritos_internship/crawl_results/MOF/"
# query = '''"Machine Learning" AND (diffusion OR diffusivity) AND (MOFs OR ZIFs OR "metal-organic frameworks" OR COFs OR "covalent-organic frameworks)'''
folder_base_output_dir = "/home/onyxia/work/demokritos_internship/crawl_results/"
# query = 'inverse design AND "metal-organic frameworks"'
# query = '"metal-organic frameworks" AND "material design" AND "properties"'
query = 'RAG AND "code generation"'
base_output_dir = folder_base_output_dir + query.replace(' ', '_') + '/'
prompt = 'Code generation is an area of artificial intelligence that aims to automate parts of software development. Retrieval-Augmented Generation (RAG) models are a novel approach in this field, combining information retrieval and text generation to produce context-aware code. These methods could help improve the relevance and quality of generated code, making them valuable for a wide range of applications, from prototyping to optimizing software for specific tasks.'
# prompt = "The query focuses on the use of Retrieval-Augmented Generation (RAG) models for automating and enhancing code generation. These models combine information retrieval and text generation capabilities to produce high-quality, context-aware code. The aim is to address challenges such as improving code relevance, reducing errors, and optimizing code for specific domains. Potential applications include rapid prototyping, system architecture optimization, and error mitigation in software development."
llm = OllamaLLM(model='llama3.2')

# searcher = ChemRxivSearcher()
searcher = ArxivSearcher()

sim_classifier = SimilarityClassifier(name_embed_model='intfloat/multilingual-e5-base')
hyde_classifier = HydeSimilarityClassifier(name_embed_model='intfloat/multilingual-e5-base')

# Query expansion configurations
query_expander_on_seed = LLMQueryExpander(llm=llm, template=SeedQueryBasedTemplate())
query_expander_on_seed_and_prompt = LLMQueryExpander(llm=llm, template=SeedQueryPromptBasedTemplate())
query_expander_best_page = LLMQueryExpander(llm=llm, template=MostRelevantPagesBasedTemplate(nb_pages=1))
query_expander_best_page_and_prompt = LLMQueryExpander(llm=llm, template=MostRelevantPagesPromptBasedTemplate(nb_pages=1))

# Hyde generator
hyde_generator = LLMHydeGenerator(llm=llm, template=HydeBasedTemplate())
hyde_prompt_generator = LLMHydeGenerator(llm=llm, template=HydePromptBasedTemplate())

## Configurations
configurations = []

## BASELINE ##
# configurations.append({
# "query_expander" : None,
# "classifier" : None,
# "threshold": None,
# "nb_pages_per_requests": None,
# "hyde_generator": None
# })

## 4 configurations ##
## 1) and 2) EXPANDER ON SEED QUERY 
# configurations.append({
# "query_expander" : query_expander_on_seed,
# "classifier" : None,
# "threshold": None,
# "hyde_generator": None
# })
# simple classifier : cosine similarity
# improved classifier : hyde_cos_sim 

## 3) What if we expand with best page ? -> EXPANDER ON BEST PAGE
# configurations.append({
# "query_expander" : query_expander_best_page,
# "classifier" : hyde_classifier,
# "hyde_generator": hyde_generator
# })
# 4) MAYBE IT'S BETTER WHEN USING A PROMPT ? -> EXPANDER ON BEST PAGE AND PROMPT
# configurations.append({
# "query_expander" : query_expander_best_page_and_prompt,
# "classifier" : hyde_classifier,
# "hyde_generator": hyde_prompt_generator
# })

#-> EXPANDER ON INITIAL QUERY AND PROMPT
configurations.append({
"query_expander" : query_expander_on_seed_and_prompt,
"classifier" : hyde_classifier,
"hyde_generator": hyde_prompt_generator
})

print(f'{len(configurations)} configurations to test')
##################################################################################
def get_query_expander_name(config):
    if config["query_expander"] is None : 
        query_expander_name = ''
    elif isinstance(config["query_expander"].template, SeedQueryBasedTemplate) :
        query_expander_name = 'SeedQueryBasedTemplate'
    elif isinstance(config["query_expander"].template, SeedQueryPromptBasedTemplate) :
        query_expander_name = 'SeedQueryPromptBasedTemplate'
    elif isinstance(config["query_expander"].template, MostRelevantPagesBasedTemplate) :
        query_expander_name = 'MostRelevantPagesBasedTemplate'
    elif isinstance(config["query_expander"].template, MostRelevantPagesPromptBasedTemplate) :
        query_expander_name = 'MostRelevantPagesPromptBasedTemplate'
    return(query_expander_name)

def get_classifier_name(config):
    if config["classifier"] is None : 
        classifier_name = ''
    elif isinstance(config["classifier"], SimilarityClassifier) :
        classifier_name = 'SimilarityClassifier'
    elif isinstance(config["classifier"], HydeSimilarityClassifier) :
        classifier_name = 'HydeSimilarityClassifier'
    return(classifier_name)

def get_hyde_generator_name(config):
    if config["hyde_generator"] is None : 
        hyde_generator_name = ''
    elif isinstance(config["hyde_generator"].template, HydeBasedTemplate) :
        hyde_generator_name = 'HydeBasedTemplate'
    elif isinstance(config["hyde_generator"].template, HydePromptBasedTemplate) :
        hyde_generator_name = 'HydePromptBasedTemplate'
    return(hyde_generator_name)

# Création des folders et lancement des crawlers
for i, config in enumerate(configurations, 1):
    query_expander_name = get_query_expander_name(config)
    classifier_name = get_classifier_name(config)
    hyde_generator_name = get_hyde_generator_name(config)

    if (query_expander_name, classifier_name, hyde_generator_name) == ('', '', ''):
        folder_name = 'baseline'
    else : 
        folder_name = f"{query_expander_name}_{classifier_name}_{hyde_generator_name}/"

    folder_path = base_output_dir + folder_name

    if not os.path.exists(folder_path):
        print(folder_name)
    
        # Lancer le crawler
        crawl_session = CrawlSession(session_name=folder_name, query=query, prompt=prompt)
        
        crawler_client = ClientCrawler(
            folder=folder_path,
            crawl_session=crawl_session,
            searcher=searcher,
            classifier=config["classifier"],
            query_expander=config["query_expander"],
            hyde_generator=config["hyde_generator"],
            seed_urls=[]
        )

        crawler_client.crawl()
        print('-----------------------------------------------')




