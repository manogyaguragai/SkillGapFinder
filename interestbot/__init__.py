from llama_index.tools.duckduckgo import DuckDuckGoSearchToolSpec
from llama_index.readers.web import SimpleWebPageReader 
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import VectorStoreIndex
from llama_index.llms.openai import OpenAI


def search_for_jobs(areas_of_interest):
    tool_spec = DuckDuckGoSearchToolSpec()
    summaries =[]
    for interest in areas_of_interest:
        user_question= f"Jobs that involve {interest}"

        search_results = tool_spec.duckduckgo_full_search(query=user_question, max_results=2) 
        links = [item['href'] for item in search_results]

        docs = SimpleWebPageReader().load_data(links)

        valid_documents = [doc for doc in docs if doc.text]

        node_parser = SentenceSplitter()
        nodes = node_parser.get_nodes_from_documents(valid_documents)

        index = VectorStoreIndex(nodes)

        question = "Give me a summary of the given document."
        summaries.append( index.as_query_engine(llm=OpenAI(model="gpt-4o-mini",temperature=0.0)).query(question).response)
    print(summaries)
    return summaries

