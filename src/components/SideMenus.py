# SideMenus.py
import streamlit as st


class SideMenus:
    def __init__(self):
        # インスタンス化
        pass

    def session_state_viewer(self):
        with st.sidebar:
            st.subheader("for debug.")
            with st.expander("session_state", expanded=False):
                st.write(st.session_state)
