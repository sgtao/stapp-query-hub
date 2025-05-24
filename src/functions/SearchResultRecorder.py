# SearchResultRecorder.py
import datetime
import os
import yaml

# 保存先ディレクトリとファイル名を定数で定義
RESULTS_DIR = "results"
DEFAULT_YAMLFILE_PATH = os.path.join(RESULTS_DIR, "query_response.yaml")


class SearchResultRecorder:
    def __init__(self, yaml_file=DEFAULT_YAMLFILE_PATH):
        """
        YAMLファイル保存用マネージャ
        :param yaml_file: 保存先YAMLファイルのパス
        """
        self.yaml_file = yaml_file
        self.results_dir = RESULTS_DIR

        # ディレクトリがなければ作成
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)

    def save_to_yamlfile(self, label="Wikipedia", query=None, data=None):
        """
        検索結果をYAMLファイルにリスト形式で追記保存
        """
        # タイムスタンプ生成
        now = datetime.datetime.now()
        timestamp = now.strftime("%y%m%d-%H:%M:%S")

        # 1件分のレコードを作成
        item = {
            "type": label,
            "timestamp": timestamp,
            "query": query,
            "result": data,
        }

        # # 既存ファイルの読み込み（なければ空リスト）
        # if os.path.exists(self.yaml_file):
        #     with open(self.yaml_file, "r", encoding="utf-8") as f:
        #         try:
        #             items = yaml.safe_load(f)
        #             if not isinstance(items, list):
        #                 items = []
        #         except Exception:
        #             items = []
        # else:
        #     items = []
        items = []

        # 新しいitemを追加
        items.append(item)

        # YAMLとして上書き保存
        # with open(self.yaml_file, "w", encoding="utf-8") as f:
        with open(self.yaml_file, "a", encoding="utf-8") as f:
            yaml.safe_dump(
                items, f, allow_unicode=True, default_flow_style=False
            )

    def load_from_yamlfile(self):
        """
        YAMLファイルを読み込んでPythonオブジェクトとして返す
        """
        if not os.path.exists(self.yaml_file):
            raise FileNotFoundError(f"{self.yaml_file} が存在しません")
        with open(self.yaml_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data

    def get_yamlfile_path(self):
        return self.yaml_file

    def get_results_dir(self):
        return self.results_dir

    def get_yaml_filelist(self):
        # resultsディレクトリ内のYAMLファイル一覧
        yaml_files = []
        if not os.path.exists(self.results_dir):
            return yaml_files

        for f in os.listdir(self.results_dir):
            if os.path.isfile(
                os.path.join(self.results_dir, f)
            ) and f.endswith(".yaml"):
                yaml_files.append(os.path.join(self.results_dir, f))
        return yaml_files
