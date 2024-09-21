from llama_index.llms.openai import OpenAI
from llama_index.tools.duckduckgo import DuckDuckGoSearchToolSpec
from llama_index.readers.web import SimpleWebPageReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import VectorStoreIndex
from bs4 import BeautifulSoup

def recommender(data_to_send):
  
  job = data_to_send.get('job')
  industry = data_to_send.get('industry')
  
  user_question = f'{job or industry} roadmap.sh'  
  
  print(f'USER QUESTION: \n\n {user_question}')
  
  tool_spec = DuckDuckGoSearchToolSpec()

  if user_question != "None":
    search_results = tool_spec.duckduckgo_full_search(query=user_question, max_results=2,region="np-np") 
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
      
      # Ensure that each document has valid content
    valid_documents = [doc for doc in documents if doc.text is not None]
      
    if valid_documents:
      print("WEB CONTENT FETCHED:")
         
    else:
      print("No valid content was fetched from the provided URLs.")

  except Exception as e:
    print(f"Error fetching data: {e}")
    
  soup = BeautifulSoup(valid_documents, 'html.parser')
  urls = []

  for link in soup.find_all('a', href=True):
      urls.append(link['href'])
      
  print(f'FETCHED URLS: \n\n {urls}')

  node_parser = SentenceSplitter(chunk_size=1024, chunk_overlap=100)
    
  nodes = node_parser.get_nodes_from_documents(valid_documents, show_progress=True)

  index = VectorStoreIndex(nodes)
      
  llm = OpenAI(model="gpt-4", temperature=0.00, system_prompt=
              """
              You are an expert career specialist who can make marvellous roadmap charts according to given job information.
              From the given document, extract information that will help you make a roadmap chart for the given job.
              You will be provided with a list of {urls} that contain links to certain resources that the user might need.
              Understand the URLs and recommend the most relevant information from them.
              """
              )

  question = "Give me prper roadmap flow chart and links to resources to learn the topics in the given documents."

  return(index.as_query_engine(llm=llm).query(question).response)
