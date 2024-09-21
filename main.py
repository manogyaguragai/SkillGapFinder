import streamlit as st
import os
from utils import get_gap
from recommenderbot import recommender
from recommenderbot.flowchart import get_flowchart
st.set_page_config(page_title="SkillGapFinder", layout="wide",page_icon=os.path.join("assets","logo_transparent.png"))

from ragbot import ragbot
import tempfile
from utils import filters
cols = st.columns(3)

st.markdown("""<h1 style='text-align: center; color: black;'>SkillGapFinder</h1>""", unsafe_allow_html=True)
columns = st.columns([10,12])
with st.container(border=1):
    upload = st.file_uploader("Upload your syllabus", type="pdf")
    data  =filters()
    bitton_col = st.columns([13,0.9])
    if bitton_col[-1].button("Submit"):
        with st.spinner("**Processing**"):
            if upload:
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    temp_file.write(upload.read())
                    temp_file_path = temp_file.name

                data_from_file = ragbot(path=temp_file_path)
                # st.write(data_from_file)
                with st.expander("**Course Overview**",expanded=True):
                    st.write(data_from_file.response)
            
                try:
                    resource, urls = recommender(data)
                    response = get_gap(data_from_file=data_from_file,web_results=resource)
                    roadmap = get_flowchart(urls,data)
                    with st.expander("**Course/Industry Gap**",expanded=False):
                        st.write(response)

                    with st.expander("**Roadmap and Resources**"):
                        st.write(resource)
                        if roadmap:
                            st.image(roadmap)
                        
                        st.info("No roadmap found")
                except NameError:
                    st.info("Please upload your syllabus")
            else:
                st.info("Please upload your syllabus")