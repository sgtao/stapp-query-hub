# wikipedia_search.py
import time

import streamlit as st
import wikipedia

from components.WikipediaPage import wiki_page_viewer

APP_TITLE = "Wikipedia Search"


def initial_session_state():
    # Wikipedia Searchの状態・結果を管理するセッションの初期化
    if "wiki_query_word" not in st.session_state:
        st.session_state.wiki_query_word = ""
        # st.rerun()
    if "wiki_query_results" not in st.session_state:
        st.session_state.wiki_query_results = []
        # st.rerun()


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
    st.page_link("main.py", label="Back to Home", icon="🏠")

    st.title(f"📔 {APP_TITLE}")

    """
    In the meantime,
    Search user input by wikipedia
    """
    wikipedia.set_lang("ja")

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
        col5,
    ) = st.columns(5)
    with col1:
        if st.button(label="🔍 Search", type="primary"):
            # blank input case
            if user_input == "":
                st.warning("Please enter a word to search.")
                time.sleep(2)
                st.rerun()

            # query word
            try:
                words = wikipedia.search(user_input, results=5)
                for word in words:
                    st.session_state.wiki_query_results.append(
                        {
                            "word": word,
                            "summary": wikipedia.summary(word),
                            "link": f"https://ja.wikipedia.org/wiki/{word}",
                        }
                    )
                st.session_state.wiki_query_word = user_input
            except Exception as e:
                st.error(f"Error: {e}")
                st.session_state.wiki_query_word = ""
                st.session_state.wiki_query_results = []
                time.sleep(2)
                st.rerun()

    with col2:
        if st.button("🧹 Clear"):
            st.session_state.wiki_query_word = ""
            st.session_state.wiki_query_results = []
            st.info("Cleared!")
            time.sleep(2)
            st.rerun()
    with col3:
        pass
    with col4:
        pass
    with col5:
        pass

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
    # Run the main function
    main()
