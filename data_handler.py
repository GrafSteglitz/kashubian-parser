"""
@module
"""
import re

from morphemes import pos, validator_tree, number, gender, person, degree, accentuation, adjective_suffixes, \
    paradigm_list, case


class DataHandler:
    """
    A class for miscellaneous methods that handle parsing data.
    """
    @staticmethod
    def match_paradigm(word_dict, word_family):
        """

        :param word_dict:
        :param word_family:
        :return:
        """
        matched = 0
        print(word_dict)
        # word_family.append(word_dict['value'])
        total = len(word_family)
        for member in word_family:
            member_matched = False
            for p in paradigm_list:
                for k in p:
                    if member.endswith(k):
                        matched += 1
                        member_matched = True
                        break
                if member_matched:
                    break
        match_score = matched / total
        return match_score

    def make_attrs_obj(self, attrs_list):
        """

        :param attrs_list:
        :return:
        """
        duplicates = self.validate_attrs(attrs_list)
        if not duplicates:
            return []
        this_pos = ""
        for attr in attrs_list:
            if attr in pos:
                this_pos = attr
                break
        if this_pos not in validator_tree:
            print("Pos not found. Not purging, exiting...")
            return attrs_list
        new_attrs_set = {a for a in attrs_list if a in validator_tree[this_pos]}
        new_attrs_set.add(this_pos)
        return list(new_attrs_set)

    @staticmethod
    def validate_attrs(in_attrs_list):
        """

        :param in_attrs_list: a list of sublists to validate
        :return: a dict of duplicates
        """
        if not isinstance(in_attrs_list, set):
            return {}
        type_dict = {}
        duplicates = {}

        for attr in in_attrs_list:
            for cat in [pos, number, case, gender, person, degree, accentuation]:
                if attr in cat:
                    if cat['id'] not in type_dict:
                        type_dict.update({cat['id']: []})
                        type_dict[cat['id']].append(attr)
                        break

                    duplicates.update({cat['id']: type_dict[cat['id']]})
                    duplicates[cat['id']].append(attr)
        # for x, y in type_dict.items():
        #     if len(y) > 1:
        #         return False
        # return True
        return duplicates

    @staticmethod
    def process_attributes(in_attrs=""):
        """This method parses the short form of word attributes and returns a full dictionary containing them.
        :param in_attrs: attributes to process (Form = "sg:dat:m3:" etc ...)
        :return: return {} if not found, else grammatical dictionary
        """
        # w = self.word
        if not in_attrs:
            print("Analyser.process_attributes(): No attributes provided!")
            return {}
        output = {}
        # possible word attributes are listed below. All attrs must be UNIQUE!!

        attr_list = [pos, number, case, gender, person, degree, accentuation]

        in_attrs = in_attrs.split(":")

        for d in attr_list:
            output.update({d['id']: []})
            for a in list(d.keys()):
                for attr in in_attrs:
                    if a == attr:
                        output[d['id']].append(a)
        return output

    # def clean_attrs(self,attrs_list):
    #     found_cats = []
    #     for each in attrs_list:
    #         for attr in each:
    #             pass

    @staticmethod
    def get_adjective(in_word):
        """

        :param in_word:
        :return:
        """
        adjs = adjective_suffixes
        out_dict = {}
        for a in adjs:
            if in_word.endswith(a):
                if a == "é":
                    m = re.search(r"ni", in_word)
                    if m:
                        continue
                out_dict.update({in_word: {"ending": a}})
        return out_dict

    @staticmethod
    def sanitise_output():
        """

        :return:
        """
        pass

    @staticmethod
    def dict_to_reverse_list(d):
        """

        :param d:
        :return:
        """
        out_list = list(d.keys())

        def sorter(e):
            return len(e)

        out_list.sort(reverse=True, key=sorter)
        return out_list