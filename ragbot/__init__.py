from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter, SentenceWindowNodeParser
from llama_index.core.postprocessor import MetadataReplacementPostProcessor
from llama_index.llms.openai import OpenAI
import os
import tempfile

def ragbot(uploaded_file):
  if uploaded_file:
    query = "Give me detailed information about all the courses, knowledge, skills and programming languages provided in the given document."
    
    with tempfile.TemporaryDirectory() as tempdir:
      uploaded_file_path = os.path.join(tempdir, "uploaded_file.pdf")
      with open(uploaded_file_path, "wb") as f:
        f.write(uploaded_file.read())

      reader = SimpleDirectoryReader(input_dir=tempdir)
      print(reader)
      
      documents = reader.load_data()
      
      node_parser = SentenceWindowNodeParser.from_defaults(
          window_size=3,
          window_metadata_key="window",
          original_text_metadata_key="original_text",
      )
      
      text_splitter = SentenceSplitter()

      # node_parser = SentenceSplitter()

      nodes = node_parser.get_nodes_from_documents(documents, show_progress=True)
      
      base_nodes = text_splitter.get_nodes_from_documents(documents)
      
      sentence_index = VectorStoreIndex(nodes)
      
      base_index = VectorStoreIndex(base_nodes)
      
      llm = OpenAI(model="gpt-4o-mini", temperature=0.00,)

      query_engine = sentence_index.as_query_engine(
            similarity_top_k=2,
            # the target key defaults to `window` to match the node_parser's default
            node_postprocessors=[
                MetadataReplacementPostProcessor(target_metadata_key="window")
            ],
            llm=llm
      )
      
      window_response = query_engine.query(query)

      # index = VectorStoreIndex(nodes)
            
      # return index.as_query_engine(llm=llm).query(query).response
      
      return window_response.response

        