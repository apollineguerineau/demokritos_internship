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

    def search(self, filename, crawl_session, nb_results=None):
        query = crawl_session.current_query
        old_fetched_pages = crawl_session.fetched_pages

        query = query.replace(" AND ", "+AND+").replace(" OR ", "+OR+")
        query = re.sub(r'\s+', '+', query)

        arxiv_url ='http://export.arxiv.org/api/query?search_query=all:'
        search_url = arxiv_url + query

        data = urllib.request.urlopen(search_url + '&max_results=1')
        xml_content = data.read().decode('utf-8')
        namespaces = {'opensearch': 'http://a9.com/-/spec/opensearch/1.1/'}
        root = ET.fromstring(xml_content)
        total_results = int(root.find('opensearch:totalResults', namespaces).text)
        if not nb_results : 
            nb_results = total_results

        print(f'{total_results} papers for query {query}')

        new_candidate_pages = []
        data = urllib.request.urlopen(search_url + '&sortBy=relevance&sortOrder=descending')
        i=0
        while len(new_candidate_pages) < nb_results and i<total_results : 
            if i%10==0 : 
                data = urllib.request.urlopen(search_url + f'&start={i}&max_results={10}' '&sortBy=relevance&sortOrder=descending')
            xml_content = data.read().decode('utf-8')
            root = ET.fromstring(xml_content)
            fetched_pages =  root.findall('{http://www.w3.org/2005/Atom}entry')
                    
            for _ in range(len(fetched_pages)) : 
                    if len(new_candidate_pages) < nb_results : 
                        web_page = self.read_arxiv_page(fetched_pages[_])
                        if web_page : 
                            if web_page not in old_fetched_pages and web_page not in new_candidate_pages:
                                web_page.get_with_query = query
                                new_candidate_pages.append(web_page)
                                with open(filename, mode='a', newline='', encoding='utf-8') as csvfile:
                                    writer = csv.writer(csvfile)
                                    writer.writerow({
                                        'url': web_page.url,
                                        'title': web_page.title,
                                        'description': web_page.description,
                                        'publication_date': web_page.publication_date,
                                        'language': web_page.language,
                                        'notes': web_page.notes,
                                        'score': web_page.score,
                                        'get_with_query': web_page.get_with_query
                                        })
            i+=1
        return(new_candidate_pages)

    def read_arxiv_page(self, fetched_page) : 
        namespaces = {
            'opensearch': 'http://a9.com/-/spec/opensearch/1.1/',
            'arxiv': 'http://arxiv.org/schemas/atom'
        }
        url = fetched_page.find('{http://www.w3.org/2005/Atom}id').text
        title = fetched_page.find('{http://www.w3.org/2005/Atom}title').text
        description = fetched_page.find('{http://www.w3.org/2005/Atom}summary').text
        links = ''
        publication_date = fetched_page.find('{http://www.w3.org/2005/Atom}published').text
        authors = []
        for author in fetched_page.findall('{http://www.w3.org/2005/Atom}author'):
            name = author.find('{http://www.w3.org/2005/Atom}name').text
            affiliation = author.find('arxiv:affiliation', namespaces)
            affiliation_text = affiliation.text if affiliation is not None else ''
            authors.append({'name': name, 'affiliation': affiliation_text})
        journal = ''
        language = ''
        notes = ''
        page = Page(url, title, description, links, publication_date, authors, language, notes)
        return page