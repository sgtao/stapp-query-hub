# QiitaSearch.py
import time

import streamlit as st

from functions.QiitaItemRequestor import QiitaItemRequestor
from functions.SearchResultRecorder import SearchResultRecorder


class QiitaSearch:
    def __init__(self):
        self.query_word = ""
        self.num_results = 5  # デフォルトの表示件数
        self.qiita_query_results = []
        if "query_word" not in st.session_state:
            st.session_state.query_word = ""
        if "qiita_num_results" not in st.session_state:
            st.session_state.qiita_num_results = 5
        if "qiita_query_results" not in st.session_state:
            st.session_state.qiita_query_results = []

    def query_input(self):
        """
        ユーザーからの入力を受け付けるための関数
        """
        _input_placeholder = "query word(e.g. Python, Streamlit, etc.)."
        _input_placeholder += "if blank, show latest articles."
        self.query_word = st.text_input(
            label="Search Qiita",
            value=st.session_state.query_word,
            placeholder=_input_placeholder,
            # key="wiki_query_input",
        )

    def num_results_slider(self):
        st.session_state.qiita_num_results = st.slider(
            label="Number of Results",
            min_value=1,
            max_value=100,
            step=1,
            value=st.session_state.qiita_num_results,
        )
        return st.session_state.qiita_num_results

    def query_submit(self):
        """
        ユーザーが入力したクエリを送信するための関数
        """
        qiita_requestor = QiitaItemRequestor()
        if st.button(label="🔍 Search", type="primary"):
            st.session_state.query_word = self.query_word
            self.qiita_query_results = qiita_requestor.get_articles(
                params={"query": self.query_word},
            )
            # record query result
            search_recorder = SearchResultRecorder()
            _query_word = (
                self.query_word if self.query_word else "latest articles"
            )
            search_recorder.save_to_yamlfile(
                label="Wikipedia",
                query=_query_word,
                data=self.qiita_query_results,
            )
            st.session_state.qiita_query_results = self.qiita_query_results
            # st.session_state.qiita_result = qiita_requestor.get_results()
            # st.rerun()
            return self.qiita_query_results

    def render_search_results(self, results_list):
        st.write(f"表示件数: {len(results_list)} 件")
        st.write()
        for result in results_list:
            self.qiita_item(result, id=result["id"], info_open=False)

    def qiita_item(self, article, id=None, article_body=None, info_open=True):
        # 記事タイトルをリンクとして表示n
        st.markdown(f"### [{article['title']}]({article['url']})")
        # id をコピーボタン付きで表示
        if id is not None:
            col1, col2 = st.columns([1, 2])
            col1.info("記事ID(for copy):")
            col2.code(article["id"])

        with st.expander("show item info.", expanded=info_open, icon="📌"):
            # 記事の基本情報を表示
            user_name = article["user"]["name"]
            user_id = article["user"]["id"]
            group_info = (
                article["group"]["name"] if article["group"] else "なし"
            )
            group_id = article["group"]["id"] if article["group"] else "なし"
            info_text = (
                # f"記事ID: {article['id']}, "
                f"作成日: {article['created_at']}, "
                f"最終更新日: {article['updated_at']}, "
                f"作成者: {user_name} (ID: {user_id} ), "
                f"グループ: {group_info} (ID: {group_id})"
            )
            st.write()
            st.success(info_text)
            # タグリストを作成
            tag_list = " ".join(tag["name"] for tag in article["tags"])
            st.write()
            st.info(f"タグ: {tag_list}")
            # st.markdown(f"## Title: {article['title']}")
            st.markdown(article["body"])

        if article_body is not None:
            # 記事本文を表示
            st.write(article_body)

        # 区切り線を追加
        st.markdown("---")

    def clear_query(self):
        if st.button("🧹 Clear"):
            # st.session_state["wiki_query_input"] = ""
            st.session_state.query_word = ""
            st.session_state.qiita_query_results = []
            st.info("Cleared!")
            time.sleep(2)
            st.rerun()

    def render_query_inputs(self):
        query_word = st.session_state.query_word
        query_results = st.session_state.qiita_query_results
        # lang_code = st.session_state.lang_code
        self.num_results = st.session_state.wiki_num_results

        # submit to query
        col1, col2 = st.columns([4, 1], vertical_alignment="bottom")
        with col1:
            query_word = self.query_input()
        with col2:
            query_results = self.query_submit(
                query_word=query_word,
                # lang_code=lang_code,
                # num_results=num_results,
            )

        # search control
        (
            col1,
            col2,
            col3,
            col4,
        ) = st.columns([2, 1, 1, 1])

        with col1:
            # lang_code = self.lang_selector()
            pass

        with col2:
            self.num_results = self.num_results_slider()

        with col3:
            pass

        with col4:
            self.clear_query()

        return query_results
