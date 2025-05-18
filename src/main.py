import streamlit as st

st.set_page_config(
    page_title="Streamlit App",
    page_icon=":shark:",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(
    """
    # Welcome to Streamlit!
    [streamlit app](https://streamlit.io/) for navigate to query info.
    """
)


# サイドバーのページに移動
# st.page_link("pages/example_app.py", label="Go to Example App")
# st.page_link("pages/01_example_app.py", label="Go to Example App", icon="🚀")
