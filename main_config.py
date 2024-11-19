from model.client_crawler import ClientCrawler

from model.business_object.crawl_session import CrawlSession
from model.business_object.page import Page

from model.classifier.similarity_classifier import SimilarityClassifier
from model.classifier.hyde_similarity_classifier import HydeSimilarityClassifier

from model.llm.template.seed_query_based_template import SeedQueryBasedTemplate
from model.llm.template.most_relevant_pages_based import MostRelevantPagesBasedTemplate
from model.llm.template.hyde_based_template import HydeBasedTemplate

from model.llm.ollama_llm import OllamaLLM

from model.query_expansion.llm_query_expander import LLMQueryExpander

from model.hyde_generator.llm_hyde_generator import LLMHydeGenerator

from model.searcher.arxiv_searcher import ArxivSearcher
from model.searcher.chemrxiv_searcher import ChemRxivSearcher

from model.stop_criteria.duration_stop_criteria import DurationStopCriteria
from model.stop_criteria.nb_relevant_stop_criteria import NbRelevantStopCriteria
from itertools import product

from itertools import product
import os
import time
from tqdm import tqdm

from itertools import product
import os

# Configuration de base
# base_output_dir = "/home/onyxia/work/demokritos_internship/crawl_results/MOF/"
# query = '''"Machine Learning" AND (diffusion OR diffusivity) AND (MOFs OR ZIFs OR "metal-organic frameworks" OR COFs OR "covalent-organic frameworks)'''
base_output_dir = "/home/onyxia/work/demokritos_internship/crawl_results/RAG/"
query = '''RAG AND "code generation"'''
llm = OllamaLLM(model='llama3.2')
maximum_duration = 5
stop_criteria = DurationStopCriteria(maximum_duration=maximum_duration)
# searcher = ChemRxivSearcher()
searcher = ArxivSearcher()
nb_pages = 50

# Classifiers et leurs seuils
sim_classifier = SimilarityClassifier(name_embed_model='intfloat/multilingual-e5-base')
# threshold_sim = 0.85070133468372
threshold_sim = 0.8022592372014438

hyde_classifier = HydeSimilarityClassifier(name_embed_model='intfloat/multilingual-e5-base')
# threshold_hyde = 0.9087440326574849
threshold_hyde = 0.8817781945392197
# Query expansion configurations
query_expander_none = None
query_expander_on_seed = LLMQueryExpander(llm=llm, template=SeedQueryBasedTemplate())
query_expander_best_page = LLMQueryExpander(llm=llm, template=MostRelevantPagesBasedTemplate(nb_pages=1))

# Hyde generator
hyde_generator = LLMHydeGenerator(llm=llm, template=HydeBasedTemplate())

## Configurations
configurations = []

## NO EXPANDER
configurations.append({
"query_expander" : None,
"classifier" : None,
"threshold": None,
"nb_pages_per_requests": None,
"hyde_generator": None
})

configurations.append({
"query_expander" : None,
"classifier" : sim_classifier,
"threshold": threshold_sim,
"nb_pages_per_requests": None,
"hyde_generator": None
})

configurations.append({
"query_expander" : None,
"classifier" : hyde_classifier,
"threshold": threshold_hyde,
"nb_pages_per_requests": None,
"hyde_generator": hyde_generator
})

## EXPANDER ON SEED QUERY
configurations.append({
"query_expander" : query_expander_on_seed,
"classifier" : sim_classifier,
"threshold": threshold_sim,
"nb_pages_per_requests": nb_pages,
"hyde_generator": None
})

configurations.append({
"query_expander" : query_expander_on_seed,
"classifier" : hyde_classifier,
"threshold": threshold_hyde,
"nb_pages_per_requests": nb_pages,
"hyde_generator": hyde_generator
})

## EXPANDER ON BEST PAGES
configurations.append({
"query_expander" : query_expander_best_page,
"classifier" : sim_classifier,
"threshold": threshold_sim,
"nb_pages_per_requests": nb_pages,
"hyde_generator": None
})

configurations.append({
"query_expander" : query_expander_best_page,
"classifier" : hyde_classifier,
"threshold": threshold_hyde,
"nb_pages_per_requests": nb_pages,
"hyde_generator": hyde_generator
})

print(f'{len(configurations)} configurations to test')

# Création des folders et lancement des crawlers
for i, config in enumerate(configurations, 1):
    # Définir les noms dynamiques pour le folder
    expander_name = (
        "none"
        if config["query_expander"] is None
        else "seed_query_based"
        if isinstance(config["query_expander"].template, SeedQueryBasedTemplate)
        else "best_paper_based"
    )
    
    classifier_name = (
        "none"
        if config["classifier"] is None
        else "sim_cos"
        if config["classifier"] == sim_classifier
        else "hyde_sim_cos"
    )
    
    threshold_value = (
        "none"
        if config["threshold"] is None
        else f"{config['threshold']:.3f}"
    )
    
    folder_name = f"{expander_name}_{classifier_name}_thr_{threshold_value}_pages_{config['nb_pages_per_requests']}/"
    folder_path = base_output_dir + folder_name

    if not os.path.exists(folder_path):
        print(folder_name)
    
        # Lancer le crawler
        crawl_session = CrawlSession(session_name=f'test_config_{i}', query=query)
        
        crawler_client = ClientCrawler(
            folder=folder_path,
            crawl_session=crawl_session,
            stop_criteria=stop_criteria,
            searcher=searcher,
            nb_pages_per_request=config["nb_pages_per_requests"],
            threshold=config["threshold"],
            classifier=config["classifier"],
            query_expander=config["query_expander"],
            hyde_generator=config["hyde_generator"],
            seed_urls=[]
        )

        crawler_client.crawl()
        print('-----------------------------------------------')




