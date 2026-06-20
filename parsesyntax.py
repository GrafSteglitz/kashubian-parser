"""
@module
"""
# from dataclasses import dataclass, field

from morphemes import prepositions, case


# @dataclass
class ParseSyntax:
    """
    A class to parse the syntax of Kashubian sentences.
    """
    # big_list: list = field(init=False)
    def __init__(self):
        self.big_list = []

    def syntactic_parse(self):
        """
        The method that invokes the sentence-oriented parse_sentence() method.
        :return: None
        """
        for sentence in self.big_list:
            # nxt = next(iter(self.big_list))
            self.parse_sentence(sentence)

    def parse_sentence(self, word_list):
        """

        :param word_list:
        :return:
        """
        for count, each in enumerate(word_list):
            if isinstance(each, dict) and each['value'] in prepositions:
                self.parse_on_preposition(count, each, word_list)

    def parse_on_preposition(self, index, in_dict, sentence_list):
        """

        :param index:
        :param in_dict:
        :param sentence_list:
        :return:
        """
        prerequisites = [in_dict, 'reqs' in in_dict]
        for p in prerequisites:
            if not p:
                return
        reqs = in_dict['reqs']

        def jump(offset=1):
            new_index = index + offset
            # if new_index > len(sentence_list) - 1:
            #     new_index = len(sentence_list) - 1
            new_index = min(new_index, len(sentence_list) - 1)
            return sentence_list[new_index]

        # # loop through words in the sentence while they match the reqs specified by the preposition
        # # break on the first word that does not match
        found_req = None
        for req in reqs:
            if found_req:
                break
            i = 1
            while i < len(sentence_list):
                skip_list = ['coord']
                next_word = jump(i)
                if self.check_reqs(req, next_word):
                    found_req = req
                    break
                # skip coordinating conjunctions and keep looking
                if not self.attrs_contains('coord', next_word['attrs']):
                    break
                i += 1

        if found_req:
            in_dict['reqs'] = [found_req]

    @staticmethod
    def attrs_contains(search_attr, attrs_list):
        """

        :param search_attr:
        :param attrs_list:
        :return:
        """
        for sublist in attrs_list:
            if search_attr in sublist:
                return True
        return False

    @staticmethod
    def check_reqs(req, in_word_dict):
        """

        :param req:
        :param in_word_dict:
        :return:
        """
        attrs_list = in_word_dict['attrs']
        try:
            _ = (e for e in attrs_list)
        except TypeError:
            print(f'{attrs_list} is not iterable')

        # checking for conjunctions (they have no bearing on case usage)
        if in_word_dict['value'] == 'i':
            # print('i')
            pass
        list_of_match_sets = []

        for attrs_set in attrs_list:
            if attrs_set is None:
                continue
                # print('attrs_set is not iterable')
            if req in attrs_set:
                current_list = [a for a in attrs_set if a not in case and a != req]
                current_list.append(req)
                list_of_match_sets.append(current_list)

        if list_of_match_sets:
            in_word_dict['attrs'] = list_of_match_sets
            in_word_dict['syntax_resolved'] = True
            return True

        return False
