import os
from dotenv import load_dotenv
import pandas as pd

from model.query_expansion.no_query_expander import NoQueryExpander
from model.query_expansion.llm_query_expander import LLMQueryExpander

from model.llm.openai_llm import OpenAILLM
from model.llm.hugging_face_llm import HuggingFaceLLM
from model.llm.ollama_llm import OllamaLLM

from model.llm.template.seed_query_based_template import SeedQueryBasedTemplate
from model.llm.template.current_query_based_template import CurrentQueryBasedTemplate

from model.searcher.zenodo_searcher import ZenodoSearcher
from model.sorter.random_sorter import RandomSorter
# from model.sorter.classifier.transformer_based_classifier import FineTunedClassifier
from model.sorter.classifier_sorter import ClassifierSorter
from model.client_crawler import ClientCrawler
from model.business_object.crawl_session import CrawlSession
from model.business_object.page import Page

from db.crawler_session_dao import CrawlSessionDAO
from model.stop_criteria.nb_relevant_stop_criteria import NbRelevantStopCriteria

load_dotenv()
ZENODO_ACCESS_TOKEN = os.getenv('ZENODO_TOKEN')
OPENAI_ACCESS_TOKEN = os.getenv('OPENAI_TOKEN')
HUGGINGFACE_ACCESS_TOKEN = os.getenv('HUGGINGFACE_TOKEN')

# 1. Choice of searcher
searcher = ZenodoSearcher(3, ZENODO_ACCESS_TOKEN)

# 2. Choice of sorter
sorter = RandomSorter()

# classifier_model = FineTunedClassifier(name='bert fine tuned', path_to_model='./fine_tuned_model', path_to_tokenizer='google-bert/bert-base-cased')
# sorter = ClassifierSorter(classifier_model=classifier_model)

# 3. Choice of query expansor
query_expander = NoQueryExpander()

# llm = OllamaLLM('llama3.2')
# template_script = 'Your task is to expand this request : {}. Please generate one additional term that might help retrieve more relevant results in a broader context. The goal is to give a synonym, a related term, or any other variation that could improve the search results. Your response must be only one term and the output must be in json format with key "related_term".'
# template = SeedQueryBasedTemplate(template_script)
# query_expander = LLMQueryExpander(llm, template)

# 4. Choice of initial parameters
name_session = 'test_llm_expansion'
query = 'alloy'
seed_pages = [Page(url='a url', title='a title', description='a description', links='some links', publication_date='11/10/24', authors='authors', language='eng', notes='a fake page just to try', score=1)]
crawl_session = CrawlSession(name_session, sorter, query_expander, searcher, query, seed_pages)
stop_criteria = NbRelevantStopCriteria(crawl_session, 20)

# Crawl
crawler = ClientCrawler(crawl_session, stop_criteria)
crawler.crawl()
