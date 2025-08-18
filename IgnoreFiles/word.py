from morphemes import *
import re


class Sentence:
    def __init__(self):
        self.words = list()


class Word:
    def __init__(self, in_word=None):
        self.value = in_word
        self.type = []
        self.base = None
        self.req_case = []
        self.attrs = []
        # position in the text
        self.pos = int()
        self.prev = None
        self.next = None
        # position in the sentence
        self.sentence = []
        self.s_pos = int()
        self.root = []
        self.morph = []

    def is_adjective(self):
        adjs = adjective_suffixes
        for a in adjs:
            if self.value.endswith(a):
                if a == "é":
                    m = re.search(r"ni", self.value)
                    if m:
                        continue
                s = re.search(a, self.value)
                sp = s.span()
                self.root.append(self.value[0:sp[0]])

                return self.root
                # out_dict.update({in_word: {"ending": a}})

    def is_preposition(self):
        for p in prepositions:
            if self.value == p:
                self.type.append("preposition")
        return self.type


class Adjective(Word):
    def __init__(self, in_word=None):
        super().__init__(in_word)
        self.type = "adjective"


if __name__ == '__main__':
    w = Word('apartnémù')
    w.is_adjective()
