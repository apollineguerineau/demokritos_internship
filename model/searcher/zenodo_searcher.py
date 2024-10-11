from searcher.abstract_searcher import AbstractSearcher
from model.crawl_session import CrawlSession
import requests
from model.page import Page


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
        total_pages = int(fetched_result['hits']['total'])
        fetched_pages = fetched_result['hits']['hits']

        i=0
        new_candidate_pages = []
        while len(new_candidate_pages) < self.nb_results and i<24 :
            page = self.read_zenodo_page(fetched_pages[i])
            if page not in old_fetched_pages :
                new_candidate_pages.append(page)
            i+=1
        return(new_candidate_pages)

    def read_zenodo_page(self, fetched_page) : 
        url = fetched_page.get('doi_url', '')
        title = fetched_page['metadata'].get('title', '')
        description = fetched_page['metadata'].get('description', '')
        links = fetched_page.get('links', {})
        publication_date = fetched_page['metadata'].get('publication_date', '')
        authors = fetched_page['metadata'].get('creators', [])
        journal = fetched_page['metadata'].get('journal', '')
        language = fetched_page['metadata'].get('language', '')
        notes = fetched_page['metadata'].get('notes', '')
        page = Page(url, title, description, links, publication_date, authors, language, notes)
        return page





