class Tag():

    def __init__(self, name, input_sentences):
        self.__name = str(name)
        self.__input_sentences = list(map(lambda i: str(i).lower().strip(), input_sentences))

    def fit(self, sentence):
        # print("++++++++++++++++++", self.__name, self.__input_sentences)
        return any(map(sentence.match, self.__input_sentences))
        
    def __str__(self):
        return self.__name


def retrieve_tags(tags, sentence):
    return list(filter(lambda t: t.fit(sentence), tags))