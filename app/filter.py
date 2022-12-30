from typing import Union

import pandas as pd
import streamlit as st
from pandas import DataFrame

from app.utils import memoize

user_text_input = []


def filter_dataframe(inp_df: pd.DataFrame) -> Union[tuple[DataFrame, None], tuple[DataFrame, list]]:
    """
    Adds a UI on top of a dataframe to filter columns
    Args:
        inp_df (pd.DataFrame): Original dataframe
    Returns:
        pd.DataFrame: Filtered dataframe
    """
    global user_text_input
    # azure_download()
    modify = st.checkbox("Add filters")
    st.session_state.og_df = inp_df.copy()
    if not modify:
        return inp_df, None

    # any pre-process if need be
    df = inp_df.copy()
    df['name'] = df['name'].str.strip()
    # kicking off streamlit flow
    modification_container = st.container()
    with modification_container:
        column = st.selectbox("Filter dataframe on", ['name'], key="column_name", )
        # for column in to_filter_columns:
        left, right = st.columns((1, 30))
        left.write("↳")
        # Treat columns with < 10 unique values as categorical
        if 'name' in column.lower():
            ingred_names = df[column].drop_duplicates().sort_values(ascending=True)
            user_text_input = right.multiselect(f'Filter {column} column on:', ingred_names, )
        elif 'input' in column.lower():
            inp = right.text_input(f"Search for substring in '{column}' column", )
            user_text_input = [inp] if inp else None

        if user_text_input:
            st.write("Filtered Rows")
            st.session_state.filtered_df = df[
                df[column].str.contains(fr"\b({'|'.join(user_text_input)})\b", regex=True, na=False,
                                        case=False)]
            st.session_state.user_text_input = user_text_input
            memoize(st.session_state.filtered_df)
        # if 'input' in column.lower():
        #     left, right = st.columns((1, 60))
        #     left.write("↳")
        #     ingred_names = df['name'].drop_duplicates().sort_values(ascending=True)
        #     user_text_input = right.multiselect(f'Select your value for {column}:', ingred_names, )
        #
        #     if user_text_input:
        #         st.write("Filtered Rows")
        #         st.session_state.filtered_df = df[
        #             df['name'].str.contains(fr"\b({'|'.join(user_text_input)})\b", regex=True, na=False,
        #                                     case=False)]
        #         st.session_state.user_text_input = user_text_input

    return df, user_text_input
