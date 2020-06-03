import re

class Sentence():

    def __init__(self, raw_sentence):
        self.__raw_sentence = str(raw_sentence)
        self.__tokenized = str(self.__raw_sentence.lower().strip())

    def match(self, pattern):
        # print('MATCH', str(pattern), self.__tokenized)
        return re.match(str(pattern), self.__tokenized)

    def tokenize(self):
        return self.__tokenized