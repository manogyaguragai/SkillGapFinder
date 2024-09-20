from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.llms.openai import OpenAI
import os
import tempfile

def ragbot(uploaded_file):
    if uploaded_file:
        
        query = "What are the knowledge and skills provided in the given document?"
        
        with uploaded_file.TemporaryDirectory() as tempdir:
            uploaded_file_path = os.path.join(tempdir, "uploaded_file.pdf")
            with open(uploaded_file_path, "wb") as f:
                f.write(uploaded_file.read())

            reader = SimpleDirectoryReader(input_dir=tempdir)
            print(reader)
            
            documents = reader.load_data()

            index = VectorStoreIndex.from_documents(documents)
            
            llm = OpenAI(model="gpt-4o-mini", temperature=0.00, system_prompt=
              """
                As an AI, your task is to act as a curriculum expert. 
                Analyze the provided document, which contains curriculum information from a formal teaching institution. 
                Identify and recognize the knowledge and skills a student is expected to learn from this curriculum.
              """
              )
            
            return index.as_query_engine(llm=llm).query(query).response

        