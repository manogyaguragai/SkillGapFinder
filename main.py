import streamlit as st
from searchbot import web_searcher
from ragbot import ragbot

upload = st.file_uploader("Upload your syllabus", type="pdf")
st.write(ragbot(uploaded_file=upload))
columns = st.columns(3)

selected_industry = columns[0].selectbox(
    label="Choose your industry",
    options=["IT"]
)
selected_job = columns[1].selectbox(
    label="Choose your preferred job",
    options=[None,"Python developer","Backend developer","Frontend developer","Fullstack developer","Data analyst","UI/UX","Q/A","Product Manager"],index=0
)

selected_level = columns[2].selectbox(
    label="Choose your level preference",
    options=["Intern","Junior","Mid-Level","Senior"]
)

data_to_send = {
    "industry": selected_industry,
    "job": selected_job,
    "level": selected_level
}

st.write(web_searcher(data_to_send))