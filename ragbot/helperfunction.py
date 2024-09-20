from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.llms.openai import OpenAI
import os
import tempfile


def initialize_index(uploaded_file):
    with tempfile.TemporaryDirectory() as tempdir:
        uploaded_file_path = os.path.join(tempdir, "uploaded_file.pdf")
        with open(uploaded_file_path, "wb") as f:
            f.write(uploaded_file.read())

        reader = SimpleDirectoryReader(input_dir=tempdir)
        print(reader)
        documents = reader.load_data()

        index = VectorStoreIndex.from_documents(documents)
    
    return index

def query_index(index, query):
    query_engine = index.as_query_engine(llm=OpenAI(model="gpt-4o-mini",temperature=0.0,))
    response = query_engine.query(query)
    return response


