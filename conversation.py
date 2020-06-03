from sentence import Sentence
from tags import retrieve_tags
from intents import retrieve_intents
from footprint import run_footprint_cicle
import events

class Conversation():


    def __init__(self, tags, intents):
        self.__last_event = None
        self.__tags = tags
        self.__intents = intents
        self.__footprints = []

    def is_finished(self):
        return self.__last_event ==  events.END

    def input_sentence(self, raw_sentence):
        sentence = Sentence(raw_sentence)

        tags = retrieve_tags(self.__tags, sentence)
        
        intent = retrieve_intents(self.__intents, sentence, footprints=self.__footprints, tags=tags)
        
        self.__footprints = run_footprint_cicle(self.__footprints, intent.footprints())

        self.__last_event = intent.event()

        # print("------ TAGS: ", list(map(str, tags)))
        # print("------ FOOTPRINTS: ", list(map(str, self.__footprints)))
        # print("------ INTENT: ", str(intent))

        return intent.answer()