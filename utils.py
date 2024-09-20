
from llama_index.llms.openai import OpenAI
from prompt import PROMPT

llm = OpenAI(model="gpt-4o-mini",temperature=0.0)

def get_gap(web_results, data_from_file):
    return llm.complete(PROMPT.format(curriculum=web_results, industry_standards=data_from_file)).text

