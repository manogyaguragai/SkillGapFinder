from llama_index.llms.openai import OpenAI
from llama_index.tools.duckduckgo import DuckDuckGoSearchToolSpec
from llama_index.readers.web import SimpleWebPageReader
from llama_index.core import PromptTemplate
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import VectorStoreIndex

def web_searcher(filters):
  user_question=f'hello'
  print(f'USER QUESTION: \n\n {user_question}')
  tool_spec = DuckDuckGoSearchToolSpec()

  if user_question != "None":
    search_results = tool_spec.duckduckgo_full_search(query=user_question, max_results=5) 
  else:
    search_results = "None"

  st.subheader("Search Results Fetched")
  st.write(search_results)

  try:
    urls = [item['href'] for item in search_results]
  except:
    urls = []

  st.subheader("URL LIST EXTRACTED")
  st.write(urls)

  try:
      # Fetch data from URLs using TrafilaturaWebReader
      documents = SimpleWebPageReader().load_data(urls)
      
      # Ensure that each document has valid content
      valid_documents = [doc for doc in documents if doc.text is not None]
      
      if valid_documents:
          st.write("WEB CONTENT FETCHED:")
          # for doc in valid_documents:
          #     with st.container(border=True):
          #       st.write(doc)
      else:
          st.write("No valid content was fetched from the provided URLs.")

  except Exception as e:
      st.write(f"Error fetching data: {e}")
      
  custom_prompt = PromptTemplate(
    """
      You are tasked with extracting information about jobs from the provided document. 
      The document contains job descriptions, requirements, salary information, and various other technical details. 
      Your task is to provide a brief overview of the job description and focus primarily on elaborating the job requirements.
      It is crucial that you strictly stick to the information present in the document and do not make any assumptions or hallucinate additional details.
      Present the requirements as clearly and thoroughly as possible without adding any extraneous information.
      Refined job description
      """
      )

  node_parser = SentenceSplitter(chunk_size=1024, chunk_overlap=100)
    
  nodes = node_parser.get_nodes_from_documents(valid_documents, show_progress=True)

  index = VectorStoreIndex(nodes)
      
  # Settings.llm = OpenAI(model="gpt-4o-mini", temperature=0.0)

  # query_engine = index.as_query_engine(
          # text_qa_template=custom_prompt
      # )
      
  llm = OpenAI(model="gpt-4o-mini", temperature=0.00, system_prompt=
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
  response = index.as_query_engine(llm=llm).query(question)
  st.write(response.response)

  # refined_descriptions = []
  # for doc in valid_documents:
  #       # st.write(doc)
  #       response = query_engine.query(f"Extract and refine the job description, company name, salary and requirements from the following document: {doc}")
  #       st.write(f'RESPONSE')
  #       st.write(response.response)
        # refined_descriptions.append({
        #     'url': doc.metadata['url'],
        #     'refined_description': response.response
        # })

  # for job in refined_descriptions:
  #     with st.container(border=True):
  #       st.write(f"URL: {job['url']}")
  #       st.write(f"Refined Description: {job['refined_description']}")
  #       st.write("-" * 50)