import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime

from model.query_expansion.no_query_expander import NoQueryExpander
from model.query_expansion.llm_query_expander import LLMQueryExpander

from model.llm.openai_llm import OpenAILLM
from model.llm.hugging_face_llm import HuggingFaceLLM
from model.llm.ollama_llm import OllamaLLM

from model.llm.template.seed_query_based_template import SeedQueryBasedTemplate
from model.llm.template.current_query_based_template import CurrentQueryBasedTemplate

from model.searcher.zenodo_searcher import ZenodoSearcher
from model.sorter.random_sorter import RandomSorter
from model.sorter.classifier.transformer_based_classifier import TransformerBasedClassifier
from model.sorter.classifier_sorter import ClassifierSorter
from model.client_crawler import ClientCrawler
from model.business_object.crawl_session import CrawlSession
from model.business_object.page import Page
from model.business_object.get_seed_pages_from_csv import GetSeedPagesFromCsv

from db.crawler_session_dao import CrawlSessionDAO
from model.stop_criteria.nb_relevant_stop_criteria import NbRelevantStopCriteria

load_dotenv()

def setup_seed_pages(seed_pages_file) : 
    return(GetSeedPagesFromCsv(seed_pages_file).get_pages())
    
def setup_searcher(searcher_name, **args):
    if searcher_name=="ZenodoSearcher":
        try : 
            ZENODO_ACCESS_TOKEN = os.getenv('ZENODO_TOKEN')
            nb_pages_per_request = int(args['nb_pages_per_request'])
            return(ZenodoSearcher(nb_pages_per_request, ZENODO_ACCESS_TOKEN))
        except : 
            print('Pas de clé pour Zenodo')
            return(None)

def setup_sorter(sorter_name, **args):
    if sorter_name == 'RandomSorter' : 
        return(RandomSorter())
    
    elif sorter_name == 'ClassifierSorter' : 
        type_classifier = args['type_classifier']
        path_to_model = args['path_to_model']
        path_to_tokenizer = args['path_to_tokenizer']
        classifier_model = setup_classifier(type_classifier, path_to_model, path_to_tokenizer)
        return(ClassifierSorter(classifier_model))

def setup_classifier(type_classifier, path_to_model, path_to_tokenizer):
    if type_classifier == 'TransformerBasedClassifier' : 
        return(TransformerBasedClassifier(path_to_model, path_to_tokenizer))
    
def setup_query_expansor(expansor_name, **args): 
    if expansor_name == 'NoQueryExpander':
        return(NoQueryExpander())
    
    elif expansor_name == 'LLMQueryExpander':
        name_template = args['name_template']
        template_script = args['template_script']
        name_llm_framework= args['name_llm_framework']
        model = args['model']
        
        template = setup_template(name_template, template_script)
        llm = setup_LLM(name_llm_framework, model)

        return(LLMQueryExpander(llm, template))

def setup_template(name_template, template_script):
    if name_template == "SeedQueryBasedTemplate":
        return(SeedQueryBasedTemplate(template_script))
    elif name_template == "CurrentQueryBasedTemplate":
        return(CurrentQueryBasedTemplate(template_script))
    
def setup_LLM(name_llm_framework, model):
    if name_llm_framework == 'Ollama':
        return(OllamaLLM(model))
    elif name_llm_framework == 'HuggingFaceLLM':
        try : 
            HUGGINGFACE_ACCESS_TOKEN = os.getenv('HUGGINGFACE_TOKEN')
            return(HuggingFaceLLM(model, HUGGINGFACE_ACCESS_TOKEN))
        except : 
            print('Pas de clé pour HuggingFace trouvée, utilisation de Ollama')
            return(OllamaLLM(model))
        
    elif name_llm_framework == 'OpenAILLM':
        try : 
            OPENAI_ACCESS_TOKEN = os.getenv('OPENAI_TOKEN')
            return(OpenAILLM(model, OPENAI_ACCESS_TOKEN))
        except : 
            print('Pas de clé pour OpenAI trouvée, utilisation de Ollama')
            return(OllamaLLM(model))
        
def setup_stop_criteria(stop_criteria_name, **args):
    if stop_criteria_name=="NbRelevantStopCriteria":
        nb_relevant_pages = int(args['nb_relevant_pages'])
        return(NbRelevantStopCriteria(nb_relevant_pages))

def setup_crawling_session(session_name, sorter, query_expander, searcher, query, seed_pages) :
    return(CrawlSession(session_name, sorter, query_expander, searcher, query, seed_pages))

def setup_client_crawler(crawl_session, stop_criteria):
    return(ClientCrawler(crawl_session, stop_criteria))
