from model.searcher.abstract_searcher import AbstractSearcher
from model.business_object.crawl_session import CrawlSession
import requests
from model.business_object.page import Page
import re
import urllib, urllib.request
import xml.etree.ElementTree as ET
import csv

class ArxivSearcher(AbstractSearcher) : 
    def __init__(self):
        self.name = "Arxiv API"

    def get_max_results(self, query):
        query = query.replace(" AND ", "+AND+").replace(" OR ", "+OR+")
        query = re.sub(r'\s+', '+', query)
        url = 'http://export.arxiv.org/api/query?search_query=all:' + query
        data = urllib.request.urlopen(url + '&max_results=1')
        xml_content = data.read().decode('utf-8')
        namespaces = {'opensearch': 'http://a9.com/-/spec/opensearch/1.1/'}
        root = ET.fromstring(xml_content)
        total_results = int(root.find('opensearch:totalResults', namespaces).text)
        return(total_results)
    
    def get_page(self, query, num_page):
        query = query.replace(" AND ", "+AND+").replace(" OR ", "+OR+")
        query = re.sub(r'\s+', '+', query)
        requests_url = 'http://export.arxiv.org/api/query?search_query=all:' + query + f'&start={num_page}&max_results={1}&sortBy=relevance&sortOrder=descending'
        data = urllib.request.urlopen(requests_url)
        xml_content = data.read().decode('utf-8')
        root = ET.fromstring(xml_content)
        data_page = root.findall('{http://www.w3.org/2005/Atom}entry')
        page = self.read_arxiv_page(data_page[0])
        return(page)

    def read_arxiv_page(self, fetched_page) : 
        namespaces = {
            'opensearch': 'http://a9.com/-/spec/opensearch/1.1/',
            'arxiv': 'http://arxiv.org/schemas/atom'
        }
        url = fetched_page.find('{http://www.w3.org/2005/Atom}id').text
        title = fetched_page.find('{http://www.w3.org/2005/Atom}title').text
        description = fetched_page.find('{http://www.w3.org/2005/Atom}summary').text
        page = Page(url, title, description)
        return page