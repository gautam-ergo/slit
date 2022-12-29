import time
from typing import Any

import pandas as pd
import streamlit as st

from app.processor import process

user_text_input: list = []
file_specified: bool = False
input_df: Any = ""


def read_input(file):
    global file_specified
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
    file_specified = True
    return temp


def upload_input():
    global input_df, file_specified
    upload = st.button('Upload Input File', type='primary')
    holder = st.empty()
    with holder.container():
        if upload:
            file_specified = False
        if (upload or ('source' in st.session_state)) and not file_specified:
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
                st.info("Reading 'trainingdata_dev.csv' from '/main' at the directory root")
                input_df = read_input(file=r'trainingdata_dev.csv')

    if file_specified:
        holder.empty()
        process(input_df)
