# QiitaItemRequestor.py
from urllib.parse import urlencode

import requests

from functions.AppLogger import AppLogger


# Qiita APIのベースURL
BASE_URL = "https://qiita.com/api/v2"


class QiitaItemRequestor:
    def __init__(self, base_url=BASE_URL):
        self.endpoint = f"{base_url}/items"
        # Qiita APIのレート制限に関する情報を初期化
        # refer: https://qiita.com/api/v2/docs
        self.rate_remaining = 60
        self.query_word = ""
        self.results = []
        self.logger = AppLogger(name="QiitaItemRequestor")

    def get_rate_remaining(self):
        return self.rate_remaining

    def get_results(self):
        """
        Qiita APIから取得した記事のリストを返す。

        Returns:
            list: Qiita APIから取得した記事のリスト。
        """
        return self.results

    def get_articles(self, params=None, page_size=20, page_num=1):
        """
        Qiita APIから記事を取得するための共通関数。

        指定されたエンドポイントとオプションのパラメータを使用して、
        Qiita APIからデータを取得します。

        Args:
            query (str): クエリ文字列。デフォルト(None)の場合は最新記事を取得
            page_size (int, optional): １ページのアイテム数（`per_page`）
            pane_num (int, optional): ページ番号（`page`パラメータ）

        Returns:
          tuple(list or dict): APIからのレスポンスをJSON形式で返します。
        """

        try:
            # `query`の指定有無でアクセスURI を変化させる
            page_uri = f"{self.endpoint}?page={page_num}&per_page={page_size}"
            if params is None:
                self.query_word = "Latest Articles"
                uri = f"{page_uri}"
            else:
                self.query_word = params
                query_string = urlencode(params)
                uri = f"{page_uri}&query={query_string}"

            # print(f"request GET {uri}")
            response = requests.get(uri)
            response.raise_for_status()  # HTTPエラーをチェック

            # Rate-Remainingをヘッダーから取得
            self.rate_remaining = int(
                response.headers.get("Rate-Remaining", 0)
            )

            # for debugging
            self.results = []

            # extract necessary info. from response
            for item in response.json():
                # 記事の基本情報を取得
                # print(item)
                user_info = {}
                group_info = {}
                if item["user"]:
                    user_info = {
                        "name": item["user"].get("name", ""),
                        "id": item["user"].get("id", ""),
                    }
                if item["group"]:
                    group_info = {
                        # "name": item["group"].get("name", ""),
                        # "id": item["group"].get("id", ""),
                        "name": item["group"]["name"],
                        "id": item["group"]["id"],
                    }
                self.results.append(
                    {
                        "id": item.get("id", ""),
                        "title": item.get("title", ""),
                        "url": item.get("url", ""),
                        "body": item.get("body", ""),
                        "created_at": item.get("created_at", ""),
                        "updated_at": item.get("updated_at", ""),
                        "user": user_info,
                        "group": group_info,
                        "tags": item.get("tags", []),
                    }
                )

            self.logger.info_log(
                f"Search results for '{self.query_word}': {self.results}"
            )

            # return response.json()
            return self.results

        except Exception as e:
            self.logger.error_log(
                f"Exception occur at {self.query_word} : {e}"
            )
            raise e
        # finally:
        #     return response.json()
