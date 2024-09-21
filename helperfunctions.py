import streamlit as st
from streamlit_card import card

def info_card_module():
    upload_curriculum, arrow1, upload_cv, arrow2, select_job = st.columns(5)
    
    with upload_curriculum:
        curriculum_card = card(
            title="Upload Curriculum",
            text="Upload Curriculum pdf Below",
            image="https://www.shutterstock.com/image-vector/study-programme-icon-vector-logotype-600nw-2248370371.jpg",
            styles={
                "card": {
                    "border-radius": "30px",
                    "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                    },
                "title": {
                    "text-shadow": "2px 2px 4px #000000",
                    },
                "text": {
                    "text-shadow": "2px 2px 4px #000000",
                    },
                }   
            )
    with arrow1:
        arrow1card = card(
            title="",
            text="",
            image="https://png.pngtree.com/png-vector/20190411/ourmid/pngtree-vector-forward-icon-png-image_925823.jpg"
        )
        
    with upload_cv:
        cv_card = card(
            title="Upload CV",
            text="Click on me if you have a CV",
            image="https://www.creativefabrica.com/wp-content/uploads/2021/06/13/CV-or-Resume-Icon-Graphics-13336606-1-1-580x376.jpg",
            styles={
                "card": {
                    "border-radius": "30px",
                    "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                    },
                "title": {
                    "text-shadow": "2px 2px 4px #000000",
                    },
                "text": {
                    "text-shadow": "2px 2px 4px #000000",
                    },
                }   
            )
    with arrow2:
        arrow2card = card(
            title=" ",
            text=" ",
            image="https://png.pngtree.com/png-vector/20190411/ourmid/pngtree-vector-forward-icon-png-image_925823.jpg"
        )
        
    with select_job:
        job_card = card(
            title="Select Job",
            text="Click on Me if You Don't know what Job you want!",
            image="https://www.creativefabrica.com/wp-content/uploads/2021/03/24/Job-search-icon-Graphics-9935352-1-1-580x386.jpg",
            styles={
                "card": {
                    "border-radius": "30px",
                    "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                    },
                "title": {
                    "text-shadow": "2px 2px 4px #000000",
                    },
                "text": {
                    "text-shadow": "2px 2px 4px #000000",
                    },
                }   
            )
                
    
    # return curriculum_card, cv_card, job_card

def cv_upload_options():
    columns = st.columns(3)
    if columns[0].checkbox("I have a CVer"):
        uploaded_file = st.file_uploader("Upload your CV", type="pdf")

        return uploaded_file
    
    if columns[1].checkbox("I don't know what Job I want!"):
        st.write("Lets Gather Your Interests.")
    
    return None