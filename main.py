from model.searcher.arxiv_searcher import ArxivSearcher
import urllib
import re

searcher = ArxivSearcher()


query = 'inverse design AND "metal-organic frameworks"'
# query = 'LLM'

total = searcher.get_max_results(query)
print(total)




