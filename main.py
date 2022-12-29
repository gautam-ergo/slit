import streamlit as st

from app.uploader import upload_input


def init():
    if 'selected' not in st.session_state:
        st.session_state.selected = False
    if 'run_once' not in st.session_state:
        st.session_state.run_once = False
    if 'reviewed' not in st.session_state:
        st.session_state.download_disable = True
    if 'data_updated' not in st.session_state:
        st.session_state.data_updated = False
    st.session_state.og_df = None
    st.session_state.filtered_df = None
    upload_input()


if __name__ == "__main__":
    init()
