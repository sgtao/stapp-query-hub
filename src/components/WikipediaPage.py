# WikipediaPage.py
import streamlit as st

# import wikipedia

from functions.WikipediaQuery import WikipediaQuery


class WikipediaPage:
    def __init__(self, title=None):
        self.title = title
        if title:
            self.load_page(title)
        else:
            self.page = None

    def load_page(self, title):
        wikipedia_query = WikipediaQuery(title)
        self.page = wikipedia_query.get_page()
        self.title = self.page.title
        self.url = self.page.url

    def display_linked_title(self):
        st.markdown(f"### [{self.title}]({self.url})")

    def display_page_info(self):
        if not self.page:
            st.error("ページが読み込まれていません。")
            return

        wp = self.page
        with st.expander("ページ情報:"):
            st.write("original_title:", wp.original_title)
            st.write("pageid:", wp.pageid)
            st.write("parent_id:", wp.parent_id)
            st.write("revision_id:", wp.revision_id)
        # st.write("coordinates:", wp.coordinates)
        with st.expander("概要:"):
            st.write(wp.summary)
        with st.expander(f"カテゴリ ({len(wp.categories)})"):
            st.write(wp.categories)

    def display_page_detail(self):
        if not self.page:
            st.error("ページが読み込まれていません。")
            return

        wp = self.page
        st.subheader("詳細")
        with st.expander("セクション一覧"):
            st.write(wp.sections)
        with st.expander("本文（全文表示）"):
            st.write(wp.content)
        with st.expander("HTML（全文表示）"):
            st.code(wp.html, language="html")

    def display_links_images(self):
        if not self.page:
            st.error("ページが読み込まれていません。")
            return

        wp = self.page
        st.subheader("リンク・画像")
        with st.expander(f"リンク一覧: {len(wp.links)}"):
            st.write(wp.links)
        with st.expander(f"画像URL一覧: {len(wp.images)}"):
            st.write(wp.images)

    def display_references(self):
        if not self.page:
            st.error("ページが読み込まれていません。")
            return

        wp = self.page
        st.subheader("参考")
        with st.expander(f"参考文献数: {len(wp.references)}"):
            st.write(wp.references)

    def display_all_info(self):
        if not self.page:
            st.error("ページが読み込まれていません。")
            return

        wp = self.page
        st.subheader("全情報")
        with st.expander("ページ情報:"):
            st.write("title, url, original_title")
            st.code(wp.title)
            st.code(wp.url)
            st.code(wp.original_title)

            st.write("pageid, parent_id, revision_id")
            st.code(wp.pageid)
            st.code(wp.parent_id)
            st.code(wp.revision_id)
        # st.write("coordinates:", wp.coordinates)
        with st.expander("概要:"):
            st.code(wp.summary)
        with st.expander("本文（全文表示）"):
            st.code(wp.content)
        with st.expander(f"カテゴリ ({len(wp.categories)})"):
            st.code(wp.categories)
        # st.write("section:", wp.section)
        with st.expander("セクション一覧"):
            st.code(wp.sections)
        with st.expander(f"リンク一覧: {len(wp.links)}"):
            st.code(self.page.links)
        with st.expander(f"画像URL一覧: {len(wp.images)}"):
            st.code(wp.images)
        with st.expander(f"参考文献数: {len(wp.references)}"):
            st.code(wp.references)
        with st.expander("HTML"):
            st.code(wp.html, language="html")


def wiki_page_viewer(title=None):
    """
    Wikipediaページを表示する
    """
    wp = WikipediaPage(title)
    wp.display_linked_title()
    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "ページ情報・概要・カテゴリ",
            "詳細",
            "リンク・画像・参考",
            "全情報(for copy)",
        ]
    )
    with tab1:
        wp.display_page_info()
    with tab2:
        wp.display_page_detail()
    with tab3:
        wp.display_links_images()
        wp.display_references()
    with tab4:
        wp.display_all_info()

    return wp
