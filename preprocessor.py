"""
@module
"""
import re
from dataclasses import dataclass

# Typographic punctuation characters used in Kashubian text.
# Defined via chr() to avoid Python 3.12+ treating „" (U+201E/U+201D) as string delimiters.
_TYPOGRAPHIC_PUNCT = chr(8222) + chr(8221) + chr(8230) + chr(8211)  # „"…–


@dataclass
class PreprocessedData:
    word_list: list
    sentence_list: list
    word_set: set


class Preprocessor:
    """A class to preprocess the Kashubian text for subsequent analysis."""

    def preprocess(self, text: str) -> PreprocessedData:
        """
        Preprocess the imported text for further analysis.
        :param text: raw text string
        :return: PreprocessedData
        """
        word_list = self._get_word_list(text)
        sentence_list = self._get_sentences(text)
        sentence_list = self._remove_line_breaks(sentence_list)
        sentence_list = self._rebuild_word_list(sentence_list)
        word_set = self._build_word_set(word_list)
        return PreprocessedData(word_list=word_list, sentence_list=sentence_list, word_set=word_set)

    @staticmethod
    def _get_word_list(text: str) -> list:
        word_list = re.split(r"[\n.\s,\"\-]+", text)
        pattern = re.compile(r"[\d!#%&'()*+,\-./:;<=>?@\[\]^_{|}~" + _TYPOGRAPHIC_PUNCT + "]+")
        word_list = [re.sub(pattern, "", item).lower() for item in word_list]
        return [item for item in word_list if item]

    @staticmethod
    def _get_sentences(text: str) -> list:
        dash = chr(8211)
        sentence_splitter = re.compile(r"( *[.?!…" + dash + "])+ *")
        sentence_list = re.split(sentence_splitter, text)
        sentence_odds = sentence_list[::2]
        sentence_evens = sentence_list[1:][::2]
        it_length = min(len(sentence_odds), len(sentence_evens))
        res = {sentence_odds[i]: sentence_evens[i] for i in range(it_length)}
        return [a + b for a, b in res.items()]

    @staticmethod
    def _remove_line_breaks(sentence_list: list) -> list:
        patt2 = re.compile(r"[\n ]+")
        return [re.sub(patt2, " ", item) for item in sentence_list]

    @staticmethod
    def _rebuild_word_list(sentence_list: list) -> list:
        new_sentence_list = []
        for s in sentence_list:
            word_list = re.split(r"\s+", s)
            word_list = [item for item in word_list if item]
            new_sentence_list.append(word_list)
        return [item for item in new_sentence_list if item]

    @staticmethod
    def _build_word_set(word_list: list) -> set:
        word_set = set(word_list)
        word_set.discard('')
        return word_set
