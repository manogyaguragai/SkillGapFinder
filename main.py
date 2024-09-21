import streamlit as st
import os
st.set_page_config(page_title="SkillGapFinder", layout="wide",page_icon=os.path.join("assets","logo_transparent.png"))
import tempfile
from utils import get_gap
from recommenderbot import project_recommender
from recommenderbot.flowchart import get_flowchart
from searchbot import research_bot
from ragbot import ragbot
from utils import filters
from helperfunctions import cv_upload_options



st.markdown("""
        <style>
               .block-container {
                    padding-top: 2rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)
st.markdown("""<h1 style='text-align: center; color: black;'>SkillGapFinder</h1>""", unsafe_allow_html=True)

with st.container():
    syllabus_upload = st.file_uploader("Upload your syllabus", type="pdf")
        
    cv_info = cv_upload_options()

    data = filters()

    bitton_col = st.columns([13, 0.9])

    if bitton_col[-1].button("Submit"):
        with st.spinner("**Processing**"):
            if not syllabus_upload:
                st.info("Please upload your syllabus")
                st.stop()
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(syllabus_upload.read())
                syllabus_path = temp_file.name
            
            if cv_info:
                with tempfile.NamedTemporaryFile(delete=False) as temp_file_cv:
                    temp_file_cv.write(cv_info.read())
                    cv_path = temp_file_cv.name
                data_from_file_cv = ragbot(path=cv_path)
                cv_resp = data_from_file_cv.response
                with st.expander("**Your Skills**", expanded=True):
                    st.write(cv_resp)

            else:
                cv_resp = None
            
            data_from_file_syllabus = ragbot(path=syllabus_path)
                
            search_results = research_bot(data)
            
            resource, urls = project_recommender(data)
            syllabus_response = data_from_file_syllabus.response
            response = get_gap(data_from_file=syllabus_response, web_results=search_results,cv_data=cv_resp)
            
            roadmap_url = get_flowchart(urls, data)
            


            with st.expander("**Course Overview**", expanded=True):
                st.write(syllabus_response)
            
            with st.expander("**Web Search Results**", expanded=False):
                st.write(search_results)
            
            with st.expander("**Identified Gap Between Your Curriculum and the Industry**", expanded=False):
                st.write(response)
            
            with st.expander("**Roadmap and Project Ideas**"):
                st.write(resource)
                st.markdown(f'[**View Detailed Roadmap here**]({roadmap_url})', unsafe_allow_html=True)
                    

