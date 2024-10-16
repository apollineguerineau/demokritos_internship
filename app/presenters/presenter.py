# presenter/presenter.py
from app.setup import *
from db.crawler_session_dao import CrawlSessionDAO

class CrawlerPresenter:
    def __init__(self, view, view_export):
        self.view = view
        self.view_export = view_export

    def get_all_sessions(self):
        # Use the DAO to get a list of all session names and their IDs
        return CrawlSessionDAO().get_list_session_name_and_id()

    def get_session_data_by_id(self, session_id):
        # Use the DAO to get the data of a session by its ID
        return CrawlSessionDAO().get_session_by_id(session_id)

    def configure_crawler(self):
        # get values from view
        # try : 
        session_name = self.view.get_session_name()
        query = self.view.get_query()
        seed_pages_file = self.view.get_seed_page_file()

        searcher_name = self.view.get_searcher_choice()
        nb_pages_per_request = self.view.get_nb_page_per_request()
        if not nb_pages_per_request : 
            nb_pages_per_request = 3
        args_searcher = {'nb_pages_per_request' : nb_pages_per_request}

        sorter_name = self.view.get_sorter_choice()
        type_classifier = self.view.get_classifier_choice()
        path_to_model = self.view.get_model_path()
        path_to_tokenizer = self.view.get_tokenizer_path()
        args_sorter = {'type_classifier' : type_classifier,
                    'path_to_model' : path_to_model,
                    'path_to_tokenizer' : path_to_tokenizer}

        expansor_name = self.view.get_query_expander_choice()
        name_template = self.view.get_template_choice()
        template_script = self.view.get_script()
        if not template_script:
            template_script = "Your task is to expand this request : {}. Please generate one additional term that might help retrieve more relevant results in a broader context. The goal is to give a synonym, a related term, or any other variation that could improve the search results. Your response must be only one term and the output must be in json format with key 'related_term'."
        name_llm_framework = self.view.get_framework()
        model = self.view.get_llm_model()
        args_expansor = {'name_template' : name_template,
                        'template_script' : template_script,
                        'name_llm_framework' : name_llm_framework, 
                        'model' : model}

        stop_criteria_choice = self.view.get_stop_criteria_choice()
        nb_relevant_pages = self.view.get_nb_relevant_pages()
        if not nb_relevant_pages : 
            nb_relevant_pages = 15
        args_stop_criteria = {'nb_relevant_pages' : nb_relevant_pages}
        # except : 
        #     self.view.show_message("One or more values not correct")

        # set up crawler
        if seed_pages_file :
            seed_pages = setup_seed_pages(seed_pages_file)
        else : 
            seed_pages = []
        searcher = setup_searcher(searcher_name, **args_searcher)
        sorter = setup_sorter(sorter_name, **args_sorter)
        query_expander = setup_query_expansor(expansor_name, **args_expansor)
        stop_criteria = setup_stop_criteria(stop_criteria_choice, **args_stop_criteria)
        crawl_session = setup_crawling_session(session_name, sorter, query_expander, searcher, query, seed_pages)
        crawler_client = setup_client_crawler(crawl_session, stop_criteria)

        self.view.show_message("Begin crawling process ?")
        try : 
            crawler_client.crawl()
            self.view.show_message("Crawling process over")
        except : 
            self.view.show_message("Something went wrong")


        

