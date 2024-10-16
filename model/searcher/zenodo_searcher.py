from model.searcher.abstract_searcher import AbstractSearcher
from model.business_object.crawl_session import CrawlSession
import requests
from model.business_object.page import Page
import re

class ZenodoSearcher(AbstractSearcher) : 
    def __init__(self, nb_results, token):
        self.token = token
        self.nb_results = nb_results
        self.name = f"Zenodo API, {nb_results} pages per request"

    def search(self, query, old_fetched_pages):
        response = requests.get('https://zenodo.org/api/records',
                    params={'q': query,
                            'access_token': self.token})
        fetched_result = response.json()
        total_results = fetched_result['hits']['total']

        new_candidate_pages = []
        i=1
        while len(new_candidate_pages) < self.nb_results and i<total_results : 
            response = requests.get('https://zenodo.org/api/records',
                                    params={'q': query,
                                            'access_token': self.token,
                                            'page':i})
            fetched_result = response.json()
            fetched_pages = fetched_result['hits']['hits']
        
            j=0
            while len(new_candidate_pages) < self.nb_results and j<len(fetched_pages):
                web_page = self.read_zenodo_page(fetched_pages[i])
                if web_page not in old_fetched_pages and web_page not in new_candidate_pages:
                    new_candidate_pages.append(web_page)
                j+=1
            
            i+=1
        return(new_candidate_pages)
    
    def remove_tags(self, text):
        if type(text)==str : 
            clean = re.sub(r'<.*?>', '', text)  # Supprime tout ce qui est entre < et >
            return clean
        else : 
            return('')

    def read_zenodo_page(self, fetched_page) : 
        url = fetched_page.get('doi_url', '')
        title = fetched_page['metadata'].get('title', '')
        description = self.remove_tags(fetched_page['metadata'].get('description', ''))
        links = fetched_page.get('links', {})
        publication_date = fetched_page['metadata'].get('publication_date', '')
        authors = fetched_page['metadata'].get('creators', [])
        journal = fetched_page['metadata'].get('journal', '')
        language = fetched_page['metadata'].get('language', '')
        notes = self.remove_tags(fetched_page['metadata'].get('notes', ''))
        page = Page(url, title, description, links, publication_date, authors, language, notes)
        return page





