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

query = '''"Machine Learning" AND (diffusion OR diffusivity) AND (MOFs OR ZIFs OR "metal-organic frameworks" OR COFs OR "covalent-organic frameworks)'''
llm = OllamaLLM(model='llama3.2')
stop_criteria = DurationStopCriteria(maximum_duration=120)
searcher = ChemRxivSearcher()

#################################### PARAMETERS ####################################
nb_pages_per_request = [10, 50, 100]

# Classifier
sim_classifier = SimilarityClassifier(name_embed_model='intfloat/multilingual-e5-base')
threshold_sim = [0.84, 0.85, 0.86]

hyde_classifier = HydeSimilarityClassifier(name_embed_model='intfloat/multilingual-e5-base')
threshold_hyde = [0.84, 0.85, 0.86]

# Query expansor
template_expansion_on_seed = SeedQueryBasedTemplate()
template_expansion_best_page = MostRelevantPagesBasedTemplate(nb_pages=1)
query_expander_on_seed = LLMQueryExpander(llm=llm, template=template_expansion_on_seed)
query_expander_best_page = LLMQueryExpander(llm=llm, template=template_expansion_best_page)

# Hyde generator
template_hyde = HydeBasedTemplate()
hyde_generator = LLMHydeGenerator(llm=llm, template=template_hyde)

#####################################################################################

crawl_session = CrawlSession(session_name='test', query=query)

crawler_client = ClientCrawler(folder = "/Users/apollineguerineau/Documents/ENSAI/3A/Greece/internship/eval/test",
                               crawl_session=crawl_session, 
                               stop_criteria=stop_criteria,
                               searcher=searcher, 
                               nb_pages_per_request=10, 
                               threshold=0.8,
                               classifier=sim_classifier,
                               query_expander=query_expander_on_seed, 
                               hyde_generator=None,
                               seed_urls=[]
                               )

crawler_client.crawl()
print('Nombre de pages récupérées : ')
print(len(crawler_client.crawl_session.fetched_pages))



