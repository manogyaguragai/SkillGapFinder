import streamlit as st

def cv_upload_options():
    columns = st.columns(3)
    if columns[0].checkbox("I have a CV"):
        uploaded_file = st.file_uploader("Upload your CV", type="pdf")

        return uploaded_file
    
    return None