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

# Configuration de base
base_output_dir = "/Users/apollineguerineau/Documents/ENSAI/3A/Greece/internship/eval/test/"
query = '''"Machine Learning" AND (diffusion OR diffusivity) AND (MOFs OR ZIFs OR "metal-organic frameworks" OR COFs OR "covalent-organic frameworks)'''
llm = OllamaLLM(model='llama3.2')
stop_criteria = DurationStopCriteria(maximum_duration=120)
searcher = ChemRxivSearcher()

# Classifiers et leurs seuils
sim_classifier = SimilarityClassifier(name_embed_model='intfloat/multilingual-e5-base')
threshold_sim = 0.85

hyde_classifier = HydeSimilarityClassifier(name_embed_model='intfloat/multilingual-e5-base')
threshold_hyde = 0.902

# Query expansion configurations
query_expander_none = None
query_expander_on_seed = LLMQueryExpander(llm=llm, template=SeedQueryBasedTemplate())
query_expander_best_page = LLMQueryExpander(llm=llm, template=MostRelevantPagesBasedTemplate(nb_pages=1))

# Hyde generator
hyde_generator = LLMHydeGenerator(llm=llm, template=HydeBasedTemplate())

# Combinaisons possibles
query_expanders = [query_expander_none, query_expander_on_seed, query_expander_best_page]
classifiers_and_thresholds = [
    (None, None),  # Pas de classificateur
    (sim_classifier, threshold_sim),  # Similarity classifier
    (hyde_classifier, threshold_hyde),  # Hyde classifier
]
nb_pages_per_requests_options = [10, 50, 100]

# Initialisation des configurations
configurations = []

# Génération des configurations
for query_expander, (classifier, threshold) in product(query_expanders, classifiers_and_thresholds):
    if query_expander is None :
        # Cas particulier : seulement nb_pages_per_requests = 100
        nb_pages_per_requests = [100]
    else:
        # Tous les autres cas
        nb_pages_per_requests = nb_pages_per_requests_options
    
    for nb_pages in nb_pages_per_requests:
        config = {
            "query_expander": query_expander,
            "classifier": classifier,
            "threshold": threshold,
            "nb_pages_per_requests": nb_pages,
            "hyde_generator": hyde_generator if classifier == hyde_classifier else None,
        }
        configurations.append(config)
print(len(configurations))

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

    if not os.path.exists(folder_path) : 
    
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

