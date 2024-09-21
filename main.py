import streamlit as st
st.set_page_config(page_title="SkillGapFinder", layout="wide",page_icon=os.path.join("assets","logo_transparent.png"))

import os
import tempfile
from utils import get_gap
from recommenderbot import project_recommender
from recommenderbot.flowchart import get_flowchart
from searchbot import research_bot
from ragbot import ragbot
from utils import filters




cols = st.columns(3)

st.markdown("""<h1 style='text-align: center; color: black;'>SkillGapFinder</h1>""", unsafe_allow_html=True)
columns = st.columns([10,12])
with st.container(border=1):
    upload = st.file_uploader("Upload your syllabus", type="pdf")
    
    data  = filters()
    
    bitton_col = st.columns([13,0.9])
    
    if bitton_col[-1].button("Submit"):
        with st.spinner("**Processing**"):
            if upload:
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    temp_file.write(upload.read())
                    temp_file_path = temp_file.name
                
                try:
                    data_from_file = ragbot(path=temp_file_path)
                    
                    search_results = research_bot(data)
                    
                    resource, urls = project_recommender(data)
                    
                    response = get_gap(data_from_file=data_from_file,web_results=resource)
                    
                    
                    roadmap_img, roadmap_url = get_flowchart(urls,data)
                    
                    
                    with st.expander("**Course Overview**",expanded=True):
                        st.write(data_from_file.response)
                        
                    with st.expander("**Web Search Results**",expanded=False):
                        st.write(search_results)
 
                    with st.expander("**Identified Gap Between Your Curriculum and the Industry**",expanded=False):
                        st.write(response)

                    with st.expander("**Roadmap and Project Ideas**"):
                        st.write(resource)
                        st.markdown(f'[**View Detailed Roadmap here**]({roadmap_url})',unsafe_allow_html=True)
                        
                except Exception as e:
                    st.write(e)
                    # st.info("Please upload your syllabus")
            else:
                st.info("Please upload your syllabus")