import pandas as pd
import streamlit as st

from app.editor import editable_grid
from app.filter import filter_dataframe
from app.utils import convert_df, cache_input, replacements, pair_replacements, memoize


def process(source_df: pd.DataFrame):
    st.title("🚀")

    cached_df = cache_input(source_df)

    data, filtered = filter_dataframe(cached_df)

    if not filtered:
        st.write("All rows:")
        # st.dataframe(data)
        memoize(data)

    if filtered:
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
                st.session_state.data_updated = False
                st.json(replacements)

        if st.session_state.get('FormSubmitter:form_1-Submit') or st.session_state.data_updated:
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

            # kinda Footers
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
