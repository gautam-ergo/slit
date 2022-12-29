import pandas as pd
import streamlit as st

from app.editor import editable_grid
from app.utils import convert_df, cache_input, replacements, pair_replacements

user_text_input = []


def process(source_df: pd.DataFrame):
    global user_text_input

    st.title("🚀")

    def filter_dataframe(inp_df: pd.DataFrame) -> pd.DataFrame:
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
            return inp_df

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
                st.dataframe(st.session_state.filtered_df)
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

        return df

    cached_df = cache_input(source_df)

    data = filter_dataframe(cached_df)

    if not user_text_input:
        st.write("All rows:")
        st.dataframe(data)

    if user_text_input:
        # if 'user_text_input' in st.session_state and st.session_state.user_text_input:
        st.write(f"Total Rows-{len(cached_df)}, Filtered Rows-{len(st.session_state.filtered_df)}")
        with st.form(key='form_1'):
            ncol = len(st.session_state.user_text_input)
            cols = st.columns([ncol, 0.1, 0.1])
            # for i, col in enumerate(cols):
            for i in range(ncol):
                col = cols[i % 1]
                col.text_input(f"Replacement word for {st.session_state.user_text_input[i]}"
                               , key=f"Replacement_{i}")
            submitted = st.form_submit_button('Submit')
            if submitted:
                pair_replacements()
                st.session_state.selected = st.session_state['FormSubmitter:form_1-Submit']  # True
                st.json(replacements)

        if st.session_state.get('FormSubmitter:form_1-Submit'):
        # if st.session_state.selected and replacements:
            my_expander = st.expander("Modified Data", expanded=True)
            with my_expander:
                dic = {r"\b(?i){}\b".format(k.strip()): v for k, v in replacements.items()}
                st.session_state.og_df['input'].replace(dic, regex=True, inplace=True)
                display = st.session_state.og_df[
                    st.session_state.og_df.index.isin(st.session_state.filtered_df.index)
                ]
                # paginate_df(display)
                editable_grid(display)

            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                approved = st.button(
                    'Approve Changes',
                    key='reviewed',
                    disabled=False,
                    type="primary",
                )
                if approved:
                    if not st.session_state.data_updated:
                        # with col2:
                        st.error("Data Update incomplete")
                        st.stop()
                    st.session_state.download_disable = not approved

            with col3:
                downloaded = st.download_button(
                    "Download Modified file",
                    convert_df(st.session_state.og_df),
                    "file.csv",
                    "text/csv",
                    key='download-csv',
                    help='Approve changes to enable download',
                    disabled=st.session_state.download_disable,
                )
                if downloaded:
                    st.session_state.download_disable = True
