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

    def final_stats(self, big_list: list, word_list: list):
        """

        :param big_list: annotated corpus
        :param word_list: flat word list for corpus length
        """
        unparsed_count = 0
        corpus_length = len(word_list)
        self.unparsed = []
        for sentence in big_list:
            for each in sentence:
                if len(each['attrs']) > 1:
                    unparsed_count += 1
                    self.unparsed.append(each)
        percent = str((unparsed_count/corpus_length)*100) + '%'

        logger.info(f"Words unparsed: {unparsed_count}/{corpus_length} (= {percent}%)")
