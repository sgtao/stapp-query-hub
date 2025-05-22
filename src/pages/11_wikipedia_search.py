# wikipedia_search.py
import time

import streamlit as st

from components.SideMenus import SideMenus
from components.WikiSearch import WikiSearch
from components.WikipediaPage import wiki_page_viewer

# from components.WikipediaLangSelector import WikipediaLangSelector
from functions.AppLogger import AppLogger
from functions.SearchResultRecorder import SearchResultRecorder

# from functions.WikipediaQuery import WikipediaQuery


APP_TITLE = "Wikipedia Search"


def initial_session_state():
    pass


@st.dialog("Modal:", width="large")
def modal(type=None, title=None):
    def _modal_closer():
        if st.button(label="Close Modal"):
            st.info("モーダルを閉じます...")
            time.sleep(1)
            st.rerun()

    st.write(f"Modal for {type}:")
    if type == "page_viewer":
        wiki_page_viewer(title)
        _modal_closer()
    else:
        st.write("No Definition.")


def main():
    app_logger = AppLogger(APP_TITLE)
    app_logger.app_start()
    search_recorder = SearchResultRecorder()

    st.page_link("main.py", label="Back to Home", icon="🏠")

    st.title(f"📔 {APP_TITLE}")

    """
    In the meantime,
    Search user input by wikipedia
    """
    # wikipedia.set_lang("ja")
    wiki_search = WikiSearch()
    query_results = wiki_search.render_query_inputs()
    search_recorder.save_to_yamlfile(query_results)

    # Display the search results
    st.write("### Search Results")
    # if not st.session_state.wiki_query_results:
    if not query_results:
        st.info("一致なし")
    else:
        # for result in st.session_state.wiki_query_results:
        for result in query_results:
            with st.expander(f"📚 {result.get('word')}", expanded=False):
                st.write(result.get("link"))
                st.info(result.get("summary"))
                if st.button(
                    label="🔗 Wiki. Page",
                    help=f"Open {result.get('word')} in Wikipedia",
                    key=f"wiki_link_{result.get('word')}",
                ):
                    # page_content = wikipedia.page(word).content
                    # st.info(f"[{word}](https://ja.wikipedia.org/wiki/{word})")
                    # st.markdown(page_content)
                    modal("page_viewer", result.get("word"))


if __name__ == "__main__":
    # Initialize session state
    initial_session_state()
    # SideMenu for Debugging
    side_menus = SideMenus()
    side_menus.session_state_viewer()
    # Run the main function
    main()
