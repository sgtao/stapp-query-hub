# WikipediaQuery.py
import wikipedia

from functions.AppLogger import AppLogger


class WikipediaQuery:
    def __init__(self, query_word=None):
        wikipedia.set_lang("ja")
        self.query_word = query_word
        self.results = []
        self.page = None
        self.logger = AppLogger(name="WikipediaQuery")

    def search(self, query_word=""):
        if not query_word:
            return []
        else:
            self.query_word = query_word

        self.results = []
        try:
            words = wikipedia.search(self.query_word, results=5)
            for word in words:
                self.results.append(
                    {
                        "word": word,
                        "summary": wikipedia.summary(word),
                        "link": f"https://ja.wikipedia.org/wiki/{word}",
                    }
                )
            self.logger.info_log(
                f"Search results for '{self.query_word}': {self.results}"
            )
            return self.results
        except wikipedia.exceptions.DisambiguationError as e:
            self.logger.error_log(f"Disambiguation error: {e}")
            return []
        except wikipedia.exceptions.PageError as e:
            self.logger.error_log(f"Page error: {e}")
            return []

    def get_page(self, title=""):
        page_title = title
        if not title:
            page_title = self.query_word

        self.logger.info_log(f"get wikipedia page `{page_title}`")

        try:
            self.page = wikipedia.page(page_title)
            self.logger.info_log(f"Page for `{page_title}`: {self.page}")
            return self.page
        except wikipedia.exceptions.DisambiguationError as e:
            self.logger.error_log(f"Disambiguation error: {e}")
            return ""
        except wikipedia.exceptions.PageError as e:
            self.logger.error_log(f"Page error: {e}")
            return ""
