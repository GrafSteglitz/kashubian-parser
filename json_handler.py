import json
# import re


# def txt_to_json(in_file):
#     f = open(in_file)
#     f_content = f.read()
#     f.close()
#     sentences_list = re.split('\\.+\\s* ', f_content)
#
#     out_d = {}
#     for count, s in enumerate(sentences_list):
#         word_split = s.split()
#         name = 's' + str(count)
#         out_d.update({name: {'word_list': word_split}})
#         for c, w in enumerate(word_split):
#             w_name = 'w' + str(c)
#             w_dict = {w_name: {'text': w, 'attrs': '', 'base': ''}}
#             out_d[name].update(w_dict)
#
#     return out_d


def write_json(in_json, out_file, offset=0):
    # x = json.dumps(source, indent=4)
    with open(out_file, 'w') as outfile:
        json.dump(in_json, outfile, ensure_ascii=False, indent=offset)


# def correct_json(in_data):
#     iterables = [list, tuple]
#     if isinstance(in_data, dict):
#         _looper(in_data.values())
#     if isinstance(in_data, set):
#         in_data = list(in_data)
#         _looper(in_data)
#     if type(in_data) in iterables:
#         _looper(in_data)
#
#
# def _looper(in_iterable):
#     # my_iter = [a]
#     # in_iterable = [list(a) for a in in_iterable if isinstance(a, set)]
#     sets = [a for a in in_iterable if isinstance(in_iterable, set)]
#     sets = [list(a) for a in sets]
#     not_sets = [a for a in in_iterable if not isinstance(in_iterable, set)]


# if __name__ == '__main__':
#     # write_json('corpus_test.json', json_dic)
#     # json_dic = dict({'s1': dict()})
#     # h = txt_to_json('./Texts/example.txt')
#     # write_json('corpus_test.json', h)
#     d = {'value': 'dnia', 'morph': ['dni', 'a'], 'attrs': [{'sg', 'nom', 'f', 'subst'}, {'acc', 'm1', 'm2', 'subst',
#          'sg', 'gen'}], 'index': 1, 'ignore': False, 'syntax_resolved': False}
#     correct_json(d)
#     print(d)
