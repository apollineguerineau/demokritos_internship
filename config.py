# script for LLM templates
MOSTRELEVANTBASED = """Your task is to expand the following search query based on 
                    additional information from a relevant page title. 
                    Start by analyzing the initial query and then consider how the title provided 
                    can enhance the context. Generate an improved query by adding one or more related 
                    terms, synonyms, or key variations that reflect a broader or more specific focus based
                    on both the original query and the page title. Your goal is to optimize the query for
                    retrieving more relevant search results. 
                    This is the initial query : {}.
                    And this is the relevant page title : {}. 
                    Please generate a new expanded boolean query that integrates these insights. The response must be in JSON format, with the key "expanded_query" and for value the suggested expansion. Just output the json."""
MOSTRELEVANT_PROMPT_BASED = """Your task is to expand the following search query based on 
                    additional information from a relevant page title. 
                    Start by analyzing the initial query and then consider how the title provided 
                    can enhance the context. Generate an improved query by adding one or more related 
                    terms, synonyms, or key variations that reflect a broader or more specific focus based
                    on both the original query and the page title. Your goal is to optimize the query for
                    retrieving more relevant search results. 
                    This is the initial query : {}. This is additional context to better understand the initial query : {}. 
                    And this is the relevant page title : {}. 
                    Please generate a new expanded boolean query that integrates these insights. The response must be in JSON format, with the key "expanded_query" and for value the suggested expansion. Just output the json."""
QUERYBASED = '''Your task is to expand the following search query. 
            Generate an improved query by adding one or more related terms, 
            synonyms, or key variations that reflect a broader or more specific focus based 
            on the original query. Your goal is to optimize the query for retrieving more relevant search results. 
            This is the initial query : {}. Please generate a new expanded boolean query. 
            The response must be in JSON format, with the key "expanded_query" and for value the suggested expansion. 
            Just output the json.'''
QUERY_PROMPT_BASED = '''Your task is to expand the following search query. 
            Generate an improved query by adding one or more related terms, 
            synonyms, or key variations that reflect a broader or more specific focus based 
            on the original query. Your goal is to optimize the query for retrieving more relevant search results. 
            This is the initial query : {}. And this is additional context to better understand the initial query : {}. Please generate a new expanded boolean query. 
            The response must be in JSON format, with the key "expanded_query" and for value the suggested expansion. 
            Just output the json.'''
HYDE = "Your task is to generate a research paper title and abstract based on a search query I will provide. The title should be precise, engaging, and clearly reflect the main topic. The abstract should provide a clear overview of the objectives, methodology, and implications of the research. Please output your response in json format with keys 'title' and 'abstract'. This is the search query : {}"
HYDE_PROMPT = "Your task is to generate a research paper title and abstract based on a search query and additional context I will provide. The title should be precise, engaging, and clearly reflect the main topic. The abstract should provide a clear overview of the objectives, methodology, and implications of the research. Please output your response in json format with keys 'title' and 'abstract'. This is the search query : {}. And this is the context : {}"
