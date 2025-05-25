# results_viewer.py
from datetime import datetime
import os
import yaml

import streamlit as st

from functions.AppLogger import AppLogger
from functions.SearchResultRecorder import SearchResultRecorder

# APP_TITLE = "APIクライアントアプリ"
APP_TITLE = "Query Result Viewer"
YAML_FILE_PATH = "results/query_response.yaml"


def display_yaml_results(yaml_file_path):
    try:
        with open(yaml_file_path, "r", encoding="utf-8") as f:
            items = yaml.safe_load(f)
        if not items:
            st.info("記録された検索結果がありません。")
            return
        for idx, item in enumerate(items):
            _type = item.get("type", "")
            _timestamp = item.get("timestamp", "--")
            _query_word = item.get("query", "--")
            label = f"{idx+1:02d} [{_type}] ({_timestamp}) : {_query_word}"

            with st.expander(label=label, expanded=False):
                st.write("**クエリ:**", item.get("query", ""))
                st.write("**タイプ:**", item.get("type", ""))
                st.write("**時刻:**", item.get("timestamp", ""))
                st.write("**結果:**")
                for res in item.get("result", []):
                    # for Wikipedia results
                    if "word" in res:
                        st.markdown(
                            f"- [{res.get('word', '')}]({res.get('link', '')})"
                        )
                    if "summary" in res:
                        st.caption(res["summary"])
                    # for Qiita results
                    if "title" in res:
                        st.markdown(
                            f"- [{res.get('title', '')}]({res.get('url', '')})"
                        )
                    if "body" in res:
                        st.markdown(res["body"])

    except FileNotFoundError:
        st.error(f"YAMLファイルが見つかりません: {yaml_file_path}")
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")


def rotate_yaml_file(yaml_file_path):
    try:
        now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        base, ext = os.path.splitext(yaml_file_path)
        rotated_file = f"{base}_{now}{ext}"
        os.rename(yaml_file_path, rotated_file)
        if not os.path.exists(yaml_file_path):
            # デフォルトのYAMLファイルが存在しない場合, create blank file
            with open(yaml_file_path, "w", encoding="utf-8") as f:
                f.write(f"# created at {now}\n")

        st.success(f"YAMLファイルをローテートしました: {rotated_file}")
        return rotated_file
    except FileNotFoundError:
        st.error(f"YAMLファイルが見つかりません: {yaml_file_path}")
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")


def main():
    app_logger = AppLogger(APP_TITLE)
    app_logger.app_start()
    search_recorder = SearchResultRecorder()

    st.page_link("main.py", label="Back to Home", icon="🏠")

    st.title(f"👓 {APP_TITLE}")

    record_files = search_recorder.get_yaml_filelist()
    index_file = record_files.index(YAML_FILE_PATH)
    st.session_state.disable_rotate = False

    def _on_change_select():
        st.session_state.disable_rotate = record_file != YAML_FILE_PATH

    record_file = st.selectbox(
        label="Select log file",
        options=record_files,
        on_change=_on_change_select,
        index=index_file,
    )

    # ファイルのローテートボタン
    col1, col2 = st.columns(2)
    with col1:
        if st.button(
            label="Rotate Record",
            help=f"rotate {YAML_FILE_PATH}",
            disabled=st.session_state.disable_rotate,
            icon="🔃",
        ):
            # rotated = rotate_yaml_file(YAML_FILE_PATH)
            rotate_yaml_file(record_file)
            st.rerun()
    with col2:
        if st.button("Rerun (`R`)", icon="🏃"):
            st.rerun()

    # YAMLファイルの内容表示
    display_yaml_results(record_file)


if __name__ == "__main__":
    main()
