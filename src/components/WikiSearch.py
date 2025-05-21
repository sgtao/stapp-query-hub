# WikiSearch.py
import time

import streamlit as st

from components.WikipediaLangSelector import WikipediaLangSelector
from functions.WikipediaQuery import WikipediaQuery


class WikiSearch:
    def __init__(self):
        # Wikipedia Searchの状態・結果を管理するセッションの初期化
        if "lang_code" not in st.session_state:
            st.session_state.lang_code = "ja"
        if "wiki_query_word" not in st.session_state:
            st.session_state.wiki_query_word = ""
        if "wiki_num_results" not in st.session_state:
            st.session_state.wiki_num_results = 5
        if "wiki_query_results" not in st.session_state:
            st.session_state.wiki_query_results = []

    def query_input(self):
        return st.text_input(
            label="Search Wikipedia",
            value=st.session_state.wiki_query_word,
            placeholder="Search Wikipedia",
            # key="wiki_query_input",
        )

    def lang_selector(self):
        lang_selector = WikipediaLangSelector()

        st.session_state.lang_code = lang_selector.select_language(
            lang_code=st.session_state.lang_code
        )
        return st.session_state.lang_code

    def num_results_slider(self):
        st.session_state.wiki_num_results = st.slider(
            label="Number of Results",
            min_value=1,
            max_value=20,
            step=1,
            value=st.session_state.wiki_num_results,
        )
        return st.session_state.wiki_num_results

    def query_submit(self, query_word, lang_code, num_results):
        # query_results = wiki_search.query_submit(
        #     user_input=user_input,
        #     lang_code=lang_code,
        #     num_results=num_results,
        # )
        wiki_query_results = st.session_state.wiki_query_results
        if st.button(label="🔍 Search", type="primary"):
            # blank input case
            if query_word == "":
                st.warning("Please enter a word to search.")
                time.sleep(2)
                st.rerun()

            # query word
            try:
                st.session_state.wiki_query_word = query_word
                wikipedia_query = WikipediaQuery(
                    # query_word=user_input, lang=st.session_state.lang_code
                    # query_word=query_word,
                    lang=lang_code,
                )
                # st.session_state.wiki_query_results = wikipedia_query.search(
                wiki_query_results = wikipedia_query.search(
                    query_word=query_word,
                    # num_results=st.session_state.wiki_num_results,
                    num_results=num_results,
                )
            except Exception as e:
                st.error(f"Error: {e}")
                time.sleep(2)
                st.rerun()
            finally:
                st.session_state.wiki_query_results = wiki_query_results

        return wiki_query_results

    def clear_query(self):
        if st.button("🧹 Clear"):
            # st.session_state["wiki_query_input"] = ""
            st.session_state.wiki_query_word = ""
            st.session_state.wiki_query_results = []
            st.session_state.lang_code = "ja"
            st.info("Cleared!")
            time.sleep(2)
            st.rerun()

    def render_query_inputs(self):
        query_word = st.session_state.wiki_query_word
        query_results = st.session_state.wiki_query_results
        lang_code = st.session_state.lang_code
        num_results = st.session_state.wiki_num_results

        # submit to query
        col1, col2 = st.columns([4, 1], vertical_alignment="bottom")
        with col1:
            query_word = self.query_input()
        with col2:
            query_results = self.query_submit(
                query_word=query_word,
                lang_code=lang_code,
                num_results=num_results,
            )

        # search control
        (
            col1,
            col2,
            col3,
            col4,
        ) = st.columns([1, 2, 1, 1])

        with col1:
            lang_code = self.lang_selector()

        with col2:
            num_results = self.num_results_slider()

        with col3:
            pass

        with col4:
            self.clear_query()

        return query_results
