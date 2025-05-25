# qiita_search.py
import streamlit as st

from components.SideMenus import SideMenus

# from components.WikipediaLangSelector import WikipediaLangSelector
from functions.AppLogger import AppLogger
from functions.QiitaItemRequestor import QiitaItemRequestor
from functions.SearchResultRecorder import SearchResultRecorder

# from functions.WikipediaQuery import WikipediaQuery


APP_TITLE = "Qiita API Search App"


def initial_session_state():
    if "wiki_query_word" not in st.session_state:
        st.session_state.wiki_query_word = ""
    if "query_results" not in st.session_state:
        st.session_state.query_results = []


def render_search_results(results_list):
    st.write(f"表示件数: {len(results_list)} 件")
    st.write()
    for result in results_list:
        qiita_item(result, id=result["id"], info_open=False)


def qiita_item(article, id=None, article_body=None, info_open=True):
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
        group_info = article["group"]["name"] if article["group"] else "なし"
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


def main():
    app_logger = AppLogger(APP_TITLE)
    app_logger.app_start()

    st.page_link("main.py", label="Back to Home", icon="🏠")

    st.title(f"💻 {APP_TITLE}")

    """
    In the meantime,
    Search user input by wikipedia
    """
    # wikipedia.set_lang("ja")
    qiita_requestor = QiitaItemRequestor()
    _input_placeholder = "query word(e.g. Python, Streamlit, etc.)."
    _input_placeholder += "if blank, show latest articles."
    query_word = st.text_input(
        label="Search Qiita",
        value=st.session_state.wiki_query_word,
        placeholder=_input_placeholder,
        # key="wiki_query_input",
    )
    if st.button(label="🔍 Search", type="primary"):
        qiita_query_results = qiita_requestor.get_articles(
            params={"query": query_word},
        )
        # record query result
        search_recorder = SearchResultRecorder()
        search_recorder.save_to_yamlfile(
            label="Wikipedia",
            query={query_word if query_word else "latest articles"},
            data=qiita_query_results,
        )
        st.session_state.query_results = qiita_query_results
        # st.session_state.qiita_result = qiita_requestor.get_results()
        st.rerun()

    # Display the search results
    st.write("### Search Results")
    # if not st.session_state.wiki_query_results:
    if not st.session_state.query_results:
        st.info("一致なし")
    else:
        # st.json(st.session_state.query_results)
        # for result in st.session_state.wiki_query_results:
        render_search_results(st.session_state.query_results)


if __name__ == "__main__":
    # Initialize session state
    initial_session_state()
    # SideMenu for Debugging
    side_menus = SideMenus()
    side_menus.session_state_viewer()
    # Run the main function
    main()
