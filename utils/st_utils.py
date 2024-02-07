import streamlit as st

sts = st.session_state


def init_session_state(dict_keys):
    for k, v in dict_keys.items():
        if k not in st.session_state:
            st.session_state[k] = v
