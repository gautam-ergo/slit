import streamlit as st

replacements = {}


@st.cache
def cache_input(df):
    return df


@st.experimental_singleton
def memoize(df):
    st.dataframe(df, use_container_width=True)


# @st.experimental_memo
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')


def pair_replacements():
    replacements.clear()
    for i, word in enumerate(st.session_state.user_text_input):
        if not st.session_state[f"Replacement_{i}"]:
            st.error("replacement cannot be blank")
            st.stop()
        replacements[st.session_state.user_text_input[i]] = st.session_state[f"Replacement_{i}"]
