import streamlit as st
import os
from utils import get_gap
from recommenderbot import recommender

st.set_page_config(page_title="SkillGapFinder", layout="wide",page_icon=os.path.join("assets","logo_transparent.png"))

from ragbot import ragbot
import tempfile
from utils import filters
cols = st.columns(3)
cols[0].image(os.path.join("assets","logo_transparent.png"),width=200)
# st.image(os.path.join("assets","logo_transparent.png"))
# with st.form(key="select_job_options"):
with st.container(border=1):
    upload = st.file_uploader("Upload your syllabus", type="pdf")
    data  =filters()
    bitton_col = st.columns([13,0.9])
    if bitton_col[-1].button("Submit"):
        if upload:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(upload.read())
                temp_file_path = temp_file.name

            data_from_file = ragbot(path=temp_file_path)
            with st.expander("**Course Overview**",expanded=True):
                    # st.write("")
                st.write(data_from_file.response)
                # wb_results = web_searcher(data_to_send)
        st.toast("Your response has been submitted")#We will replace this with function to do other stuff :)


# web_saerch = """"
# A mid-level data analyst in Nepal typically engages in the following key responsibilities and requirements, reflective of the evolving tech and data landscape within the region:

# ### Key Responsibilities:
# 1. Data Collection and Management:
#     - Collecting data from various sources including databases and digital platforms.
#     - Ensuring data quality and integrity through regular audits and updates.

# 2. Data Analysis:
#     - Conducting statistical and analytical studies on datasets.
#     - Identifying trends, patterns, and insights that inform business decisions.

# 3. Reporting and Visualization:
#     - Creating detailed reports and dashboards using tools like Tableau, Power BI, or Excel.
#     - Presenting data findings to stakeholders in a clear and actionable manner.

# 4. Collaboration:
#     - Working closely with cross-functional teams, such as IT, marketing, sales, and finance, to understand their data needs and deliver solutions.
#     - Collaborating with senior analysts and data scientists on complex projects.

# 5. Database Management:
#     - Managing and querying data from relational databases using SQL.
#     - Maintaining and updating data warehouses as needed.

# ### Skills Requirements:
# 1. Technical Skills:
#     - Proficiency in statistical software and tools such as R, Python, SAS, or SPSS.
#     - Advanced Excel skills including pivot tables, v-lookups, and macros.
#     - Strong SQL skills for querying and manipulating data in relational databases.

# 2. Analytical Skills:
#     - Strong analytical and problem-solving abilities.
#     - Ability to interpret complex data sets and convey findings in a coherent manner.

# 3. Communication Skills:
#     - Excellent verbal and written communication skills to present findings and make recommendations.
#     - Ability to translate technical data into understandable insights for non-technical stakeholders.

# 4. Attention to Detail:
#     - High attention to detail to ensure accuracy in data analysis and reporting.

# 5. Experience:
#     - Typically, 3-5 years of experience in a data analysis role.
#     - Experience with data visualization tools and software.

# ### Educational Requirements:
# 1. Degree:
#     - A bachelor’s degree in data science, statistics, mathematics, computer science, information management, or a related field.

# 2. Certifications (Preferred but not always required):
#     - Certifications in data analytics, such as Google Data Analytics Certification, Microsoft Certified: Data Analyst Associate, or other relevant certifications.

# ### Job Market Insights:
# - The demand for data analysts in Nepal is growing as more companies realize the importance of data-driven decision-making.
# - Sectors such as telecommunications, finance, healthcare, and e-commerce are prominent employers.
# - Remote work opportunities exist, allowing collaboration with international teams and clients.

# By combining technical expertise with strong analytical and communication skills, mid-level data analysts in Nepal play a crucial role in helping organizations leverage data for strategic advantages. The evolving tech scene in Nepal offers ample opportunities for growth and professional development in this field.
# """
try:
    resource, urls = recommender(data)
    response = get_gap(data_from_file=data_from_file,web_results=resource)

    st.write("Identified Gap")
    st.write(response)

    st.write("Flowchart and Resources")
    st.write(resource)
    st.write(urls)
except NameError:
    st.info("Please upload your syllabus")