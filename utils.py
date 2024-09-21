import re
from llama_index.llms.openai import OpenAI
from prompt import PROMPT
from interestbot import search_for_jobs
import streamlit as st
llm = OpenAI(model="gpt-4o-mini",temperature=0.0)

def get_gap(web_results,data_from_file,cv_data):
    
    response = llm.complete(PROMPT.format(curriculum=data_from_file, industry_standards=web_results, cv_file=cv_data)).text

    pattern = r"\d+(?=%)"  
    
    matches = re.search(pattern, response)

    if matches:
        percentage = int(matches.group()) 
    else:
        percentage = None

    return response, percentage

def dialog():
    with st.form("Interests"):
        interests = st.multiselect(
            label="What are your interests in the field of IT?",
            options=["Cybersecurity","Software Development","Data Science","Graphic Designing","Web Development","Artificial Intelligence","Machine Learning","Product Management","Product Design"],
            help="Select all that apply",   
        )

        if st.form_submit_button("Submit"):
            # return interests
            if not interests:
                st.error("Please select at least one interest")
                st.stop()
            
            with st.spinner("Fetching Results"):
                return search_for_jobs(interests)



def filters():
    columns = st.columns(3)

    jobs_by_industry = {
        "IT": ["Python Developer", "Backend Developer", "Frontend Developer", "Fullstack Developer", "Data Analyst", "UI/UX", "Q/A", "Product Manager", "Penetration Tester", "Software Development", "Data Science", "Automation", "Web Development", "Artificial Intelligence", "Machine Learning", "Product Management", "Product Design"],
    }

    levels_by_industry =["Entry Level", "Mid Level", "Senior Level"]

    selected_industry = columns[0].selectbox(
        label="Choose your industry",
        options=["IT"]
    )

    selected_job = columns[1].selectbox(
        label="Choose your preferred job",
        options=[None] + jobs_by_industry.get(selected_industry, []),
        index=0
    )

    selected_level = columns[2].selectbox(
        label="Choose your level preference",
        options=[None] + levels_by_industry,
        index=0
    )

    data_to_send = {
        "industry": selected_industry,
        "job": selected_job,
        "level": selected_level
    }
    return data_to_send 