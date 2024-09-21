from llama_index.tools.duckduckgo import DuckDuckGoSearchToolSpec
from llama_index.readers.web import SimpleWebPageReader 
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import VectorStoreIndex
from llama_index.llms.openai import OpenAI


def search_for_jobs(areas_of_interest):
    tool_spec = DuckDuckGoSearchToolSpec()
    user_question = f"I am interested in {areas_of_interest}, what are the best ways to land a job as a beginner?"
    search_results = tool_spec.duckduckgo_full_search(query=user_question, max_results=5) 
    links = [item['href'] for item in search_results]

    docs = SimpleWebPageReader().load_data(links)

    valid_documents = [doc for doc in docs if doc.text]

    node_parser = SentenceSplitter(chunk_size=1024, chunk_overlap=100)
    nodes = node_parser.get_nodes_from_documents(valid_documents, show_progress=True)

    index = VectorStoreIndex(nodes)

    question = "Give me a detailed list of Job Description, Hiring Comapny, Salary and Job Requirements from all given documents."
    response = index.as_query_engine(llm=OpenAI(model="gpt-4o-mini",temperature=0.0)).query(question)
    return response

