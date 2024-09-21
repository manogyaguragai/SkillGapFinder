import streamlit as st
from streamlit_card import card
from utils import dialog     
def info_card_module():
    upload_curriculum,upload_cv,select_job = st.columns(3)
    
    with upload_curriculum:
        curriculum_card = card(
            title="Upload Curriculum",
            text="Upload Curriculum pdf Below",
            image="https://www.shutterstock.com/image-vector/study-programme-icon-vector-logotype-600nw-2248370371.jpg",
            styles={
                "card": {
                    "border-radius": "10px",
                    "box-shadow": "0 0 30px rgba(0,0,0,0.5)",
                    },
                "title": {
                    "text-shadow": "2px 2px 4px #000000",
                    },
                "text": {
                    "text-shadow": "2px 2px 4px #000000",
                    },
                }   
            )
        
        
        syllabus_upload = st.file_uploader("Upload your syllabus", type="pdf")
    
    with upload_cv:
        cv_card = card(
            title="Upload CV",
            text="Click on me if you have a CV",
            image="https://www.creativefabrica.com/wp-content/uploads/2021/06/13/CV-or-Resume-Icon-Graphics-13336606-1-1-580x376.jpg",
            on_click=lambda: st.session_state.update({"cv_selected": True}),
            styles={
                "card": {
                    "border-radius": "10px",
                    "box-shadow": "0 0 30px rgba(0,0,0,0.5)",
                    },
                "title": {
                    "text-shadow": "2px 2px 4px #000000",
                    },
                "text": {
                    "text-shadow": "2px 2px 4px #000000",
                    },
                } ,
            )
        if st.session_state.get("cv_selected", False):
            uploaded_file = st.file_uploader("Upload your CV", type="pdf")
    
    with select_job:
        job_card = card(
            title="Select Job",
            text="Click on Me if You Don't know what Job you want!",
            image="https://www.creativefabrica.com/wp-content/uploads/2021/03/24/Job-search-icon-Graphics-9935352-1-1-580x386.jpg",
            on_click=lambda: st.session_state.update({"job_selected": True}),
            styles={
                "card": {
                    "border-radius": "10px",
                    "box-shadow": "0 0 30px rgba(0,0,0,0.5)",
                    },
                "title": {
                    "text-shadow": "2px 2px 4px #000000",
                    },
                "text": {
                    "text-shadow": "2px 2px 4px #000000",
                    },
                }   
            )
        st.write(" ")
        st.write(" ")
        # st.write(" ")
        if st.session_state.get("job_selected", False):
            user_interests = dialog()
            st.write(user_interests)
    
    try:
        return syllabus_upload,uploaded_file
    except:
        return [syllabus_upload,None]
