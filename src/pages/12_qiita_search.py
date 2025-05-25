# qiita_search.py
import streamlit as st

from components.SideMenus import SideMenus
from components.QiitaSearch import QiitaSearch

# from components.WikipediaLangSelector import WikipediaLangSelector
from functions.AppLogger import AppLogger

# from functions.WikipediaQuery import WikipediaQuery


APP_TITLE = "Qiita API Search App"


def initial_session_state():
    pass


def main():
    app_logger = AppLogger(APP_TITLE)
    app_logger.app_start()

    st.page_link("main.py", label="Back to Home", icon="🏠")

    st.title(f"💻 {APP_TITLE}")
    qiita_search = QiitaSearch()
    """
    In the meantime,
    Search user input by wikipedia
    """
    qiita_search.query_input()

    qiita_query_results = qiita_search.query_submit()

    # Display the search results
    st.write("### Search Results")
    if not qiita_query_results:
        st.info("一致なし")
    else:
        qiita_search.render_search_results(qiita_query_results)


if __name__ == "__main__":
    # Initialize session state
    initial_session_state()
    # SideMenu for Debugging
    side_menus = SideMenus()
    side_menus.session_state_viewer()
    # Run the main function
    main()
