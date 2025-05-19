# wikipedia_search.py
import time

import streamlit as st

from components.SideMenus import SideMenus
from components.WikipediaPage import wiki_page_viewer
from components.WikipediaLangSelector import WikipediaLangSelector
from functions.AppLogger import AppLogger
from functions.WikipediaQuery import WikipediaQuery


APP_TITLE = "Wikipedia Search"


def initial_session_state():
    # Wikipedia Searchの状態・結果を管理するセッションの初期化
    if "lang_code" not in st.session_state:
        st.session_state.lang_code = "ja"
    if "wiki_query_word" not in st.session_state:
        st.session_state.wiki_query_word = ""
    if "wiki_query_results" not in st.session_state:
        st.session_state.wiki_query_results = []
    if "wiki_num_results" not in st.session_state:
        st.session_state.wiki_num_results = 5


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

    st.page_link("main.py", label="Back to Home", icon="🏠")

    st.title(f"📔 {APP_TITLE}")

    """
    In the meantime,
    Search user input by wikipedia
    """
    # wikipedia.set_lang("ja")

    user_input = st.text_input(
        label="Search Wikipedia",
        value=st.session_state.wiki_query_word,
        placeholder="Search Wikipedia",
    )
    (
        col1,
        col2,
        col3,
        col4,
    ) = st.columns([1, 2, 1, 1])

    with col1:
        wiki_lang_selector = WikipediaLangSelector()
        st.session_state.lang_code = wiki_lang_selector.select_language(
            lang_code=st.session_state.lang_code
        )

    with col2:
        st.session_state.wiki_num_results = st.slider(
            label="Number of Results",
            min_value=1,
            max_value=20,
            step=1,
            value=st.session_state.wiki_num_results,
        )
    with col3:
        if st.button(label="🔍 Search", type="primary"):
            st.session_state.wiki_query_results = []
            # blank input case
            if user_input == "":
                st.warning("Please enter a word to search.")
                time.sleep(2)
                st.rerun()

            # query word
            try:
                st.session_state.wiki_query_word = user_input
                wikipedia_query = WikipediaQuery(
                    query_word=user_input, lang=st.session_state.lang_code
                )
                st.session_state.wiki_query_results = wikipedia_query.search(
                    query_word=user_input,
                    num_results=st.session_state.wiki_num_results,
                )
            except Exception as e:
                st.error(f"Error: {e}")
                time.sleep(2)
                st.rerun()

    with col4:
        if st.button("🧹 Clear"):
            st.session_state.wiki_query_word = ""
            st.session_state.wiki_query_results = []
            st.info("Cleared!")
            time.sleep(2)
            st.rerun()

    # Display the search results
    st.write("### Search Results")
    if not st.session_state.wiki_query_results:
        st.info("一致なし")
    else:
        for result in st.session_state.wiki_query_results:
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
