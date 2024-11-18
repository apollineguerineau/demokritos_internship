from model.business_object.crawl_session import CrawlSession
import csv
import os
from datetime import datetime

class ClientCrawler :
    def __init__(self, folder, crawl_session, stop_criteria, searcher, nb_pages_per_request=100, threshold=0.8, classifier=None, query_expander=None, hyde_generator=None, seed_urls=[]) :
        self.crawl_session = crawl_session
        self.stop_criteria = stop_criteria
        self.nb_pages_per_request = nb_pages_per_request
        self.threshold = threshold
        self.searcher = searcher
        self.classifier = classifier
        self.query_expander = query_expander
        self.folder = folder
        self.create_folder_and_docs()

        if classifier : 
            if classifier.require_hyde : 
                if not hyde_generator :
                    print('Need to choose hyde generator')
                else : 
                    print('generation of hyde paper')
                    try : 
                        hyde = hyde_generator.generate_hyde(self.crawl_session)
                        self.crawl_session.hyde = hyde
                    except : 
                        print('Error while generating hyde paper')

         # for url in seed_urls : 
        #     page = self.searcher.get_page_url(url)
        #     page.is_seed=True
        #     if classifier : 
        #         page.score = self.classifier.attribute_score(self.crawl_session, page)
        #     self.crawl_session.add_fetched_page(page)
        #     self.write_page(self.folder + 'fetched_pages.csv', page)

    def create_folder_and_docs(self):
        os.makedirs(self.folder, exist_ok=True)

        with open(self.folder + '/session_infos.csv', mode='w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'session_name', 'searcher', 'query_expansion', 'classifier', 'threshold', 'nb_pages_per_request', 'stop_criteria', 'hyde', 'all_queries', 'nb_seed_pages','nb_fetched_pages', 'duration'
            ]
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)
        
        with open(self.folder + '/fetched_pages.csv', mode='w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'url', 'title', 'description','score', 'get_with_query', 'time_fetch', 'is_seed'
            ]
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)

       

    def crawl(self):
        i=0 
        while not self.stop_criteria.is_reached(self.crawl_session) : 
            if self.query_expander :
                if i>0:
                    #expand query
                    print('--- query expansion ---')
                    new_query = self.query_expander.expand_query(self.crawl_session)
                    self.crawl_session.current_query = new_query
                    self.crawl_session.all_queries += ';' + self.crawl_session.current_query

            max_results = self.searcher.get_max_results(self.crawl_session.current_query)
            nb_new_pages = 0
            j=0
            while j<max_results-1 and nb_new_pages<self.nb_pages_per_request and not self.stop_criteria.is_reached(self.crawl_session) :
                page = self.searcher.get_page(self.crawl_session.current_query, num_page=j)
                # if page.url not in [fetched_page.url for fetched_page in self.crawl_session.fetched_pages] : 
                if page not in self.crawl_session.fetched_pages :
                    print(j)
                    print(True)
                    page.get_with_query=self.crawl_session.current_query
                    if self.classifier : 
                        score = self.classifier.attribute_score(self.crawl_session, page)
                        if score >= self.threshold : 
                            page.score = score
                            self.crawl_session.add_fetched_page(page)
                            self.write_page(self.folder + '/fetched_pages.csv', page)
                            nb_new_pages+=1   
                            print(f'{nb_new_pages} added')
                    else : 
                        self.crawl_session.add_fetched_page(page)
                        self.write_page(self.folder + '/fetched_pages.csv', page)
                        nb_new_pages+=1   
                        print(f'{nb_new_pages} added')
                j += 1
            i +=1 
        end = datetime.now()
        duration = end - self.crawl_session.start_time
        self.write_crawl_session(self.folder + '/session_infos.csv', duration=duration)

    def write_page(self, filename, page):
        if page.is_seed : 
            time_fetching = None
        else : 
            time_fetching = datetime.now()
        with open(filename, mode='a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([page.url,
                            page.title,
                            page.description,
                            page.score,
                            page.get_with_query,
                            time_fetching,
                            page.is_seed])

    def write_crawl_session(self, filename, duration):
        if self.query_expander : 
            name_expander = self.query_expander.name
        else : 
            name_expander = 'no expansion'
        if self.classifier : 
            name_classifier = self.classifier.name
        else : 
            name_classifier = 'no classifier'
        with open(filename, mode='a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([self.crawl_session.session_name, 
                             self.searcher.name, 
                             name_expander, 
                             name_classifier, 
                             self.threshold, 
                             self.nb_pages_per_request, 
                             self.stop_criteria.name, 
                             self.crawl_session.hyde, 
                             self.crawl_session.all_queries, 
                             len(self.crawl_session.seed_pages),
                             len(self.crawl_session.fetched_pages),
                             duration])
    