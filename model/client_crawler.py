from model.business_object.crawl_session import CrawlSession
from db.crawler_session_dao import CrawlSessionDAO
import csv
from datetime import datetime

class ClientCrawler :
    def __init__(self, crawl_session, stop_criteria) :
        self.crawl_session = crawl_session
        self.stop_criteria = stop_criteria
        
    def crawl(self):
        CrawlSessionDAO().create_crawl_session(self.crawl_session, self.stop_criteria)
        pages_counter = len(self.crawl_session.fetched_pages)
        i=0 
        while not self.stop_criteria.is_reached(self.crawl_session) : 

            if i>0:
                start_expansion = datetime.now()
                #expand query
                new_query = self.crawl_session.query_expander.expand_query(self.crawl_session)
                self.crawl_session.current_query = new_query
                self.crawl_session.all_queries += '\n' + self.crawl_session.current_query
                end_expansion = datetime.now()
                duration_expansion = end_expansion - start_expansion
                print(f'duration of query expansion : {duration_expansion}')

            #get new pages
            start_fetching = datetime.now()
            new_fetched_pages = self.crawl_session.searcher.search(self.crawl_session.current_query, self.crawl_session.fetched_pages)
            end_fetching = datetime.now()
            duration_fetching = end_fetching - start_fetching
            print(f'duration of fetching : {duration_fetching}')

            #sort fetched pages
            start_sorting = datetime.now()
            sorted_fetched_pages = self.crawl_session.sorter.sort(self.crawl_session.fetched_pages, new_fetched_pages)
            self.crawl_session.fetched_pages = sorted_fetched_pages
            end_sorting = datetime.now()
            duration_sorting = end_sorting - start_sorting
            print(f'duration of sorting : {duration_sorting}')

            # Compte le nombre de nouvelles pages ajoutées
            pages_counter += len(new_fetched_pages)

            # Met à jour la session toutes les 10 nouvelles pages
            if pages_counter >= 10:
                CrawlSessionDAO().update_crawl_session(self.crawl_session)
                print(f"Session updated after {pages_counter} new pages.")
                pages_counter = 0  # Réinitialise le compteur

            print(f"{len(self.crawl_session.fetched_pages)} récupérés")
            i+=1
        CrawlSessionDAO().update_crawl_session(self.crawl_session)

    
    