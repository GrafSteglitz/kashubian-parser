"""
@module
"""
import re


class Preprocessor:
    """A class to preprocess the Kashubian text for subsequent analysis."""
    def __init__(self):
        self.data = ''
        self.word_list = []
        self.sentence_list = []
        self.word_set = set()

    def __get_word_list(self):
        # split text into words
        self.word_list = re.split(r"[\n.\s,\"\-]+", self.data)
        pattern = re.compile(r"[\d!#%&'()*+,\-./:;<=>?@\[\]^_{|}~„”…–]+")
        # remove punctuation and numbers
        self.word_list = [re.sub(pattern, "", item).lower() for item in self.word_list]
        self.word_list = [item for item in self.word_list if item]

    def __get_sentences(self):
        dash = chr(8211)
        sentence_splitter = re.compile(r"( *[.?!…" + dash + "])+ *")
        self.sentence_list = re.split(sentence_splitter, self.data)
        sentence_odds = self.sentence_list[::2]
        sentence_evens = self.sentence_list[1:][::2]
        it_length = min(len(sentence_odds), len(sentence_evens))
        # temp_dict = {}
        res = {sentence_odds[i]: sentence_evens[i] for i in range(it_length)}
        new_list = []
        for a, b in res.items():
            new_list.append(a + b)
        self.sentence_list = new_list

    def __remove_line_breaks(self):

        # remove line-breaks from each sentence
        patt2 = re.compile(r"[\n ]+")
        self.sentence_list = [re.sub(patt2, " ", item) for item in self.sentence_list]

    def __rebuild_word_list(self):
        new_sentence_list = []

        for s in self.sentence_list:
            word_list = re.split(r"\s+", s)
            # purge empty strings
            word_list = [item for item in word_list if item]
            new_sentence_list.append(word_list)

        # purge empty sentences
        self.sentence_list = [item for item in new_sentence_list if item]

    def __build_word_set(self):

        # word_list still contains empty strings
        # build a set of all words in the corpus
        self.word_set = set(self.word_list)
        if '' in self.word_set:
            self.word_set.remove('')
        # self.get_word_stats()

    def preprocess(self):
        """
        A method to automatically preprocess the imported text for further analysis.
        :return:
        """
        # split text into words
        self.__get_word_list()
        self.__get_sentences()
        self.__remove_line_breaks()
        self.__rebuild_word_list()
        self.__build_word_set()
