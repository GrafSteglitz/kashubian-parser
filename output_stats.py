"""
@module
"""
from loggers.loggings import logger

class OutputStats:
    """
    A class to produce statistics about a given Kashubian text prior to parsing.
    """
    def __init__(self):
        self.stats_dict = {}
        self.stats_list = []
        self.unparsed = []
        self._word_list = []
        self._word_set = set()

    def record_word_stats(self, word_list: list, word_set: set):
        """
        Compute and write word frequency statistics.
        :param word_list: flat list of all words in the corpus
        :param word_set: set of unique words
        """
        self._word_list = word_list
        self._word_set = word_set
        self.stats_dict = {k: '' for k in word_set}
        for each in word_list:
            self.stats_dict[each] = word_list.count(each)
        self.get_most_frequent()

    def get_most_frequent(self, rank=50):
        """
        Returns the most frequent words in the corpus.
        :param rank:
        :return:
        """
        freq_list = []
        for k, v in self.stats_dict.items():
            new_dict = {k: v}
            freq_list.append(new_dict)

        def by_freq(e):
            x = list(e.values())[0]
            return x

        freq_list.sort(reverse=True, key=by_freq)
        rank = min(rank, len(freq_list) - 1)

        self.stats_list = freq_list
        self.write_freqs()

    def write_freqs(self):
        """
        Write most frequent words to a file.
        :return:
        """
        with open('./output/word_frequencies.txt','w',encoding='utf-8') as f:
            def unpack(d):
                l = list(d.items())[0]
                return l

            for each in self.stats_list:
                f.write(f'{unpack(each)[0]} {unpack(each)[1]}\n')

    def get_collocations(self):
        """
        Retrieve a list of the most common collocations in the text.
        :return:
        """
        if not self._word_set or not self._word_list:
            self.get_most_frequent()

        for stats_dict in self.stats_list:
            pass

    def final_stats(self, big_list: list):
        """
        :param big_list: annotated corpus
        """
        self.unparsed = []
        self.ambiguous = []
        self.disambiguated = []

        for sentence in big_list:
            for word in sentence:
                n = len(word['attrs'])
                if n == 0:
                    self.unparsed.append(word)
                elif n == 1:
                    self.disambiguated.append(word)
                else:
                    self.ambiguous.append(word)

        total = len(self.unparsed) + len(self.disambiguated) + len(self.ambiguous)

        def pct(count):
            return f"{(count / total) * 100:.1f}%" if total else "0%"

        logger.info(f"Total tokens: {total}")
        logger.info(f"  Disambiguated (1 analysis):  {len(self.disambiguated):>5}  ({pct(len(self.disambiguated))})")
        logger.info(f"  Ambiguous     (2+ analyses): {len(self.ambiguous):>5}  ({pct(len(self.ambiguous))})")
        logger.info(f"  Unparsed      (no analysis): {len(self.unparsed):>5}  ({pct(len(self.unparsed))})")
