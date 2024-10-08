from llama_index.llms.openai import OpenAI
from llama_index.tools.duckduckgo import DuckDuckGoSearchToolSpec
from llama_index.readers.web import SimpleWebPageReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import VectorStoreIndex
from bs4 import BeautifulSoup


def project_recommender(data_to_send):
  
  job = data_to_send.get('job')
  industry = data_to_send.get('industry')
  
  user_question = f'{job or industry} project ideas github'  
  
  print(f'USER QUESTION: \n\n {user_question}')
  
  tool_spec = DuckDuckGoSearchToolSpec()

  if user_question != "None":
    search_results = tool_spec.duckduckgo_full_search(query=user_question, max_results=5,region="np-np") 
  else:
    search_results = "None"

  print("Search Results Fetched")
  print(search_results)

  try:
    urls = [item['href'] for item in search_results]
  except:
    urls = []

  print("URL LIST EXTRACTED")
  print(urls)

  try:
      # Fetch data from URLs using TrafilaturaWebReader
    documents = SimpleWebPageReader().load_data(urls)
    print("DOCUMENTS FETCHED")
    # print(documents)
      
      # Ensure that each document has valid content
    valid_documents = [doc for doc in documents if doc.text is not None]
    print("VALID DOCUMENTS FETCHED")
    # print(valid_documents)
      
    if valid_documents:
      print("WEB CONTENT FETCHED:")
      
      all_text = " ".join([doc.text for doc in valid_documents])
      soup = BeautifulSoup(all_text, 'html.parser')
      
      urls2 = []
      for link in soup.find_all('a', href=True):
        urls2.append(link['href'])
        
         
    else:
      print("No valid content was fetched from the provided URLs.")

  except Exception as e:
    print(f"Error fetching data: {e}")
    
      
  print(f'FETCHED URLS: \n\n {urls2}')

  node_parser = SentenceSplitter(chunk_size=1024, chunk_overlap=100)
    
  nodes = node_parser.get_nodes_from_documents(valid_documents, show_progress=True)

  index = VectorStoreIndex(nodes)
      
  llm = OpenAI(model="gpt-4o-mini", temperature=0.00, system_prompt=
              """
              You are an expert career specialist who can recommend excellent projects according to given job information.
              Identify the job and industry provided in the given document.
              Extract key information about project ideas that can be implemented to get more skills on the identified job.
              Also provide a detailed roadmap to learn the topics in proper order.
              """
              )

  question = "Give me a detailed list of projects to help gain more skills on the identified job. Also provide a detailed roadmap to learn the topics"

  return(index.as_query_engine(llm=llm).query(question).response, urls2)
