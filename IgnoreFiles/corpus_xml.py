import xml.etree.ElementTree as ET
import re

tree = ET.parse('example.xml')
root = tree.getroot()
chapter = root[0]


# sens = chapter[0]
# for n in root:
#     print(n.tag)
#     for a in n:
#         print(a.tag)
#         for b in a:
#             print(b.tag + ": " + b.text)


# sen = chapter.findall('sentence')
# for a in sen:
#     print(a.text)


class XmlCorpusHandler:
    def __init__(self, in_data='./Texts/example.txt', target='example.xml'):
        self.text = ET.parse(target)
        self.root = self.text.getroot()
        self.source = in_data
        f = open(self.source)
        self.f_content = f.read()
        f.close()
        # print(self.f_content)

    def write_xml(self):
        sentences_list = self.f_content.split(".")
        sentence_d = {}
        for count, s in enumerate(sentences_list):
            word_split = s.split()
            sentence_d.update({count: word_split})
        # build input dictionary
        for x, y in sentence_d.items():
            sent = ET.Element("sentence")
            for xx in y:
                word = ET.Element("word")
                word.text = str(xx)
                word.set('attrs', '')
                sent.append(word)
            chapter.append(sent)

        tree.write("example.xml", encoding="utf-8", xml_declaration=True)

        # for x in sentences_list:
        #     root.


def modify_xml():
    for sentence in chapter.iter('sentence'):
        for word in sentence:
            if not word.get('base'):
                word.set('base', '')

    tree.write("example.xml", encoding="utf-8", xml_declaration=True)


def remove_commas():
    for sentence in chapter.iter('sentence'):
        word_list = enumerate(list(sentence))
        for count, word in word_list:
            m = re.search(r"[!#S%&'()*+,-./:;<=>?@\[\]^_{|}~]+", word.text)
            if m:
                g = m.group()
                if word.text != g and word.text.endswith(g):
                    word_list[count+1]
                    pass
                print(g)



remove_commas()
# modify_xml()
# a = XmlCorpusHandler()
# a.write_xml()
