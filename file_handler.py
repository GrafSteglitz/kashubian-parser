"""
@module
"""
import re


class FileHandler:
    """
    A class to handle file interactions.
    """
    def __init__(self, in_file="/Texts/example.txt"):
        self.in_file = in_file
        self.content = None
        self.word_list = []
        self.word_set = {}

    def read(self):
        """
        Read an entire file as a string.
        :return: Content as a string.
        """
        with open(self.in_file,'r',encoding='utf-8') as f:
            self.content = f.read()
            return self.content

    def read_lines(self):
        """
        Read a file as a list of lines.
        :return: A dictionary of the first word on the line as a key  followed by the second as a value.
        """
        with open(self.in_file,'r',encoding='utf-8') as f:
            self.content = []
            out_dict = {}

            for line in f.readlines():
                n = re.sub(r"\n", "", line)
                self.content.append(n)
                n2 = re.split(r'\s', n)

                if len(n2) == 1:
                    out_dict.update({n2[0]: ''})
                else:
                    out_dict.update({n2[0]: n2[1]})

            f.close()
            return out_dict


if __name__ == '__main__':
    FOO = FileHandler(in_file='ConfigFiles/ignores.txt')
    FOO.read_lines()
    print(FOO.content)
