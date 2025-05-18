# wikipedia_search.py
import time

import streamlit as st
import wikipedia

from components.WikipediaPage import wiki_page_viewer

APP_TITLE = "Wikipedia Search"


def main():
    st.title(f"📔 {APP_TITLE}")

    """
    In the meantime,
    Search user input by wikipedia
    """
    if "search_word" not in st.session_state:
        st.session_state.search_word = ""

    wikipedia.set_lang("ja")
    words = []

    user_input = st.text_input(
        label="Search Wikipedia",
        value=st.session_state.search_word,
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
            if user_input == "":
                st.warning("Please enter a word to search.")
                time.sleep(2)
                st.rerun()
            words = wikipedia.search(user_input)
            st.session_state.search_word = user_input
    with col2:
        if st.button("🧹 Clear"):
            st.session_state.search_word = ""
            words = []
    with col3:
        pass
    with col4:
        pass
    with col5:
        pass

    if not words:
        st.info("一致なし")
    else:
        for word in words:
            with st.expander(f"📚 {word}", expanded=False):
                st.info(wikipedia.summary(word))
                if st.button(
                    label="🔗 Wikipedia",
                    help=f"Open {word} in Wikipedia",
                    key=word,
                    # disabled=st.session_state.api_running,
                ):
                    # page_content = wikipedia.page(word).content
                    # st.info(f"[{word}](https://ja.wikipedia.org/wiki/{word})")
                    # st.markdown(page_content)
                    wiki_page_viewer(word)


if __name__ == "__main__":
    main()
