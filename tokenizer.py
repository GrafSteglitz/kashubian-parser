"""
@module
"""
import re

from helpers import make_list, merge_dicts

# Defined via chr() to avoid Python 3.12+ treating „" (U+201E/U+201D) as string delimiters.
_TYPOGRAPHIC_PUNCT = chr(8222) + chr(8221) + chr(8211)  # „"–
from loggers.loggings import logger
from morphemes import (prepositions, noun_suffixes, \
                       adjective_suffixes, verb_suffixes, przek, qub, subord_conj, coord_conj, wiedzec,
                       personal_pronouns, reflexive_pronouns, ten, chto, nicht, byc, byc_past, byc_future,
                       make_attrs_dict, get_dict_vals_as_list)


class Tokenizer:
    """
    A class to tokenize a preprocessed text (see class Preprocessor).
    """
    def __init__(self, db_handler=None, custom_ignores_dict=None):
        self.db_handler = db_handler
        self.use_db = db_handler is not None
        self.custom_ignores_dict = custom_ignores_dict or {}

    def tokenize(self, sentence_list: list) -> list:
        """
        Tokenize a preprocessed sentence list.
        :param sentence_list: list of sentences, each a list of word strings
        :return: annotated big_list
        """
        big_list = []
        for count1, s in enumerate(sentence_list):
            big_list.append([])
            current_sentence = big_list[count1]

            for count2, orth in enumerate(s):
                word = orth.lower()
                punct_num_patt = re.compile(r"[\d!#,%&'()*+\-./:;<=>?@\[\]^_{|}~" + _TYPOGRAPHIC_PUNCT + "]+")
                word = re.sub(punct_num_patt, "", word)
                word_dict = {'orth': orth, 'value': word, 'morph': [word], 'attrs': [], 'index': count2,
                             's_index': count1,
                             'ignore': False, 'syntax_resolved': False}

                presets_match_dict = self.check_presets(word)
                if presets_match_dict:
                    word_dict.update(presets_match_dict)
                    current_sentence.append(word_dict)
                    continue
                match_endings = self.check_ending(word, word_dict)
                if match_endings:
                    word_dict.update(match_endings)

                current_sentence.append(word_dict)

        logger.info("List built / corpus tokenized!")
        return big_list

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
        suffix_dict_list = [noun_suffixes, adjective_suffixes, verb_suffixes]
        all_suffixes_dict = merge_dicts(suffix_dict_list)
        suffixes_list = list(all_suffixes_dict.keys())

        suffixes_list = list(set(suffixes_list))

        def sorter(e):
            return len(e)

        suffixes_list.sort(reverse=True, key=sorter)

        praet_patt = re.compile(r'.+ł[ao]*$|.+lë$')

        if self.search(praet_patt, in_word):
            in_dict.update({'ignore': False})
            in_dict['attrs'].append(['praet'])
            return in_dict

        for morph in suffixes_list:
            if in_word.endswith(morph):
                patt = re.compile(r"(" + morph + "$)")
                tokens = re.split(patt, in_word)

                tokens = [a for a in tokens if a]
                attrs = make_list(all_suffixes_dict[morph])
                new_attrs = [make_attrs_dict(a) for a in attrs]

                in_dict.update({'value': in_word, 'morph': tokens, 'attrs': attrs})

                query = in_dict['morph'][0]
                list_from_db = []
                if self.use_db and self.db_handler:
                    list_from_db = self.db_handler._check_morph_with_db(query)

                if list_from_db:
                    db_attrs = make_attrs_dict(list_from_db)
                    new_attrs = self.merge_attrs(db_attrs, new_attrs)

                in_dict['attrs'] = new_attrs

                return in_dict

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
        for k in db_attrs.keys():
            if k in analysis.keys():
                this_new_attrs_list = [a for a in analysis[k] if a in db_attrs[k]]
                analysis[k] = this_new_attrs_list
        return analysis
