from helperfunction import initialize_index, query_index
import streamlit as st
def ragbot(uploaded_file,query):
    if uploaded_file:
        with st.spinner("Processing PDF..."):
            index = initialize_index(uploaded_file)
            st.success("PDF processed and indexed successfully!")
        response = query_index(index, query)

        st.write(response.response)
