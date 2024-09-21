import streamlit as st
import os
st.set_page_config(page_title="SkillGapFinder", layout="wide",page_icon=os.path.join("assets","logo_transparent.png"))
import tempfile
from utils import get_gap
from recommenderbot import project_recommender
from recommenderbot.flowchart import get_flowchart
from searchbot import research_bot
from interestbot import search_for_jobs
from ragbot import ragbot
from utils import filters
from helperfunctions import  info_card_module
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

cols = st.columns(3)

st.markdown("""
            <h1 style='text-align: center; color: black;'>SkillGapFinder</h1>
            """, unsafe_allow_html=True)

st.markdown("""
            <h3 style='text-align: center; color: black;'> An AI-powered Web App for Finding Skill Gaps! </h3>
            """, unsafe_allow_html=True)

with st.container(border=True):
    syllabus_upload, cv_info = info_card_module()

columns = st.columns([10,12])
with st.container(border=1):

    
    
    # CV upload options
    
    # Additional filters or options
    data = filters()
    
    # Define the button column
    bitton_col = st.columns([13, 0.9])
    
    # Handle form submission
    if bitton_col[-1].button("Submit"):
        with st.spinner("**Processing**"):
            if syllabus_upload or cv_info:  # Ensure the app runs with either or both uploads
                syllabus_path, cv_path = None, None
                
                # Process syllabus upload
                if syllabus_upload:
                    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                        temp_file.write(syllabus_upload.read())
                        syllabus_path = temp_file.name
                
                # Process CV upload if available
                if cv_info:
                    with tempfile.NamedTemporaryFile(delete=False) as temp_file_cv:
                        temp_file_cv.write(cv_info.read())
                        cv_path = temp_file_cv.name
                
                try:
                    # Extract data from the syllabus using the RAG bot
                    if syllabus_path:
                        data_from_file = ragbot(path=syllabus_path)
                    
                    # Perform web search
                    search_results = research_bot(data)
                    
                    # Get project recommendations
                    resource, urls = project_recommender(data)
                    
                    # Identify skill gaps based on the syllabus (and CV if available)
                    response, percentage = get_gap(data_from_file=data_from_file, web_results=search_results, cv_data=cv_path)
                    
                    # Generate roadmap and project ideas
                    roadmap_url = get_flowchart(urls, data)
                    
                    # Display course overview
                    with st.expander("**Course Overview**", expanded=True):
                        st.write(data_from_file.response)
                    
                    # Display web search results
                    with st.expander("**Web Search Results**", expanded=False):
                        st.write(search_results)
                    
                    # Display identified skill gap
                    with st.expander("**Identified Gap Between Your Curriculum and the Industry**", expanded=False):
                        st.write(response)
                        if percentage:
                            st.write(percentage)
                            my_bar = st.progress(percentage/100, text="You Readiness Level")
                            my_bar.progress(percentage/100, text="You Readiness Level")

                    # Display roadmap and project ideas
                    with st.expander("**Roadmap and Project Ideas**"):
                        st.write(resource)
                        st.markdown(f'[**View Detailed Roadmap here**]({roadmap_url})', unsafe_allow_html=True)
                        
                except Exception as e:
                    st.error(f"An error occurred: {e}")
            else:
                st.info("Please upload your syllabus or CV")