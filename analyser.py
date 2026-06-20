"""
@module
"""
import re

from data_handler import DataHandler
from db_handler import DBHandler
from file_handler import FileHandler
from helpers import make_list, reverse_by_length, update_vals
from mongo_handler import MongoConnection
from morphemes import noun_suffixes, \
    adjective_suffixes, verb_prefixes
from output_stats import OutputStats
from parsesyntax import ParseSyntax
from preprocessor import Preprocessor
from tokenizer import Tokenizer
from loggers.loggings import logger

logger.info('Loaded analyser.py')


class Analyser(DataHandler):
    """
    @class
    A class that conducts analysis of a Kashubian-language prose text.
    """

    def __init__(self, data, use_db, text_name):
        self.data = data
        self.text_name = text_name
        self.suffixes = noun_suffixes
        self.vprefs = verb_prefixes
        self.results = {}
        self.regexes = {'consonants': r'wrtpsdfghklzcbnmżń', 'vowels': r'aeéëùuòóôãą'}

        ignores = FileHandler(in_file='ConfigFiles/ignores.txt')
        custom_ignores_dict = ignores.read_lines()

        # intermediate pipeline results stored so final_stats() can be called after do_analyse()
        self._word_list = []
        self._big_list = []

        self.preprocessor = Preprocessor()
        db_handler = DBHandler() if use_db else None
        self.tokenizer = Tokenizer(db_handler=db_handler, custom_ignores_dict=custom_ignores_dict)
        self.syntax_parser = ParseSyntax()
        self.stats = OutputStats()

    def do_analyse(self):
        """

        :return:
        """
        preprocessed = self.preprocessor.preprocess(self.data)
        self._word_list = preprocessed.word_list

        self.stats.record_word_stats(preprocessed.word_list, preprocessed.word_set)

        self._big_list = self.tokenizer.tokenize(preprocessed.sentence_list)
        self._build_morph_dict()
        self.syntax_parser.parse(self._big_list)

        out_corpus = {self.text_name: self._big_list}
        m = MongoConnection()
        m.insert(out_corpus)
        self.stats.get_collocations()

        return self._big_list

    def final_stats(self):
        """

        :return:
        """
        self.stats.final_stats(self._big_list, self._word_list)

    def _build_morph_dict(self):
        """

        :return:
        """
        for s_list in self._big_list:
            for w_index, word_type in enumerate(s_list):

                def parse(index, word):
                    if isinstance(word, dict):
                        if 'ignore' in word:
                            if not word['ignore']:
                                self.adj_parse(word, index)

                if isinstance(word_type, dict):
                    parse(w_index, word_type)
                elif isinstance(word_type, list):
                    for each in word_type:
                        parse(w_index, each)

        logger.info("Built dictionary")

    def adj_parse(self, in_dict, w_index):
        """

        :param in_dict:
        :param w_index:
        :return:
        """
        in_dict.update({'index': w_index})
        stem = ''
        ending = ''

        if 'morph' in in_dict and in_dict['morph']:
            stem = in_dict['morph'][0]
            ending = in_dict['morph'][-1]
        word = in_dict['value']

        patt_praet = re.compile(r'ł[aeoë]$|lë$')
        if re.search(patt_praet, word):
            result = self.get_praet(word)
            if result:
                in_dict.update(result)
                in_dict['syntax_resolved'] = True
                return

        if self.check_adj_stem(stem, ending, in_dict) or self.check_s_indefs(word, in_dict):
            in_dict['syntax_resolved'] = True

    def check_s_indefs(self, word, in_dict):
        """
        Looks for s-indefinites (i.e. cos, chtos, kògòs, etc.)
        :param word: word to check
        :param in_dict: word dictionary to update
        :return: True if an s-indefinite is located
        """
        adjs = self.dict_to_reverse_list(adjective_suffixes)
        s_indefs = {'co': 'wh:nom:acc'}
        if word.endswith('s'):
            infl_stem = word[0:-1]
            if infl_stem in s_indefs:
                in_dict['attrs'] = make_list(s_indefs[infl_stem]) + make_list('s-indef')
                in_dict['morph'] = [infl_stem, 's']
                return True
            for a in adjs:
                if infl_stem.endswith(a):
                    stem = re.sub(a, '', infl_stem, 1)
                    if stem in ['jacz', 'cz', 'jak', 'czedë', 'jakò']:
                        in_dict['attrs'] = make_list(adjective_suffixes[a]) + make_list('s-indef')
                        in_dict.update({'morph': [stem, a, 's']})
                        return True
        return False

    def check_adj_stem(self, stem, ending, in_dict):
        """

        :param stem: word stem (str)
        :param ending: word ending (str)
        :param in_dict: word dict to be examined
        :return: True if found, False
        """
        adjs = self.dict_to_reverse_list(adjective_suffixes)
        if not ending or ending not in adjs:
            return False

        adj_patts = {'pact': 'ąc',
                     'ppas': 'ón'}

        def check_adj_stem(adj_attr, in_patt):
            in_patt = re.compile(fr'{in_patt}$')
            if re.search(in_patt, stem):
                in_dict['attrs'] = make_list(adj_attr)
                return True
            return False

        for k, v in adj_patts.items():
            if check_adj_stem(k, v):
                return True
        return False

    def get_praet(self, word):
        """

        :param word:
        :return:
        """
        praet_dict = {
            "ła": "praet:sg:f",
            "ł": "praet:sg:m",
            "ło": "praet:sg:n",
            "lë": "praet:pl:m1",
            "łë": "praet:pl:m2:m3:f:n"
        }
        praet_list = reverse_by_length(praet_dict)
        for item in praet_list:
            if re.search(item, word):
                split_patt = fr'({item})$'
                split = re.split(split_patt, word)
                split = [a for a in split if a]
                vowel_patt = re.compile(r'([aoë]$)')
                if re.search(vowel_patt, split[-1]):
                    new_endings = re.split(vowel_patt, split[-1])
                    new_endings = [a for a in new_endings if a]
                    split.pop()
                    for each in new_endings:
                        split.append(each)
                out = make_list(praet_dict[item])
                out_dict = {'attrs': out, 'morph': split}
                return out_dict
        return None

    def check_unresolveds(self):
        """

        :return:
        """
        for sentence in self._big_list:
            for word in sentence:
                if not word['syntax_resolved'] or len(word['attrs']) > 1:
                    self.cross_examine(word)

    def cross_examine(self, word_dict):
        """

        :param word_dict:
        :return:
        """
        try:
            word_dict.update({})
        except TypeError:
            logger.warning('No dictionary provided!')
        stem = ''
        word_family = []
        if 'morph' in word_dict:
            stem = word_dict['morph'][0]
        for each in self.stats._word_set:
            if each.startswith(stem):
                word_family.append(each)
        if len(word_family) > 2:
            self.match_paradigm(word_dict, word_family)


if __name__ == '__main__':
    my_dict = {'types': ['cat', 'mouse', 'pigeon', 'coyote'], 'foods': ['chicken', 'raisins', 'seeds', 'rabbit']}
    next_dict = {'types': ['walrus', 'camel', 'cat', 'pigeon']}
    my_new_dict = update_vals(my_dict, next_dict)
    print(my_new_dict)
