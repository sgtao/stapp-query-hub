# SearchResultRecorder.py
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
        self.results_dir = os.path.dirname(yaml_file)

        # ディレクトリがなければ作成
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)

    def save_to_yamlfile(self, data):
        """
        データをYAML形式でファイルに上書き保存
        """
        with open(self.yaml_file, "w", encoding="utf-8") as f:
            yaml.safe_dump(
                data, f, allow_unicode=True, default_flow_style=False
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
        return [
            os.path.join(self.results_dir, f)
            for f in os.listdir(self.results_dir)
            if os.path.isfile(os.path.join(self.results_dir, f))
            and f.endswith(".yaml")
        ]
