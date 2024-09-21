from llama_index.core import VectorStoreIndex
from llama_index.readers.file import PyMuPDFReader
from llama_index.llms.openai import OpenAI
loader = PyMuPDFReader()
LLM = OpenAI(model="gpt-4o-mini", temperature=0.0)

def ragbot(path):
  try:
    documents = loader.load(file_path=path)
    # print(f"{documents=}")
  except Exception as e:
    return f"Error loading document: {str(e)}"
    
  if not documents:
    return "No documents found or failed to load."

  query = """
  What technical and non-technical skills are mentioned or implied in the document?
  Mention any tools, languages, or relevant topics covered. 
  If none are mentioned, say 'No relevant skills or tools found.'
  """

  index = VectorStoreIndex.from_documents(documents,)
  # print(index)
  query_engine = index.as_query_engine(similarity_top_k=3, llm=LLM)
    
  response = query_engine.query(query)
  return response
