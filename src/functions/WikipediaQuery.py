# WikipediaQuery.py
import wikipedia

from functions.AppLogger import AppLogger


class WikipediaQuery:
    def __init__(self, query_word=None, lang="ja"):
        self.query_word = query_word
        self.used_lang = lang
        self.results = []
        self.page = None
        self.logger = AppLogger(name="WikipediaQuery")
        self.set_lang(self.used_lang)

    def set_lang(self, lang="ja"):
        """
        Set the language for Wikipedia search.
        :param lang: Language code (e.g., "ja" for Japanese)
        """
        if lang != self.used_lang:
            self.logger.info_log(
                f"Change language from {self.used_lang} to {lang}"
            )
            self.used_lang = lang
        else:
            self.logger.info_log(f"Set Language to {self.used_lang}")

        wikipedia.set_lang(lang)
        self.logger.info_log(f"Set Wikipedia language to {lang}")

    def search(self, query_word="", num_results=5):
        if not query_word:
            return []
        else:
            self.query_word = query_word

        self.results = []
        try:
            # suggested_query = wikipedia.suggest(self.query_word)
            # if suggested_query:
            #     self.logger.info_log(
            #         f"Suggested for '{self.query_word}': {suggested_query}"
            #     )
            #     self.query_word = suggested_query
            # else:
            #     self.logger.info_log(f"No suggestion of {self.query_word}.")
            #     return self.results

            # Search for the query word
            words = wikipedia.search(
                query=self.query_word,
                results=num_results,
                # suggestion=True,
            )
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
