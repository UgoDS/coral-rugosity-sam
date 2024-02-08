import streamlit as st

sts = st.session_state


def init_session_state(dict_keys):
    for k, v in dict_keys.items():
        if k not in st.session_state:
            st.session_state[k] = v


def dl_button_zip(path_zip):
    with open(path_zip, "rb") as fp:
        btn = st.download_button(
            label="Download results ZIP",
            data=fp,
            file_name="results.zip",
            mime="application/zip",
        )
