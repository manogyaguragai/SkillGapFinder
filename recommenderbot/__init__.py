from langchain.tools import DuckDuckGoSearchRun
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

def project_recommender(data_to_send):
  
  job = data_to_send.get('job')
  industry = data_to_send.get('industry')
  
  user_question = f'{job or industry} project ideas github'  
  
  prompt = """
  Given a web search of the containing unstructured and jumbled data.
  Your task is to process the input into meaningful well formatted project ideas.
  Do not present any other information that is not mentioned in the given input.
  Input:
  {input}

  Output:
  ```
  processed_job_requirements
  ```
  """
  prompot__ = PromptTemplate.from_template(prompt)
    
  search = DuckDuckGoSearchRun()#Search Tool

  to_process = search.run(user_question)
  llm = ChatOpenAI(temperature=0.0,model="gpt-4o-mini")

  chain = prompot__|llm|StrOutputParser()

  return chain.invoke(input={"input":to_process}).replace("`","")
