from llama_index.core import VectorStoreIndex
from llama_index.readers.file import PyMuPDFReader
from llama_index.llms.openai import OpenAI

loader = PyMuPDFReader()
LLM = OpenAI(model="gpt-4",temperature=0.0)
def ragbot(path):
  documents = loader.load(file_path=path)
  query = """
  Based on the information provided in the document, what technical and non-technical skills can be expected to be learned or gained? 
  Please also mention any specific tools, languages, or relevant topics referenced in the document.
  If there are no relevant skills or tools mentioned, please state that there are no relevant skills or tools.
  """
  index = VectorStoreIndex.from_documents(documents)
  query_engine = index.as_query_engine(similarity_top_k=2, llm=LLM)

  
  response = query_engine.query(query)

  return response