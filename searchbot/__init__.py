from langchain.tools import DuckDuckGoSearchRun
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
def web_search(user_input): 
    level = user_input.get('level')
    job = user_input.get('job')
    industry = user_input.get('industry')
    prompt = """
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

                If the basic requirements like education, experience, skills, etc. are not mentioned, try to generate them.

    Input:
    {input}

    """
    prompot__ = PromptTemplate.from_template(prompt)
    user_question = f'{level} {job or industry} jobs in Nepal'  
    
    search = DuckDuckGoSearchRun()#Search Tool

    to_process = search.run(user_question)
    llm = ChatOpenAI(temperature=0.0,model="gpt-4o-mini")

    chain = prompot__|llm|StrOutputParser()

    return chain.invoke(input={"input":to_process}).replace("`","")
