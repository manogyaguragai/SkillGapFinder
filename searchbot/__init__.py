from llama_index.llms.openai import OpenAI
from llama_index.tools.duckduckgo import DuckDuckGoSearchToolSpec
from llama_index.readers.web import SimpleWebPageReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import VectorStoreIndex

def web_search(user_input): 
    level = user_input.get('level')
    job = user_input.get('job')
    industry = user_input.get('industry')
  
    user_question = f'{level} {job or industry} jobs in Nepal'  
    
    tool_spec = DuckDuckGoSearchToolSpec()
    
    if user_input:
        search_results = tool_spec.duckduckgo_full_search(query=user_question, max_results=5) 
    else:
        print("No valid user input provided.")
        return "None"

    print("Search Results Fetched")
    print(search_results)

    # Ensure search_results is a list of dictionaries
    try:
        urls = [item['href'] for item in search_results if isinstance(item, dict) and 'href' in item]
    except Exception as e:
        print(f"Error extracting URLs: {e}")
        urls = []

    print("URL LIST EXTRACTED")
    print(urls)

    if not urls:
        print("No URLs found.")
        return "No URLs found."

    try:
        documents = SimpleWebPageReader().load_data(urls)
        print("DOCUMENTS FETCHED")
        
        valid_documents = [doc for doc in documents if doc.text is not None]
        print("VALID DOCUMENTS FETCHED")

    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

    node_parser = SentenceSplitter(chunk_size=1024, chunk_overlap=100)
    
    nodes = node_parser.get_nodes_from_documents(valid_documents, show_progress=True)

    index = VectorStoreIndex(nodes)
        
    llm = OpenAI(model="gpt-4o-mini", temperature=0.00, system_prompt=
                  """
                  You are an expert career specialist who can understand what job descriptions and requirements.
                  Identify all the jobs and industries provided in the given document.
                  From the available information extract the following:
                    - Job title,
                    - Job description,
                    - Job requirements,
                    - Programming language and tools used.
                    If these points aren't mentioned, do not write about them.
                  Do not present any other information that is not mentioned in the given document.
                  Present your outputs in a structured manner.

                  """
                  )

    question = "Give me a detailed list of requirements, salary range, job description and other key information for the jobs from the given document."

    return index.as_query_engine(llm=llm).query(question).response