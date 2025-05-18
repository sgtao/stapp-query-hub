import streamlit as st

st.set_page_config(
    page_title="Streamlit App",
    page_icon=":shark:",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main():
    st.markdown(
        """
        # Welcome to stapp-query-hub!
        [streamlit app](https://streamlit.io/) for navigate to query info.
        """
    )

    # サイドバーのページに移動
    # st.page_link("pages/example_app.py", label="Go to Example App")
    st.page_link(
        "pages/11_wikipedia_search.py",
        label="Go to Wikipedia Search App",
        icon="📔",
    )
    # ログ表示ページへのリンク
    st.page_link("pages/21_logs_viewer.py", label="View Logs", icon="📄")


if __name__ == "__main__":
    main()
