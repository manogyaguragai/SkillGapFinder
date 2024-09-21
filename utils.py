
from llama_index.llms.openai import OpenAI
from prompt import PROMPT
import streamlit as st
llm = OpenAI(model="gpt-4",temperature=0.0)

def get_gap( data_from_file):
    web_results = """
    ### Key Responsibilities:
1. **Financial Record Keeping**: Accountants are responsible for maintaining accurate financial records for individuals, companies, or organizations. This includes managing ledgers, journals, and billing systems.
  
2. **Preparing Financial Statements**: They prepare essential financial documents such as balance sheets, profit and loss statements, and cash flow statements. 

3. **Budgeting and Forecasting**: Accountants often assist in budget preparation and help with financial forecasting to identify future financial trends.

4. **Tax Preparation and Compliance**: Ensuring compliance with local tax regulations, preparing tax returns, and identifying tax deductions are crucial parts of the job.

5. **Auditing**: Some positions may require involvement in auditing processes, both internal and external, to verify financial accuracy.

6. **Consultation and Financial Advice**: Accountants may also provide advice on financial management, investment strategies, and budgeting to clients or management.

7. **Use of Accounting Software**: Proficiency in accounting software and tools is often required, as many firms rely on technology for financial operations.

### Qualifications:
1. **Educational Requirement**: A bachelor’s degree in accounting, finance, or a related field is typically required. 
...
In summary, accountant job descriptions in Nepal for 2023 reflect a comprehensive set of skills and responsibilities, with a strong emphasis on compliance, accuracy, and the ability to adapt to technological advancements in the field. Aspiring accountants should focus on gaining relevant qualifications and acquiring skills that align with these job requirements.

    """
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

    levels_by_industry = {
        "IT": ["Intern", "Junior Developer", "Mid-Level Developer", "Senior Developer", "Tech Lead", "CTO"],
        "Education": ["Assistant Teacher", "Teacher", "Senior Teacher", "Principal", "Dean"],
        "HR": ["Intern", "HR Assistant", "HR Specialist", "HR Manager", "HR Director"],
        "Finance": ["Junior Analyst", "Analyst", "Senior Analyst", "Finance Manager", "CFO"],
        "Healthcare": ["Intern", "Resident", "Specialist", "Consultant", "Chief Medical Officer"],
        "Marketing": ["Marketing Intern", "Marketing Executive", "Marketing Manager", "Marketing Director", "CMO"],
        "Legal": ["Intern", "Junior Lawyer", "Associate Lawyer", "Senior Lawyer", "Partner"],
        "Engineering": ["Intern", "Junior Engineer", "Engineer", "Senior Engineer", "Engineering Manager"],
        "Journalism": ["Intern", "Junior Reporter", "Staff Writer", "Senior Reporter", "Editor-in-Chief"],
        "Demographic Journalism": ["Intern", "Junior Data Journalist", "Research Analyst", "Senior Journalist", "Chief Data Journalist"]
    }

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
        options=[None] + levels_by_industry.get(selected_industry, []),
        index=0
    )

    data_to_send = {
        "industry": selected_industry,
        "job": selected_job,
        "level": selected_level
    }
    return data_to_send 