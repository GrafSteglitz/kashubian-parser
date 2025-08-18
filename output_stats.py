"""
@module
"""
from loggers.loggings import logger

class OutputStats:
    """
    A class to produce statistics about a given Kashubian text prior to parsing.
    """

    # word_set: set = field(init=False)
    # word_list: list = field(init=False)
    # stats_dict: dict = field(init=False)
    # stats_list: list = field(init=False)
    # unparsed: list = field(init=False)
    # big_list: list = field(init=False)
    def __init__(self):
        self.word_set = set()
        self.word_list = []
        self.stats_dict = {}
        self.stats_list = []
        self.unparsed = []
        self.big_list = []

    def get_word_stats(self):
        """
        A method that wraps get_most_frequent()
        :return:
        """
        self.stats_dict = {k: '' for k in self.word_set}

        for each in self.word_list:
            self.stats_dict[each] = self.word_list.count(each)
        self.get_most_frequent()

    def get_most_frequent(self, rank=50):
        """
        Returns the most frequent words in the corpus.
        :param rank:
        :return:
        """
        # self.stats_list = [k,v for k,v in self.stats_dict.items()]
        freq_list = []
        for k, v in self.stats_dict.items():
            new_dict = {k: v}
            freq_list.append(new_dict)

        def by_freq(e):
            x = list(e.values())[0]
            return x

        freq_list.sort(reverse=True, key=by_freq)
        rank = min(rank, len(freq_list) - 1)

        # print(freq_list[0:rank])
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
                f.write(f'{unpack(each)[0]} {unpack(each)[1]}')

    def get_collocations(self):
        """
        Retrieve a list of the most common collocations in the text.
        :return:
        """
        if not self.word_set or not self.word_list:
            self.get_most_frequent()

        for stats_dict in self.stats_list:
            pass

    def final_stats(self):
        """

        :return:
        """
        unparsed_count = 0
        corpus_length = len(self.word_list)
        self.unparsed = []
        for sentence in self.big_list:
            for each in sentence:
                if len(each['attrs']) > 1:
                    unparsed_count += 1
                    self.unparsed.append(each)
        percent = str((unparsed_count/corpus_length)*100) + '%'

        logger.info(f"Words unparsed: {unparsed_count}/{corpus_length} (= {percent}%)")
        # logger.info("Words unparsed: d%/d% (= s%)",unparsed_count,corpus_length,percent)