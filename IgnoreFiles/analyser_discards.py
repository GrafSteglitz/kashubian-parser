from morphemes import *

class Discards:
    def __init__(self, in_data=None):
        self.morph = Morph()
        self.data = in_data
        self.tokenized_corpus = list()
        self.word_list = list()
        self.word_set = set()
        self.sentence_list = list()
        self.big_dict = dict()
        self.current_sentence = None
        self.possible_indeclinables = list()
        # self.allroots = list()
        # self.suffixes = read_json_file("suffix_dict.json")
        self.suffixes = noun_suffixes
        # suffix_d_list = list()
        # suffix_d_list.extend(noun_suffixes.keys())
        # self.all_suffixes_d = dict(**noun_suffixes, **adjective_suffixes, **verb_suffixes)
        foo = FileHandler(in_file='../ConfigFiles/ignores.txt')
        self.custom_ignores_dict = foo.read_lines()
        # self.ignore_set = set(ignore_list + ignore_particles + list(prepositions.keys()) + self.custom_ignores
        #                       + list(adjective_suffixes.keys()))
        self.vprefs = verb_prefixes
        # self.current_root = ''
        # self.word_result = {}
        self.results = {}
        # self.do_analyse()
        self.regexes = {'consonants': re.compile(r'[wrtpsdfghklzcbnmżń]')}


    @staticmethod
    def get_miec(in_word):
        if not in_word:
            return {}
        if in_word not in miec:
            return {}
        output = {"input": in_word, "base": "miec", "attrs": miec[in_word]}
        return output

    @staticmethod
    def get_byc(in_word):
        if not in_word:
            return {}

        bf = reverse_dict(byc_future)
        output = {"base": "bëc", "attrs": ""}

        if in_word in byc.keys():
            output["attrs"] = byc[in_word]
            return output
        if in_word in byc_past.keys():
            output["attrs"] = byc_past[in_word]
            return output

        for x, y in bf.items():
            for z in x:
                if z == in_word:
                    output["attrs"] = y
                    return output

        return {}

    @staticmethod
    def is_particle(in_word):
        if in_word in ignore_particles:
            return True
        else:
            return False

    @staticmethod
    def get_pronoun(in_word):
        """
        This method checks if word is a known pronoun
        :param in_word: Word to check
        :return: If found, returns a list containing dictionaries of possible grammatical interpretations, empty list
        if not found.
        """
        if not in_word:
            return {}
        if in_word not in personal_pronouns.keys():
            return {}

        output = personal_pronouns[in_word]

        return output

    @staticmethod
    def get_wiedzec(in_word):
        if not in_word:
            print("get_wiedzec(): No input provided!")
            return dict()
        out_dict = {}
        for key, val in wiedzec.items():
            if in_word == key:
                out_dict.update({"attrs": val})

        return out_dict

    @staticmethod
    def check_prefix(in_morph, in_word):
        """
        This method checks if a prefix is in a word
        :param in_morph:
        :param in_word:
        :return: Position word is at or False if not found
        """
        out = deepcopy(affix_res)

        if not in_word.startswith(in_morph):
            return out

        out['prefix'] = in_morph
        out['pos'] = 0
        # root = next(iter(in_word.split(in_morph)), '')
        out['root'] = re.sub(re.compile(r'^' + in_morph), '', in_word)

        return out

    @staticmethod
    def check_suffix(in_morph, in_word):
        position = in_word.find(str(in_morph))
        out = deepcopy(affix_res)
        # val = self.suffixes.get(in_morph, {})

        if not in_word.endswith(in_morph):
            return out

        out['affix'] = in_morph
        out['pos'] = position
        out['root'] = re.sub(re.compile(in_morph + r'$'), '', in_word)
        return out

    def analyse_word(self, in_word, s_position, s_num):
        """
        This method looks to match the input word with a set of grammatical forms stored in morphemes. If none are
        found, it searches for prefixes and suffixes.
        :param s_num: Index of sentence in entire text in which the word occurs
        :param s_position: Position of the word in the sentence.
        :param in_word: A string containing the word to analyse
        :return: A dict of word information on success, an empty dict on failure
                word_dict = {}
        """
        in_word = re.sub(r"[!#%&'()*+,-./:;<=>?@\[\]^_{|}~]+", "", in_word)
        in_word = in_word.lower()
        prefs_found = 0
        suffs_found = 0
        instance = 0

        word_dict = dict()
        # {instance: dict(), 'f_position': count}
        word_dict[instance] = dict()
        word_dict[instance]['prefix'] = dict()
        word_dict['s_position'] = s_position
        word_dict['s_num'] = s_num

        word_dict[instance]['suffix'] = dict()
        # START CHECK IMMUTABLES
        if in_word in self.results:
            instance += 1
            word_dict.update({instance: {in_word: dict()}})

        # check for particles
        if self.is_particle(in_word):
            word_dict[instance] = {'class': 'particle'}
            instance += 1
            word_dict.update({instance: dict()})
            # return word_dict

        # check for pronouns
        pron = self.get_pronoun(in_word)
        if pron:
            if instance > 0:
                instance += 1
            word_dict[instance] = pron
            instance += 1
            word_dict.update({instance: dict()})

        be = self.get_byc(in_word)
        if be:
            word_dict[instance].update(be)
            instance += 1
            word_dict.update({instance: dict()})

        have = self.get_miec(in_word)
        if have:
            word_dict[instance] = {'class': 'verb'}
            word_dict[instance] = {'base': 'miec'}
            instance += 1
            word_dict.update({instance: dict()})

        if instance > 0:
            # if the word was found in any of the blocks above, exit the function
            return word_dict

        for n in self.vprefs:
            prefix = self.check_prefix(n, in_word)
            if prefix['pos'] == -1:
                continue

            word_dict[instance]['prefix'][prefs_found] = prefix
            prefs_found += 1
            word_dict[instance]['prefix'][prefs_found] = dict()

        for n in self.suffixes.keys():
            root = word_dict[instance].get('prefix', {}).get('root', '')
            root = root if root else in_word
            suffix = self.check_suffix(n, root)

            if suffix['pos'] != -1:
                word_dict[instance]['suffix'][suffs_found] = suffix
                suffs_found += 1
                word_dict[instance]['suffix'][suffs_found] = dict()

        if not instance and not prefs_found and not suffs_found:
            word_dict[instance] = {'root': in_word}

        clean_structure(word_dict)

        return word_dict