# WikipediaLangSelector.py
import streamlit as st

# supported languages for Wikipedia
# https://meta.wikimedia.org/wiki/List_of_Wikipedias
SUPPORTED_LANGUAGES = {
    "Japanese": "ja",
    "English": "en",
    "Cebuano": "ceb",
    "German": "de",
    "French": "fr",
    "Swedish": "sv",
    "Dutch": "nl",
    "Russian": "ru",
    "Spanish": "es",
    "Italian": "it",
    "Polish": "pl",
    "Egyptian Arabic": "arz",
    "Chinese": "zh",
    "Ukrainian": "uk",
    "Vietnamese": "vi",
    "Waray": "war",
    "Arabic": "ar",
    "Portuguese": "pt",
    "Persian": "fa",
}


class WikipediaLangSelector:
    def __init__(self):
        self.selected_language = "Japanese"

    def select_language(self, lang_code="ja"):
        # 言語名リストを作成
        language_names = list(SUPPORTED_LANGUAGES.keys())
        self.selected_language = self.get_language_by_code(lang_code)
        selected_index = (
            language_names.index(self.selected_language[0])
            if self.selected_language
            else 0
        )
        # selectboxで選択
        self.selected_language = st.selectbox(
            label="Language:",
            options=language_names,
            index=selected_index,
        )
        # 選択した言語名から言語コードを取得
        lang_code = SUPPORTED_LANGUAGES[self.selected_language]
        # 表示（確認用）
        st.write(f"(Lang. code: {lang_code})")
        # 必要に応じて返す
        return lang_code

    def get_language_by_code(self, lang_code):
        """return language name by code

        Args:
            lang_code (_type_): _description_

        Returns:
            _type_: _description_
        """
        # 言語コードから言語名を取得
        language = [
            lang
            for lang, code in SUPPORTED_LANGUAGES.items()
            if code == lang_code
        ]
        return language
