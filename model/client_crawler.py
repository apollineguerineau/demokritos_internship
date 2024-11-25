from model.business_object.crawl_session import CrawlSession
import csv
import os
from datetime import datetime
import sys

class ClientCrawler :
    def __init__(self, folder, crawl_session, searcher, classifier=None, query_expander=None, hyde_generator=None, seed_urls=[]) :
        self.crawl_session = crawl_session
        self.searcher = searcher
        self.classifier = classifier
        self.query_expander = query_expander
        self.folder = folder
        self.create_folder_and_docs()
        self.start = None
        self.nb_queries = 1

        if classifier : 
            if classifier.require_hyde : 
                
                if not hyde_generator :
                    print('Need to choose hyde generator')
                else : 
                    try : 
                        hyde = hyde_generator.generate_hyde(self.crawl_session)
                        self.crawl_session.hyde = hyde
                    except : 
                        print('Error while generating hyde paper')
            self.crawl_session.start_time = datetime.now()
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
                'session_name', 'searcher', 'query_expansion', 'classifier', 'hyde', 'all_queries', 'nb_seed_pages','nb_fetched_pages', 'duration'
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
        self.start = datetime.now()

        #Get all pages with the first query
        print("Get all pages with the first query")
        print(f"nb pages for initial result : {self.searcher.get_max_results(self.crawl_session.current_query)}")
        new_pages = self.searcher.get_all_pages(self.crawl_session.current_query)
        print('------------------------------------------------')
        for page in new_pages : 
            if self.classifier : 
                score = self.classifier.attribute_score(self.crawl_session, page)
                page.score = score
            page.get_with_query=self.crawl_session.current_query
            self.crawl_session.add_fetched_page(page)
            self.write_page(self.folder + '/fetched_pages.csv', page)  
            self.printout()
        
        #Expand the query to get new pages
        if self.query_expander :
            nb_queries = 1
            while nb_queries < 10 : 
                self.printout()
            # while not self.stop_criteria.is_reached(self.crawl_session) : 
                new_query = self.query_expander.expand_query(self.crawl_session)
                if new_query != self.crawl_session.current_query : 
                    nb_queries+=1

                    self.crawl_session.current_query = new_query
                    self.crawl_session.all_queries += ';' + self.crawl_session.current_query
                    self.nb_queries += 1
                    self.printout()

                    new_pages = self.searcher.get_all_pages(self.crawl_session.current_query)
                    # new_pages = self.searcher.get_n_pages(self.crawl_session.current_query, start=0, end=self.nb_pages_per_request)
                    for page in new_pages : 
                        # if not self.stop_criteria.is_reached(self.crawl_session) :
                            if page and page not in self.crawl_session.fetched_pages :
                                if self.classifier : 
                                    score = self.classifier.attribute_score(self.crawl_session, page) 
                                    page.score = score
                                page.get_with_query=self.crawl_session.current_query
                                self.crawl_session.add_fetched_page(page)
                                self.write_page(self.folder + '/fetched_pages.csv', page)  
                                self.printout()

        end = datetime.now()
        duration = end - self.crawl_session.start_time
        self.write_crawl_session(self.folder + '/session_infos.csv', duration=duration)
        
    def printout(self):
        current_count = len(self.crawl_session.fetched_pages)
        actual = datetime.now()
        time_diff = actual - self.start
        minutes_elapsed = time_diff.total_seconds() // 60 
        sys.stdout.write(f"\rTime elapsed: {int(minutes_elapsed)} minutes - Pages Crawled: {current_count} - nb queries : {self.nb_queries}")
        sys.stdout.flush()

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
                             self.crawl_session.hyde, 
                             self.crawl_session.all_queries, 
                             len(self.crawl_session.seed_pages),
                             len(self.crawl_session.fetched_pages),
                             duration])