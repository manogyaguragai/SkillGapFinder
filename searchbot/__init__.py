from llama_index.llms.openai import OpenAI
from llama_index.tools.duckduckgo import DuckDuckGoSearchToolSpec
from llama_index.readers.web import SimpleWebPageReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import VectorStoreIndex

def web_searcher(data_to_send):
  
  level = data_to_send['level'].lower()
  job = data_to_send.get('job')
  industry = data_to_send.get('industry')

  if level == 'intern':
    user_question = f'{job or industry} Internships in Nepal'
  else:
    user_question = f'{data_to_send["level"]} {job or industry} Jobs in Nepal'  
  
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
      
      # Ensure that each document has valid content
    valid_documents = [doc for doc in documents if doc.text is not None]
      
    if valid_documents:
      print("WEB CONTENT FETCHED:")
         
    else:
      print("No valid content was fetched from the provided URLs.")

  except Exception as e:
    print(f"Error fetching data: {e}")

  node_parser = SentenceSplitter(chunk_size=1024, chunk_overlap=100)
    
  nodes = node_parser.get_nodes_from_documents(valid_documents, show_progress=True)

  index = VectorStoreIndex(nodes)
      
  llm = OpenAI(model="gpt-4", temperature=0.00, system_prompt=
              """
              You are a career counsellor responsible for providing career guidance to students and showing the gap between academics and the selected industry.
              You must use only the information from the provided document as your knowledge base.
              You need to understand the document and give a detailed list of Job Description, Hiring Comapny, Salary and Job Requirements.
              Understand the job requirements from all documents and categorize them into "Technical Requirements" and "Non-Technical Requirements".
              Include as many requirements as possible and if there are more than 10 requirements, mention the core requirements first and label others as "Additional Requirements".
              You also need to properly format the reply making use of proper headings and units.
              Do not include any application deadlines and any other dates.
              Your goal is to assist the user by providing accurate, polite, and helpful responses based solely on the available product information.
              """
              )

  question = "Give me a detailed list of Job Description, Hiring Comapny, Salary and Job Requirements from all given documents."

  return(index.as_query_engine(llm=llm).query(question).response)
