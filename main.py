from conversation import Conversation
from tags import train_model as train_tags_model
from intents import Intent
from footprint import Footprint
import yaml


def load_data(intents_file, tags_file):
    data = None
    with open(intents_file) as resource:
        data = yaml.load(resource, Loader=yaml.FullLoader)
    
    intents = list(map(
        lambda i: Intent(
            name=i.get('name'),
            answers=i.get('answers'),
            event=i.get('event'),
            input_sentences=i.get('input_sentences', []),
            required_footprints=i.get('required_footprints', []),
            tags=i.get('tags', []),
            footprints=list(map(
                lambda f: Footprint(f.get('name'), f.get('ttl')),
                i.get('footprints', '')
                ))
        ),
        data['intents']
    ))

    tags_info = train_tags_model(tags_file)

    return (tags_info, intents)

def run_bot(tags_prediction_info, intents):
    conversation = Conversation(tags_prediction_info, intents)
    
    while not conversation.is_finished():
        sentence = str(input("Human: "))
        answer = conversation.input_sentence(sentence)
        print('Bot  :', answer)
        print()


if __name__ == '__main__':
    tags_prediction_info, intents = load_data('./resources/conversation.yml', './resources/sentence-tags-training-data.csv')
    run_bot(tags_prediction_info, intents)