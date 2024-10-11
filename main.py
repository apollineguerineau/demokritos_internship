import os
from dotenv import load_dotenv

from query_expansion import no_query_expander
from searcher import zenodo_searcher
from sorter import random_sorter
import client_crawler
from model import crawl_session, page

from db.crawler_session_dao import CrawlSessionDAO
from stop_criteria.nb_relevant_stop_criteria import NbRelevantStopCriteria

load_dotenv()
ACCESS_TOKEN = os.getenv('ZENODO_TOKEN')


name_session = 'second_try'
searcher = zenodo_searcher.ZenodoSearcher(3, ACCESS_TOKEN)
sorter = random_sorter.RandomSorter()
query_expander = no_query_expander.NoQueryExpander()
query = 'alloy'
seed_pages = [page.Page(url='a url', title='a title', description='a description', links='some links', publication_date='11/10/24', authors='authors', language='eng', notes='a fake page just to try')]
crawl_session = crawl_session.CrawlSession(name_session, sorter, query_expander, searcher, query, seed_pages)

save_path = '/Users/apollineguerineau/Desktop/Greece/internship/code/demokritos_internship/test_code/found_pages.csv'
stop_criteria = NbRelevantStopCriteria(crawl_session, 10)

crawler = client_crawler.ClientCrawler(crawl_session, save_path, stop_criteria)

crawler.crawl()

crawl_session_dao = CrawlSessionDAO()
crawl_session_dao.save_crawl_session(crawl_session, stop_criteria)