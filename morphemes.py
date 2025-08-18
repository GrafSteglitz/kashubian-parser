"""
@module
This is a file for setting up which morphemes the parser will look for"""
class Morph:
    def __init__(self):
        self.prepositions = prepositions
        self.noun_suffixes = noun_suffixes
        self.adjective_suffixes = adjective_suffixes
        self.verb_suffixes = verb_suffixes


# DICTIONARIES OF ALLOWED ATTRIBUTES
pos = {"id": "pos",
       "subst": "noun",
       "fin": "non-past form",
       "inf": "infinitive",
       "adj": "adjective",
       "prep": "preposition",
       "num": "main numeral",
       "ppron": "personal pronoun",
       "numcol": "collective numeral",
       "praet": "l-participle",
       "pact": "present active participle",
       "qub": "particle-adverb",
       "adv": "adverb",
       "coord": "coordinating conjunction",
       "subord": "subordinating conjunction",
       "refl": "reflexive pronoun (sã)"}

number = {"id": "number",
          "sg": "singular",
          "pl": "plural"}
case = {
    "id": "case",
    "nom": "nominative",
    "gen": "genitive",
    "dat": "dative",
    "acc": "accusative",
    "instr": "instrumental",
    "loc": "locative",
    "voc": "vocative",
}
gender = {"id": "gender",
          "m": "all masculine",
          "m1": "virile",
          "m2": "masculine animate non-virile",
          "m3": "masculine inanimate",
          "f": "feminine",
          "n": "neuter"}

person = {"id": "person",
          "1": "first",
          "2": "second",
          "3": "third",
          "hon": "honorific"}

degree = {"id": "degree",
          "pos": "positive",
          "com": "comparative",
          "sup": "superlative"}

aspect = {"id": "aspect",
          "impf": "imperfective",
          "perf": "perfective"}

accentuation = {"id": "accentuation",
                "akc": "accented",
                "nakc": "unaccented"}


def get_keys(cat_dict):
    """Return all tag keys from a category dict that are not 'id'. """
    return [a for a in cat_dict.keys() if a != 'id']


validator_tree = {"adj": [*get_keys(case), *get_keys(gender), *get_keys(number), *get_keys(degree)],
                  "subst": [*get_keys(case), *get_keys(gender), *get_keys(number)],
                  "fin": [*get_keys(number), *get_keys(person), *get_keys(aspect)],
                  "ppron": [*get_keys(number), *get_keys(person), *get_keys(gender), *get_keys(case)],
                  "inf": [*get_keys(aspect)],
                  "adv": [*get_keys(degree)]}

prepositions = {
    "w": "loc:acc",
    "do": "gen",
    "na": "loc:acc",
    "nad": "instr:acc",
    "ò": "loc:acc",
    "òd": "gen",
    "òde": "gen",
    "pò": "loc:acc",
    "pòd": "instr:acc",
    "pòde": "instr:acc",
    "przë": "loc",
    "przez": 'acc',
    "ù": "gen",
    "we": "loc:acc",
    "z": "gen:instr",
    "ze": "gen:instr",
    "za": "acc:instr",
    "dlô": "gen",
    "kòle": "gen",
    "nimò": "gen",
    "kù": "dat",
    "bez": "gen"
}

noun_suffixes = {
    "ów": "subst:pl:gen:m1:m2:m3:f:n",
    "ë": ("subst:pl:m1:m2:m3:f:n:nom:acc", "subst:f:sg:gen:loc"),
    "ach": "subst:pl:loc",
    "ama": "subst:instr:pl",
    "ie": "subst:m:f:n:sg:dat:loc",
    "ié": "subst:n:sg:nom:acc",
    "ù": "subst:m3:n:gen:loc",
    "u": "subst:m3:n:gen:loc",
    "òwi": ("subst:m1:m2:dat:sg", "adj:m:sg:nom"),
    "owi": ("subst:m1:m2:dat:sg", "adj:m:sg:nom"),
    "ã": ("subst:m:n:instr:sg", "subst:f:sg:acc"),
    "ą": "fem:acc:instr:sg",
    "a": ("subst:f:sg:nom", "subst:m1:m2:gen:acc:sg"),
    "i": "subst:nom:acc:pl",
    "o": ('subst:f:voc:sg', 'adv', 'subst:n:sg:nom:acc'),
    "ò": ('subst:f:voc:sg', 'adv', 'subst:n:sg:nom:acc'),
    "óm": ("subst:dat:pl", "fin:1:sg"),
    "ô": "subst:n:gen:sg",
    "e": ("subst:m1:m2:m3:sg:loc", "subst:f:sg:dat:loc")

}
derivational_n_suffixes = {
    "òsc": "subst:f",
    "ota": "subst:f"
}
f_noun_suffixes = {"a": "",
                   "i": "",
                   "ë": "",
                   "e": "",
                   "ã": "",
                   "ą": "",
                   "o": "",
                   "ò": "",
                   "ów": "",
                   "óm": "",
                   "ach": ""}

adjective_suffixes = {"ëch": "adj:pl:gen:loc",
                      "ich": "adj:pl:gen:loc",
                      "égò": ("adj:sg:acc:gen:m1:m2", "adj:sg:gen:n:m3"),
                      "é": ("adj:sg:nom:acc:n", "adj:pl:nom:acc"),
                      "ié": ("adj:sg:nom:acc:n", "adj:pl:nom:acc"),
                      "y": ("adj:nom:m1:m2:sg", "adj:acc:sg:m3"),
                      "émù": "m:dat:sg",
                      "ym": ("adj:sg:loc:instr", "adj:pl:dat"),
                      "yma": "adj:instr:pl",
                      "im": ("adj:sg:loc", "adj:sg:instr"),
                      "ima": "adj:instr:pl",
                      "ô": "adj:f:nom:sg",
                      "i": ("adj:f:sg:gen:loc", "adj:m:nom:sg")}

verb_suffixes = {"esz": "fin:2:sg",
                 "emë": "fin:1:pl",
                 "eta": "fin:2:pl",
                 "ôsz": "fin:2:sg",
                 "isz": "fin:2:sg",
                 "ią": "fin:3:pl",
                 "ôta": "fin:2:pl",
                 "ô": "fin:3:sg",
                 "ã": "fin:1:sg",
                 "c": "inf"}

ignore_list = ["a", "ach", "aha", "ala", "alakòtóm", "alana", "alaże", "alażinkò", "aleluja", "ecz", "ehe", "ej",
               "ela", "fe", "fikak", "fiu", "ha", "haha", "ha-haha", "hahaszkù", "haps", "hą", "he", "ja jam ja jo",
               "ja në", "jak to", "jakùż", "jej", "jejkù", "Jena", "Jeną", "Jene", "Jenkù", "maricznym", "maricznóm",
               "mëk", "në", "nële", "nëtale", "nóże", "ò", "òch", "òchò", "òj", "pù", "reti", "slicznym", "szlacha",
               "ala szlachòwie", "ùlana", "wej", "wejle", "wejleszcze", "wejtale", "wejtażle"]

ignore_particles = ["niech", "pòdobno"]

# przek = 'przékùjący partiklë'
przek = {'nie', 'nié', 'ni'}

qub = {"pòdobno", "gwës", "gwësno", "jo", "leno", "le", "jo", "bòdôj", "niechôj", "niech"}

subord_conj = {'czë', "żebë", "bë", "cobë", "bò", "żelë", "pòczi", "żle", "że", "niechbë"}

coord_conj = {'i', 'albò', 'ani'}

verb_prefixes = ["do", "na", "nad", "ò", "òb", "òd", "òde", "pò", "pòd", "pòde", "prze", "przë", "roz", "ù", "w", "we",
                 "wespół", "wë", "s", "z", "ze"]

byc = {"base": "bëc", "bëc": "inf", "jem": "fin:1:sg", "jes": "fin:2:sg", "je": "fin:3:sg", "jesmë": "fin:1:pl",
       "jesta": "fin:2:pl",
       "są": "fin:3:pl",
       "jesce": "hon"}
byc_past = {"base": "bëc",
            "bëł": "m:sg:praet",
            "bëła": "f:sg:praet",
            "bëło": "n:sg:praet",
            "bëlë": "m1:pl:praet",
            "bëłë": "m2:m3:f:n:pl:praet"}

byc_future = {"base": "bëc",
              "bãdã": "fin:1:sg",
              "bądã": "fin:1:sg",
              "mdã": "fin:1:sg",
              "bãdzesz": "fin:2:sg",
              "bądzesz": "fin:2:sg",
              "mdzesz": "fin:2:sg",
              "bãdze": "fin:3:sg",
              "bądze": "fin:3:sg",
              "mdze": "fin:3:sg",
              "bãdzemë": "fin:1:pl",
              "bądzemë": "fin:1:pl",
              "mdzemë": "fin:1:pl",
              "bãdzeta": "fin:2:pl",
              "bądzeta": "fin:2:pl",
              "mdzeta": "fin:2:pl",
              "bãdą": "fin:3:pl",
              "bądą": "fin:3:pl",
              "mdą": "fin:3:pl",
              "bãdzece": "fin:hon",
              "bądzece": "fin:hon",
              "mdzece": "fin:hon"}

miec = {"móm": "fin:1:sg",
        "môsz": "fin:2:sg",
        "mô": "fin:3:sg",
        "mómë": "fin:1:pl",
        "môta": "fin:2:pl",
        "mają": "fin:3:pl",
        "môce": "fin:hon"}

wiedzec = {"wiém": "fin:1:sg",
           "wiész": "fin:2:sg",
           "wié": "fin:3:sg",
           "wiémë": "fin:1:pl",
           "wiéta": "fin:2:pl",
           "wiedzą": "fin:3:pl",
           "wiéce": "fin:hon:pl",
           "wiedzec": "inf:imperf"}

# dict is formatted as follows: {ppron: {"base": str/tuple, "attrs": str/tuple}, where each item in the tuple
# matches an item in the other tuple
# unordered tagging system
personal_pronouns = {"jô": {"base": "jô", "attrs": "ppron:1:nom:sg"},
                     "mie": {"base": "jô", "attrs": "ppron:1:gen:dat:loc:sg"},
                     "miã": {"base": "jô", "attrs": "ppron:1:acc:sg"},
                     "mną": {"base": "jô", "attrs": "ppron:1:instr:sg"},

                     "të": {"base": "të", "attrs": "ppron:2:nom:sg"},
                     "cebie": {"base": "të", "attrs": "ppron:2:sg:gen:dat:acc:akc"},
                     "ce": {"base": "të", "attrs": "ppron:2:sg:acc:gen:dat:nakc"},
                     "cã": {"base": "të", "attrs": "ppron:2:sg:acc:nakc"},
                     "tobie": {"base": "të", "attrs": "ppron:2:sg:dat:loc:akc"},
                     "tobą": {"base": "të", "attrs": "ppron:2:sg:instr:akc"},

                     "òn": {"base": "òn", "attrs": "ppron:3:sg:m:nom"},
                     "jegò": {"base": "òn", "attrs": "ppron:3:sg:m:acc:gen:akc"},
                     "gò": {"base": "òn", "attrs": "ppron:3:sg:m:acc:gen:nakc"},
                     "niegò": {"base": "òn", "attrs": "ppron:3:sg:m:acc:gen:akc:praep"},
                     "jemù": {"base": "òn", "attrs": "ppron:3:sg:m:n:dat:akc"},
                     "mù": {"base": "òn", "attrs": "ppron:3:sg:m:n:dat:nakc"},
                     "nim": {"base": "òn", "attrs": "ppron:3:sg:m:n:instr:loc:nakc"},
                     "nie": {"base": "òn",
                             "attrs": ("ppron:3:sg:n:acc:akc:praep", "ppron:3:pl:n:m2:m3:f:acc:akc:praep")},

                     "òna": {"base": "òna", "attrs": "ppron:3:sg:f:nom:akc"},
                     "ją": {"base": "òna", "attrs": "ppron:3:sg:f:acc:akc"},
                     "nią": {"base": "òna", "attrs": "ppron:3:sg:f:acc:instr:akc:praep"},
                     "ji": {"base": "òna", "attrs": "ppron:3:sg:f:gen:dat:instr:akc"},
                     "ni": {"base": "òna", "attrs": "ppron:3:sg:f:gen:loc:instr:akc:praep"},

                     "òno": {"base": "òno", "attrs": "ppron:3:sg:n:nom:akc"},
                     "je": {"base": "òn", "attrs": ("ppron:3:sg:n:nom:akc", "ppron:3:pl:n:m2:m3:f:nom:akc")},

                     "më": {"base": "më", "attrs": "ppron:1:pl:m1:m2:m3:f:n:nom:akc"},
                     "nas": {"base": "më", "attrs": "ppron:1:pl:m1:m2:m3:f:n:acc:gen:loc:akc"},
                     "naju": {"base": "më", "attrs": "ppron:1:pl:m1:m2:m3:f:n:acc:gen:loc:akc"},
                     "nama": {"base": "më", "attrs": "ppron:1:pl:m1:m2:m3:f:n:dat:instr:akc"},

                     "wa": {"base": "wa", "attrs": "ppron:2:pl:m1:m2:m3:f:n:nom:akc"},
                     "was": {"base": "wa", "attrs": "ppron:2:pl:m1:m2:m3:f:n:acc:gen:loc:akc"},
                     "waju": {"base": "wa", "attrs": "ppron:2:pl:m1:m2:m3:f:n:acc:gen:loc:akc"},
                     "wama": {"base": "wa", "attrs": "ppron:2:pl:m1:m2:m3:f:n:dat:instr:akc"},

                     "òni": {"base": "òn", "attrs": "ppron:3:pl:m1:m2:m3:f:n:nom:akc"},
                     "jich": {"base": "òn", "attrs": "ppron:3:pl:m1:m2:m3:f:n:nom:gen:akc"},
                     "nich": {"base": "òn", "attrs": "ppron:3:pl:m1:m2:m3:f:n:loc:gen:akc:praep"},
                     "jima": {"base": "òn", "attrs": "ppron:3:pl:m1:m2:m3:f:n:instr:dat:akc"},
                     "nima": {"base": "òn", "attrs": "ppron:3:pl:m1:m2:m3:f:n:dat:instr:akc:praep"},

                     "òne": {"base": "òn", "attrs": "ppron:3:pl:m2:m3:f:n:nom:akc"},

                     "Wë": {"base": "Wë", "attrs": "ppron:hon:sg:pl:nom:akc"},
                     "Was": {"base": "Wë", "attrs": "ppron:hon:sg:pl:acc:gen:loc:akc"},
                     "Wóm": {"base": "Wë", "attrs": "ppron:hon:sg:pl:acc:gen:loc:akc"},
                     "Wama": {"base": "Wë", "attrs": "ppron:hon:sg:pl:instr:akc"},

                     }
reflexive_pronouns = {
    "sã": "refl:acc:gen:nakc",
    "so": "refl:dat:loc",
    "se": "refl"}

ten = {"id": "ten",
       "ten": "adj:m:nom:sg",
       "ta": "adj:f:nom:sg",
       "to": "adj:n:nom:acc:sg",
       "tegò": ("adj:m3:n:gen:sg", "adj:m1:acc:sg"),
       "temù": "adj:m1:m2:m3:dat:sg",
       "tã": "adj:f:sg:acc",
       "tą": "adj:sg:instr",
       "tim": ("adj:instr:loc:sg", "adj:dat:pl"),
       "ti": "adj:sg:f:dat:loc",
       "tima": "adj:instr:pl",
       "te": "adj:nom:acc:pl:f:n:m3",
       "tëch": "adj:loc:gen:pl"}

co = {'co': 'wh:nom:acc',
      'czegò': "wh:gen",
      "czim": "wh:instr:loc",
      "czemù": "wh:dat"}
nic = {'ni' + x: v + ':neg' for x, v in co.items() if x != 'co'}
nic.update({'nic': co['co'] + ':neg'})

chto = {'chto': 'wh:nom:sg',
        'kògò': 'wh:acc:gen:sg',
        'kòmù': 'wh:dat:sg',
        'kim': 'wh:instr:loc',
        'kògùm': 'wh:instr:loc'}
nicht = {'ni' + x: v + ':neg' for x, v in chto.items() if x != 'chto'}
nicht.update({'nicht': chto['chto'] + ':neg'})

num = ['wiele']
paradigm_list = [f_noun_suffixes]

# personal_pronouns = {"jô": {"Nom": "jô",
#                             "Acc": ("mie", "miã"),
#                             "Gen": "mie",
#                             "Dat": "mie",
#                             "Instr": "mną",
#                             "Loc": "mie"},
#                      "të": {"Nom": "të",
#                             "Acc": {"LF": "cebie", "SF": ("ce", "cã")},
#                             "Gen": {"LF": "cebie", "SF": "ce"},
#                             "Dat": {"LF": ("tobie", "cebie"), "SF": "ce"},
#                             "Instr": "tobą",
#                             "Loc": "tobie"},
#                      "òn": {"Nom": "òn",
#                             "Acc": {"LF": "jegò", "SF": "gò", "prep": "niegò"},
#                             "Gen": {"LF": "jegò", "SF": "gò", "prep": "niegò"},
#                             "Dat": {"LF": "jemù", "SF": "mù"},
#                             "Instr": "nim",
#                             "Loc": "nim"},
#                      "òna": {"Nom": "òna",
#                              "Acc": {"LF": "ją", "prep": "nią"},
#                              "Gen": {"LF": "ji", "prep": "ni"},
#                              "Dat": "ji",
#                              "Instr": "nią",
#                              "Loc": "ni"},
#                      "òno": {"Nom": "òno",
#                              "Acc": {"LF": "je", "prep": "nie"},
#                              "Gen": "jegò",
#                              "Dat": {"LF": "jemù", "SF": "mù"},
#                              "Instr": "nim",
#                              "Loc": "nim"},
#                      "më": {"Nom": "më",
#                             "Acc": ("nas", "naju"),
#                             "Gen": ("nas", "naju"),
#                             "Dat": "nama",
#                             "Instr": "nama",
#                             "Loc": ("nas", "naju")},
#                      "wa": {"Nom": "wa",
#                             "Acc": ("was", "waju"),
#                             "Gen": ("was", "waju"),
#                             "Dat": "wama",
#                             "Instr": "wama",
#                             "Loc": ("was", "waju")},
#                      "òni": {"Nom": "òni",
#                              "Acc": "jich",
#                              "Gen": {"LF": "jich", "prep": "nich"},
#                              "Dat": "jima",
#                              "Instr": {"LF": "jima", "prep": "nima"},
#                              "Loc": "nich"},
#                      "òne": {"Nom": "òne",
#                              "Acc": "je",
#                              "Gen": {"LF": "jich", "prep": "nich"},
#                              "Dat": "jima",
#                              "Instr": {"LF": "jima", "prep": "nima"},
#                              "Loc": "nich"},
#                      "Wë": {"Nom": "Wë",
#                             "Acc": "Was",
#                             "Gen": "Was",
#                             "Dat": "Wóm",
#                             "Instr": "Wama",
#                             "Loc": "Was"
#                             }
#                      }


# tree_dict = {'pos': {"id": "pos",
#                      "subst": "noun",
#                      "fin": "non-past form",
#                      "inf": "infinitive",
#                      "adj": "adjective",
#                      "prep": "preposition",
#                      "num": "main numeral",
#                      "ppron": "personal pronoun",
#                      "numcol": "collective numeral",
#                      "praet": "l-participle",
#                      "pact": "present active participle",
#                      "qub": "particle-adverb",
#                      "adv": "adverb",
#                      "coord": "coordinating conjunction",
#                      "subord": "subordinating conjunction",
#                      "refl": "reflexive pronoun (sã)"},
#              'number': {"id": "number",
#                         "sg": "singular",
#                         "pl": "plural"},
#              'case': {
#                  "id": "case",
#                  "nom": "nominative",
#                  "gen": "genitive",
#                  "dat": "dative",
#                  "acc": "accusative",
#                  "instr": "instrumental",
#                  "loc": "locative",
#                  "voc": "vocative",
#              },
#              'gender': {"id": "gender",
#                         "m": "all masculine",
#                         "m1": "virile",
#                         "m2": "masculine animate non-virile",
#                         "m3": "masculine inanimate",
#                         "f": "feminine",
#                         "n": "neuter"},
#
#              'person': {"id": "person",
#                         "1": "first",
#                         "2": "second",
#                         "3": "third",
#                         "hon": "honorific"},
#
#              'degree': {"id": "degree",
#                         "pos": "positive",
#                         "com": "comparative",
#                         "sup": "superlative"},
#
#              'aspect': {"id": "aspect",
#                         "impf": "imperfective",
#                         "perf": "perfective"},
#
#              'accentuation': {"id": "accentuation",
#                               "akc": "accented",
#                               "nakc": "unaccented"}}

def get_dict_vals_as_list(attrs_dict):
    vals = attrs_dict.values()
    new_list = []
    for each in vals:
        new_list = new_list + each
    return new_list


def make_attrs_dict(attrs_list):
    """

    :param attrs_list: a 1-D list of attributes
    :return: a dict with category keys and list of attributes
    """
    tree_list = [pos, number, gender, case, person, degree, aspect, accentuation]
    out_dict = {}
    # 'pos': [], 'number': [], 'gender': [], 'case': [], 'person': [], 'accent': [], 'degree': [],
    #                 'accentuation': []
    for each in attrs_list:
        for cat in tree_list:
            if each in cat:
                if cat['id'] not in out_dict:
                    out_dict.update({cat['id']: []})
                out_dict[cat['id']].append(each)
                continue

    return out_dict


if __name__ == '__main__':
    make_attrs_dict([['subst', 'nom', 'f', 'sg', 'instr']])
    print('something')
