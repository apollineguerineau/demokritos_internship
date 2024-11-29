from model.searcher.abstract_searcher import AbstractSearcher
from model.business_object.crawl_session import CrawlSession
from model.business_object.page import Page
import re
import urllib, urllib.request
import xml.etree.ElementTree as ET
import time
    
class ArxivSearcher(AbstractSearcher) : 
    def __init__(self):
        self.name = "Arxiv API"

    def transform_query(self,query):
        query =query.replace("-", ' ')
        query =query.replace("  ", ' ')
        query = query.replace(" ", "+")
        query = query.replace('"', "%22")
        return query

    def get_max_results(self, query):
        query = self.transform_query(query)
        url = 'http://export.arxiv.org/api/query?search_query=all:' + query + '&max_results=1'
        data = urllib.request.urlopen(url)
        xml_content = data.read().decode('utf-8')
        namespaces = {'opensearch': 'http://a9.com/-/spec/opensearch/1.1/'}
        root = ET.fromstring(xml_content)
        total_results = int(root.find('opensearch:totalResults', namespaces).text)
        return(total_results)

    def get_n_pages(self, query, start, end):
        wait_time = 3
        query = self.transform_query(query)
        nb_fetched = 0
        pages = []
        url = "http://export.arxiv.org/api/query?search_query=all:" + query
        for i in range(start, end+1, 100):
            if nb_fetched < end :
                requests_url = url + f'&start={i}&max_results={100}&sortBy=relevance&sortOrder=descending'
                data = urllib.request.urlopen(requests_url)
                xml_content = data.read().decode('utf-8')
                root = ET.fromstring(xml_content)
                data_pages = root.findall('{http://www.w3.org/2005/Atom}entry')
                for data_page in data_pages : 
                    if nb_fetched < end : 
                        page = self.read_arxiv_page(data_page)
                        pages.append(page)
                        nb_fetched+=1
                time.sleep(wait_time)
            else :
                break
        return(pages)

    def get_all_pages(self, query):
        total_results = self.get_max_results(query)
        if total_results >20000 : 
            total_results = 20000
        return(self.get_n_pages(query, 0, total_results))
    
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