import random
import events
from footprint import Footprint

class Intent():

    def __init__(self, name, answers, input_sentences=[], required_footprints=[], required_tags=[], footprints=[], event=None):
        self.__name = name
        self.__input_sentences = list(map(lambda i: str(i).lower().strip(), input_sentences))
        self.__answers = answers 
        self.__required_footprints = required_footprints
        self.__required_tags = required_tags
        self.__footprints = footprints
        self.__event = event

    def fit(self, sentence, footprints={}, tags={}):
        return (
            (len(self.__input_sentences) == 0 or any(map(sentence.match, self.__input_sentences)))
            and all(map(lambda f: not footprints.get(f) == None, self.__required_footprints))
            and all(map(lambda t: not tags.get(t) == None, self.__required_tags))
        )

    def answer(self):
        return random.choice(self.__answers)

    def event(self):
        return self.__event

    def footprints(self):
        return self.__footprints

    def __str__(self):
        return self.__name


FALLBACK_INTENNT = Intent('Fallback', ['I don\'t understand bro'])

def retrieve_intents(intents, sentence, footprints=[], tags=[]):
    footprints = dict(zip(map(str, footprints), footprints))
    tags = dict(zip(map(str, tags), tags))

    intents = list(filter(lambda t: t.fit(sentence, footprints, tags), intents))
    intents.append(FALLBACK_INTENNT)
    return intents[0]