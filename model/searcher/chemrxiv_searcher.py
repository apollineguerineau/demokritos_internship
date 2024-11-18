from model.searcher.abstract_searcher import AbstractSearcher
import requests
from model.business_object.page import Page
import urllib.parse
import re
import csv

class ChemRxivSearcher(AbstractSearcher) : 
    def __init__(self):
        self.name = "ChemRxiv API"

    def get_max_results(self, query):
        url = "https://chemrxiv.org/engage/chemrxiv/public-api/v1/items?term=" + query
        data = requests.get(url + '&limit=1')
        total_results = data.json()['totalCount']
        return(total_results)
    
    def get_page(self, query, num_page):
        requests_url = "https://chemrxiv.org/engage/chemrxiv/public-api/v1/items?term=" + query + f'&skip={num_page}' + f'&sort=RELEVANT_DESC&limit={1}'
        data = requests.get(requests_url)
        data_page = data.json()['itemHits'][0]['item']
        page = self.read_chemrxiv_page(data_page)
        return(page)

    def read_chemrxiv_page(self, data_page) : 
        url = "https://chemrxiv.org/engage/chemrxiv/article-details/" + data_page.get('id', '')
        title = data_page.get('title', '')
        description = data_page.get('abstract', '')
        page = Page(url, title, description)
        return page