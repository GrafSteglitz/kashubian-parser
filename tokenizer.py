"""
@module
"""
import re
# from dataclasses import dataclass, field

from db_handler import DBHandler
from helpers import make_list, merge_dicts
from loggers.loggings import logger
from morphemes import (prepositions, noun_suffixes, \
                       adjective_suffixes, verb_suffixes, przek, qub, subord_conj, coord_conj, wiedzec,
                       personal_pronouns, reflexive_pronouns, ten, chto, nicht, byc, byc_past, byc_future,
                       make_attrs_dict, get_dict_vals_as_list)


# @dataclass
class Tokenizer(DBHandler):
    """
    A class to tokenize a preprocessed text (see class Preprocessor).
    """
    # sentence_list: list = field(init=False)
    # big_list: list = field(init=False)
    # custom_ignores_dict: dict = field(init=False)
    # use_db: bool
    def __init__(self, use_db):
        super().__init__()
        self.sentence_list = []
        self.big_list = []
        self.custom_ignores_dict = {}
        self.use_db = use_db



    def tokenize(self):
        """
        Public method to tokenize the text.
        :return:
        """

        for count1, s in enumerate(self.sentence_list):
            self.big_list.append([])
            current_sentence = self.big_list[count1]

            for count2, orth in enumerate(s):
                word = orth.lower()
                punct_num_patt = re.compile(r"[\d!#,%&'()*+\-./:;<=>?@\[\]^_{|}~„”–]+")
                word = re.sub(punct_num_patt, "", word)
                # get a dict object for each word in sentence
                word_dict = {'orth': orth, 'value': word, 'morph': [word], 'attrs': [], 'index': count2,
                             's_index': count1,
                             'ignore': False, 'syntax_resolved': False}

                # check for immutables and monomorphs

                presets_match_dict = self.check_presets(word)
                if presets_match_dict:
                    word_dict.update(presets_match_dict)
                    current_sentence.append(word_dict)
                    continue
                match_endings = self.check_ending(word, word_dict)
                if match_endings:
                    word_dict.update(match_endings)

                current_sentence.append(word_dict)

        # ltc = len(self.tokenized_corpus)
        # lwl = len(self.word_list)
        #
        # if ltc != lwl:
        #     logging.warning(f"Corpus tagging error: len(self.tokenized_corpus) {ltc} != len(self.word_list) {lwl}")

        logger.info("List built / corpus tokenized!")
        # write_json(self.big_dict, './JSON/corpus_output.json')

    def check_presets(self, in_word):
        """

        :param in_word:
        :return:
        """
        found_dict = {}

        def add_to_attrs(in_attr):
            if not in_attr:
                return
            if 'attrs' not in found_dict:
                found_dict.update({'attrs': []})
            found_dict.update({'ignore': True})
            try:
                found_dict['attrs'] += make_list(in_attr)
            except KeyError:
                print("no key 'attrs' in found_dict")

        if in_word in self.custom_ignores_dict:
            add_to_attrs(self.custom_ignores_dict[in_word])
            return found_dict

        attrs_dict = {'coord': coord_conj,
                      'subord': subord_conj,
                      'qub': qub,
                      'przek': przek
                      }
        dict_list = [reflexive_pronouns, self.custom_ignores_dict, wiedzec, ten, chto,
                     nicht, byc, byc_past, byc_future]
        for d in dict_list:
            if in_word in d.keys():
                found_dict.update({'attrs': make_list(d[in_word]), 'ignore': True})
                if 'base' in d.keys():
                    found_dict.update({'base': d['base']})

        for k, each in attrs_dict.items():
            if in_word in each:
                add_to_attrs(k)

        if in_word in prepositions:
            found_dict.update({'reqs': re.split(":", prepositions[in_word]), 'attrs': ['prep'], 'ignore': True})

        if in_word in personal_pronouns:
            pps = personal_pronouns
            add_to_attrs(pps[in_word]['attrs'])
            found_dict.update({'base': pps[in_word]['base'], 'ignore': True})

        return found_dict

    def check_ending(self, in_word, in_dict):
        """

        :param in_word:
        :param in_dict:
        :return:
        """
        # prepare suffixes_list
        suffix_dict_list = [noun_suffixes, adjective_suffixes, verb_suffixes]
        all_suffixes_dict = merge_dicts(suffix_dict_list)
        suffixes_list = list(all_suffixes_dict.keys())

        # set to get uniques then list the suffixes again so we can reorder them
        suffixes_list = list(set(suffixes_list))

        def sorter(e):
            return len(e)

        suffixes_list.sort(reverse=True, key=sorter)

        # block below ensures no praets are caught accidentally
        praet_patt = re.compile(r'.+ł[ao]*$|.+lë$')
        # [aeioë]

        if self.search(praet_patt, in_word):
            in_dict.update({'ignore': False})
            in_dict['attrs'].append(['praet'])
            return in_dict

        for morph in suffixes_list:
            if in_word.endswith(morph):
                patt = re.compile(r"(" + morph + "$)")
                tokens = re.split(patt, in_word)

                tokens = [a for a in tokens if a]
                # here could be the place to start a stem check
                # self._check_adj_stem()
                # self.tokenized_corpus.append(tokens)
                attrs = make_list(all_suffixes_dict[morph])
                new_attrs = [make_attrs_dict(a) for a in attrs]

                in_dict.update({'value': in_word, 'morph': tokens, 'attrs': attrs})

                query = in_dict['morph'][0]
                list_from_db = []
                if self.use_db:
                    list_from_db = self._check_morph_with_db(query)


                if list_from_db:
                    db_attrs = make_attrs_dict(list_from_db)
                    new_attrs = self.merge_attrs(db_attrs, new_attrs)

                in_dict['attrs'] = new_attrs

                return in_dict

        # self.tokenized_corpus.append(make_list(in_word))
        return {}

    @staticmethod
    def search(pattern, string):
        """

        :param pattern: regex pattern
        :param string: string to search
        :return: search object if found, else None
        """
        return re.search(pattern, string)

    def merge_attrs(self, db_attrs, morph_parse_attrs):
        """

        :param db_attrs:
        :param morph_parse_attrs:
        :return:
        """
        delete_list = []
        db_attrs_set = set(get_dict_vals_as_list(db_attrs))
        for analysis in morph_parse_attrs:

            compare_set = set(get_dict_vals_as_list(analysis))
            if not db_attrs_set.issubset(compare_set):
                delete_list.append(analysis)

        if delete_list:
            morph_parse_attrs = [x for x in morph_parse_attrs if x not in delete_list]
        morph_parse_attrs = [self.purge_attrs(db_attrs, a) for a in morph_parse_attrs]
        return morph_parse_attrs if morph_parse_attrs else [db_attrs_set]

    @staticmethod
    def purge_attrs(db_attrs, analysis):
        """

        :param db_attrs:
        :param analysis:
        :return:
        """
        # db_keys = db_attrs.keys()
        for k in db_attrs.keys():
            if k in analysis.keys():
                this_new_attrs_list = [a for a in analysis[k] if a in db_attrs[k]]
                analysis[k] = this_new_attrs_list
        return analysis
        # def purge_attrs(this_attrs_list):
        #     pos_dict = {'subst': gender.keys()}
        #     removes_list = []
        #     for each in this_attrs_list:
        #         if each
        #     def check_pos():
        #         pass
        #
        #     new_list = [a for a in this_attrs_list if a in db_attrs]
        #     return new_list
        #
        # parse_dict = {k: purge_attrs(v) for k, v in analysis.items()}
        # return parse_dict
