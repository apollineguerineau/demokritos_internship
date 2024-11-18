# script for LLM templates
MOSTRELEVANTBASED = 'Your task is to expand the following search query based on additional information from three relevant page titles. Start by analyzing the initial query and then consider how the titles provided can enhance the context. Generate an improved query by adding one or more related terms, synonyms, or key variations that reflect a broader or more specific focus based on both the original query and the page titles. Your goal is to optimize the query for retrieving more relevant search results. This is the initial query : {}. And this is the three relevant page titles : {}. Please generate a new expanded boolean query that integrates these insights. The response must be in JSON format, with the key "expanded_query" and for value the suggested expansion. Just output the json.'
QUERYBASED = '''Your task is to expand the following search query. 
            Generate an improved query by adding one or more related terms, 
            synonyms, or key variations that reflect a broader or more specific focus based 
            on the original query. Your goal is to optimize the query for retrieving more relevant search results. 
            This is the initial query : {}. Please generate a new expanded boolean query. 
            The response must be in JSON format, with the key "expanded_query" and for value the suggested expansion. 
            Just output the json.'''
HYDE = "Your task is to generate a research paper title and abstract based on a search query I will provide. The title should be precise, engaging, and clearly reflect the main topic. The abstract should provide a clear overview of the objectives, methodology, and implications of the research. Please output your response in json format with keys 'title' and 'abstract'. This is the search query : {}"
