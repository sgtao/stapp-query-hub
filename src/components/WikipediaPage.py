# WikipediaPage.py
import streamlit as st
import wikipedia


class WikipediaPage:
    def __init__(self, title=None):
        self.title = title
        if title:
            # self.page = wikipedia.page(title)
            self.load_page(title)
        else:
            self.page = None

    def load_page(self, title):
        self.page = wikipedia.page(title)
        self.title = self.page.title
        self.url = self.page.url

    def display_linked_title(self):
        st.markdown(f"### [{self.title}]({self.url})")

    def display_page_info(self):
        if not self.page:
            st.error("ページが読み込まれていません。")
            return

        wp = self.page
        st.subheader("ページ情報")
        st.write("ページ情報")
        st.write("original_title:", wp.original_title)
        st.write("pageid:", wp.pageid)
        st.write("parent_id:", wp.parent_id)
        st.write("revision_id:", wp.revision_id)
        # st.write("coordinates:", wp.coordinates)
        st.write("概要:")
        st.write(wp.summary)
        st.write(f"カテゴリ ({len(wp.categories)})")
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

    def display_links(self):
        if not self.page:
            st.error("ページが読み込まれていません。")
            return

        wp = self.page
        st.subheader("リンク")
        st.write(f"リンク数: {len(wp.links)}")
        with st.expander("リンク一覧"):
            st.write(wp.links)
        st.write(f"画像数: {len(wp.images)}")
        with st.expander("画像URL一覧"):
            st.write(wp.images)

    def display_references(self):
        if not self.page:
            st.error("ページが読み込まれていません。")
            return

        wp = self.page
        st.subheader("参考")
        st.write(f"参考文献数: {len(wp.references)}")
        with st.expander("参考文献URL一覧"):
            st.write(wp.references)

    def display_all_info(self):
        if not self.page:
            st.error("ページが読み込まれていません。")
            return

        wp = self.page
        st.subheader("全情報")
        st.write("title:", wp.title)
        st.write("url:", wp.url)
        st.write("original_title:", wp.original_title)
        st.write("pageid:", wp.pageid)
        st.write("parent_id:", wp.parent_id)
        st.write("revision_id:", wp.revision_id)
        # st.write("coordinates:", wp.coordinates)
        st.write("summary:", wp.summary)
        st.write("categories:", wp.categories)
        # st.write("section:", wp.section)
        st.write("sections:", wp.sections)
        st.write("content:", wp.content)
        st.write("html:", wp.html)
        st.write("links:", self.page.links)


def wiki_page_viewer(title=None):
    """
    Wikipediaページを表示する
    """
    wp = WikipediaPage(title)
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "概要・ページ情報・カテゴリ",
            "詳細",
            "リンク",
            "画像・参考",
            "全情報",
        ]
    )
    with tab1:
        wp.display_page_info()
    with tab2:
        wp.display_page_detail()
    with tab3:
        wp.display_links()
    with tab4:
        wp.display_references()
    with tab5:
        wp.display_all_info()
