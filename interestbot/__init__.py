from langchain.tools import DuckDuckGoSearchRun
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
def search_for_jobs(area_of_interest):

    prompt = """
    Given a Jumbled list of jobs in a unstructured format.
    Your task is to process the input into meaningful well formatted jobs. Include the job title, description, and requirements.
    {input}

    """
    prompot__ = PromptTemplate.from_template(prompt)  
    
    search = DuckDuckGoSearchRun()#Search Tool

    llm = ChatOpenAI(temperature=0.0,model="gpt-4o-mini")

    chain = prompot__|llm|StrOutputParser()

        

    return chain.invoke(input={"input":search.run(area_of_interest)}).replace("`","")
        