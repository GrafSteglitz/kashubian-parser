"""
@module
"""

import re
import logging

from morphemes import pos, validator_tree


def get_other_keys(target, keys):
    """

    :param target:
    :param keys:
    :return:
    """
    if not target or not keys:
        return {}
    if not isinstance(target, dict):
        return {}
    for x in keys:
        if x in target.keys():
            target.pop(x)

    return target


def clean_structure(in_dict):
    """

    :param in_dict:
    :return:
    """
    if not isinstance(in_dict, dict):
        return

    delete = []
    for key, val in in_dict.items():
        if val in ('', {}):
            delete.append(key)
    for i in delete:
        del in_dict[i]

    for y in in_dict.values():
        if isinstance(y, dict):
            clean_structure(y)


def reverse_dict(in_dict):
    """
    Function to reverse a dictionary.
    :param in_dict:
    :return:
    """
    return {v: k for k, v in in_dict.items()}


def merge_dicts(dict_list):
    """

    :param dict_list:
    :return:
    """
    new_dict = {}
    for d in dict_list:
        for key, val in d.items():
            if key not in new_dict:
                new_dict.update({key: val})

            # if the key is in the new_dict, and the value of the identical key in d is not False, create a tuple
            # with both values and add them to new_dict
            elif key in new_dict:
                if not new_dict[key] and not val:
                    new_dict[key] = ''
                new_list = [val, new_dict[key]]
                value_list = [a for a in new_list if a]
                comp_list = []
                for x in value_list:
                    if isinstance(x, tuple):
                        comp_list = comp_list + list(x)
                    elif isinstance(x, str):
                        comp_list.append(x)

                new_tuple = tuple(comp_list)
                new_dict[key] = new_tuple
            # elif key in new_dict.keys():
            #     new_dict[key]

    return new_dict


def attrs_from_str(in_str):
    """

    :param in_str:
    :return:
    """
    out_list = re.split(r':', in_str)
    return out_list


def make_list(in_type):
    """

    :param in_type: string or tuple
    :return: a list of one ore more lists
    """
    if isinstance(in_type, tuple):
        return [re.split(r':', each) for each in list(in_type)]
    # creates a list and adds the word to it
    # then returns the list
    if isinstance(in_type, str):
        return [re.split(r':', in_type)]

    return []


# def make_attrs_dict(in_list):
#     attrs_dict = {}
#     cats = [pos, number, case, gender, person, degree, accentuation]
#     for attr in in_list:
#         for item in cats:
#             for each in item.keys():
#                 if attr == 'id':
#                     continue
#                 if attr == each:
#                     if not item['id'] in attrs_dict:
#                         attrs_dict.update({item['id']: []})
#                     attrs_dict[item['id']].append(attr)
#     return attrs_dict


def reverse_by_length(in_type):
    """

    :param in_type:
    :return:
    """

    def sorter(e):
        return len(e)

    allowed_types = [list, dict]
    if isinstance(in_type, list):
        in_type.sort(reverse=True, key=sorter)
        return in_type
    if isinstance(in_type, dict):
        key_list = list(in_type.keys())
        key_list.sort(reverse=True, key=sorter)
        return key_list
    if type(in_type) not in allowed_types:
        logging.error("Error: illegal type entered! in_type parameter must be dict or list!")


def contains_sublist(in_list):
    """

    :param in_list:
    :return:
    """
    for each in in_list:
        if isinstance(each, list):
            return True
    return False


def a_in_b(term, in_type):
    """

    :param term:
    :param in_type:
    :return:
    """
    if isinstance(in_type, list):
        if looper(term, in_type):
            return True
    elif isinstance(in_type, dict):
        if term in in_type.values():
            return True
        for v in in_type.values():
            if isinstance(v, list):
                if looper(term, v):
                    return True
    return False


def looper(term, in_list):
    """

    :param term:
    :param in_list:
    :return:
    """
    for a in in_list:
        if a == term:
            return True
        if isinstance(a, list):
            if looper(term, a):
                return True
        elif isinstance(a, dict):
            if term in a.values():
                return True
            for v in a.values():
                if isinstance(v, list):
                    if looper(term, v):
                        return True
    return False


def update_vals(old_dict, changes_dict):
    """

    :param old_dict:
    :param changes_dict:
    :return:
    """
    if not isinstance(old_dict, dict):
        return
    for each in changes_dict.keys():
        if each in old_dict and isinstance(old_dict[each], list):
            old_dict[each].append(changes_dict[each])
        else:
            old_dict.update({each: changes_dict[each]})
    return



def attributes_to_list(in_attrs):
    """

    :param in_attrs:
    :return:
    """
    if isinstance(in_attrs, tuple):
        new_list = [a.split(":") for a in in_attrs]
        return new_list
    if isinstance(in_attrs, str) and ":" in in_attrs:
        attrs_list = in_attrs.split(":")
        return attrs_list
    return make_list(in_attrs)



def update_attrs_lists(attrs_list, term):
    """

    :param attrs_list:
    :param term:
    :return:
    """
    if not attrs_list:
        return []
    for each in attrs_list:
        if term not in each:
            try:
                each.append(term)
            except AttributeError:
                print("Cannot append to str!")
    return attrs_list


# def purge_attrs_on_specified(self):
#     pass



def delete_from_attrs_lists(word_dict, term):
    """

    :param word_dict:
    :param term:
    :return:
    """
    new_attrs_list = []
    for each in word_dict['attrs']:
        if term not in each:
            continue
        each_list = list(each)
        new_list = [a for a in each_list if a != term]
        new_attrs_list.append(new_list)
    word_dict['attrs'] = new_attrs_list