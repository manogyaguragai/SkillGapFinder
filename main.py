import streamlit as st

def display_career_options():
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

    to_process =  [selected_industry, selected_job, selected_level]

    to_ret = [i for i in to_process if i]

    return to_ret

selected_options = display_career_options()
