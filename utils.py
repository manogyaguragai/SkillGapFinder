
from llama_index.llms.openai import OpenAI
from prompt import PROMPT
import streamlit as st
llm = OpenAI(model="gpt-4o-mini",temperature=0.0)

def get_gap( web_results,data_from_file):
    
    return llm.complete(PROMPT.format(curriculum=data_from_file, industry_standards=web_results)).text

def filters():
    columns = st.columns(3)
    jobs_by_industry = {
        "IT": ["Python Developer", "Backend Developer", "Frontend Developer", "Fullstack Developer", "Data Analyst", "UI/UX", "Q/A", "Product Manager"],
        "Education": ["Teacher", "Curriculum Developer", "Educational Technologist", "School Administrator", "Guidance Counselor"],
        "HR": ["HR Manager", "Recruiter", "Talent Acquisition Specialist", "HR Coordinator", "Employee Relations Manager"],
        "Finance": ["Financial Analyst", "Accountant", "Auditor", "Investment Banker", "Loan Officer", "Treasurer"],
        "Healthcare": ["Doctor", "Nurse", "Pharmacist", "Healthcare Administrator", "Medical Lab Technician"],
        "Marketing": ["Marketing Manager", "SEO Specialist", "Content Strategist", "Social Media Manager", "Brand Manager"],
        "Legal": ["Lawyer", "Paralegal", "Legal Advisor", "Legal Secretary", "Compliance Officer"],
        "Engineering": ["Mechanical Engineer", "Civil Engineer", "Electrical Engineer", "Chemical Engineer", "Project Engineer"],
        "Journalism": ["Reporter", "Editor", "Investigative Journalist", "News Anchor", "Freelance Journalist"],
        "Demographic Journalism": ["Data Journalist", "Demographic Analyst", "Investigative Reporter", "Research Journalist", "Fact-checker"]
    }

    levels_by_industry =["Intern","Entry Level", "Mid Level", "Senior Level"]

    selected_industry = columns[0].selectbox(
        label="Choose your industry",
        options=[None,"IT", "Education", "HR", "Finance", "Healthcare", "Marketing", "Legal", "Engineering", "Journalism", "Demographic Journalism"]
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