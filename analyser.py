"""
@module
"""
import re

from data_handler import DataHandler
# ignore_list, ignore_particles, byc, byc_past, byc_future, miec, co, nic, num
from file_handler import FileHandler
from helpers import make_list, reverse_by_length, update_vals
from mongo_handler import MongoConnection
# from morphemes import *
from morphemes import noun_suffixes, \
    adjective_suffixes, verb_prefixes
from output_stats import OutputStats
from parsesyntax import ParseSyntax
from preprocessor import Preprocessor
from tokenizer import Tokenizer
from loggers.loggings import logger

# from dataclasses import dataclass, field

# from copy import deepcopy

logger.info('Loaded analyser.py')

# @dataclass
class Analyser(Preprocessor, OutputStats, Tokenizer, ParseSyntax, DataHandler):
    """
    @class
    A class that conducts analysis of a Kashubian-language prose text.
    """
    # data: str
    # use_db: bool
    # big_list: list = field(init=False)

    def __init__(self, data, use_db, text_name):
        super().__init__()
        self.data = data
        self.use_db = use_db
        self.text_name = text_name
        self.suffixes = noun_suffixes

        ignores = FileHandler(in_file='ConfigFiles/ignores.txt')
        self.custom_ignores_dict = ignores.read_lines()

        self.vprefs = verb_prefixes

        self.results = {}

        self.regexes = {'consonants': r'wrtpsdfghklzcbnmżń', 'vowels': r'aeéëùuòóôãą'}
        self.big_list = []

    def do_analyse(self):
        """

        :return:
        """
        self.preprocess()
        self.get_word_stats()
        self.tokenize()
        self.build_morph_dict()
        self.syntactic_parse()
        # self.check_unresolveds()
        out_corpus = {self.text_name: self.big_list}
        m = MongoConnection()
        m.insert(out_corpus)
        self.get_collocations()
        # write_json(out_corpus, './JSON/corpus_output.json')

        return self.big_list

    def build_morph_dict(self):
        """

        :return:
        """
        for s_list in self.big_list:
            for w_index, word_type in enumerate(s_list):

                def parse(index, word):
                    if isinstance(word, dict):
                        if 'ignore' in word:
                            if not word['ignore']:
                                self.adj_parse(word, index)
                                # self.syntactic_parse(w_index, value)

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
        # do some regexes to identify obvious categories

        in_dict.update({'index': w_index})
        patt_ck = re.compile(r'.+[tdrc][gk]$')
        # patt_gk = re.compile(r'[gk]$')
        stem = ''
        ending = ''

        # if 'attrs' in in_dict:
        #     if in_dict['attrs'][0] in ignore_cats:
        #         return
        if 'morph' in in_dict and in_dict['morph']:
            stem = in_dict['morph'][0]
            ending = in_dict['morph'][-1]
        word = in_dict['value']
        # ending = in_dict['morph'][-1]
        # morphological categories for the method to ignore

        # if self.search(patt_ck, word):
        #     in_dict['attrs'] = make_list('subst:m3:nom:acc')
        #     in_dict['syntax_resolved'] = True
        #     return
        # elif self.search(patt_gk, word):
        #     in_dict['attrs'] = self.attributes_to_list('subst:m:nom')

        patt_praet = re.compile(r'ł[aeoë]$|lë$')
        if self.search(patt_praet, word):
            result = self.get_praet(word)
            if result:
                in_dict.update(result)
                in_dict['syntax_resolved'] = True
                return

        # check if has adj ending then check if participle

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
                # in_dict['syntax_resolved'] = True
                return True
            for a in adjs:
                if infl_stem.endswith(a):
                    stem = re.sub(a, '', infl_stem, 1)
                    if stem in ['jacz', 'cz', 'jak', 'czedë', 'jakò']:
                        in_dict['attrs'] = make_list(adjective_suffixes[a]) + make_list('s-indef')
                        # in_dict['syntax_resolved'] = True
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

        # for a in adjs:
        #     # check for adjectives and participle adjectives
        #     adj_regex = fr'{a}$'
        #     if self.search(adj_regex, ending):
        #         # now check the stem

        def check_adj_stem(adj_attr, in_patt):
            in_patt = re.compile(fr'{in_patt}$')
            if self.search(in_patt, stem):
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
            if self.search(item, word):
                split_patt = fr'({item})$'
                split = re.split(split_patt, word)
                split = [a for a in split if a]
                vowel_patt = re.compile(r'([aoë]$)')
                if self.search(vowel_patt, split[-1]):
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
        for sentence in self.big_list:
            for word in sentence:
                if not word['syntax_resolved'] or len(word['attrs']) > 1:
                    self.cross_examine(word)

    # @staticmethod
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
        for each in self.word_set:
            if each.startswith(stem):
                word_family.append(each)
        if len(word_family) > 2:
            self.match_paradigm(word_dict, word_family)


if __name__ == '__main__':
    # task = Analyser()
    # print(task.process_attributes("ppron:3:dat:loc:sg:m2:m3:f:n"))
    # my_set = {'1', '2', '3', '4'}
    # reverse_by_length(my_set)
    # make_attrs_dict(['adj', 'n', 'nom', 'acc', 'sg'])
    # print(merge_dicts([noun_suffixes, adjective_suffixes]))
    # task.get_adjective("mieszkanié")
    # task.db_lookup("gòsc%")
    # print(make_list(noun_suffixes['a']))
    my_dict = {'types': ['cat', 'mouse', 'pigeon', 'coyote'], 'foods': ['chicken', 'raisins', 'seeds', 'rabbit']}
    next_dict = {'types': ['walrus', 'camel', 'cat', 'pigeon']}
    my_new_dict = update_vals(my_dict, next_dict)
    print(my_new_dict)
