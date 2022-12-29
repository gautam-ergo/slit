import time

import pandas as pd
import streamlit as st

from app.processor import process

user_text_input = []
proceed = False


def read_input(file):
    global proceed
    temp = pd.read_csv(file)
    fleeting_container = st.empty()
    with fleeting_container:
        if {'name', 'input'} - set(list(temp.columns)):
            st.error(
                f"Input file does not contain required columns:'input', 'name'",
                icon='❌'
            )
            st.info(f"Parsed columns - {set(list(temp.columns))}")
            st.stop()
        st.success(f"Parsed columns - {set(list(temp.columns))}")
        time.sleep(2)
        st.success("File upload success")
        time.sleep(2)
    fleeting_container.empty()
    proceed = True
    return temp


def upload_input():
    upload = st.button('Upload Input File', type='primary')
    holder = st.empty()
    with holder.container():
        if upload or ('source' in st.session_state):
            inp_source = st.selectbox("Select file source:", ['<select>', 'Github', 'Local'], key="source", index=0)
            if 'local' in inp_source.lower():
                upload_data = st.file_uploader(
                    label='Upload Data',
                    type='csv',
                    key='uploaded_data',
                    help='Recipe ingredient training data',
                )
                if upload_data:
                    input_df = read_input(file=upload_data)

            if 'git' in inp_source.lower():
                input_df = read_input(file=r'trainingdata_dev.csv')

    if proceed:
        holder.empty()
        process(input_df)
