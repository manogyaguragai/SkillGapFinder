from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.openai import OpenAI
import os
import tempfile

def ragbot(uploaded_file):
    if uploaded_file:
        
        query = "Give me detailed information about the knowledge, skills and programming languages provided in the given document."
        
        with tempfile.TemporaryDirectory() as tempdir:
            uploaded_file_path = os.path.join(tempdir, "uploaded_file.pdf")
            with open(uploaded_file_path, "wb") as f:
                f.write(uploaded_file.read())

            reader = SimpleDirectoryReader(input_dir=tempdir)
            print(reader)
            
            documents = reader.load_data()

            node_parser = SentenceSplitter()
    
            nodes = node_parser.get_nodes_from_documents(documents, show_progress=True)

            index = VectorStoreIndex(nodes)
            
            llm = OpenAI(model="gpt-4o-mini", temperature=0.00,)
            
            return index.as_query_engine(llm=llm).query(query).response

        