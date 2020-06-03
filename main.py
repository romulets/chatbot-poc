from conversation import Conversation
from tags import Tag
from intents import Intent
from footprint import Footprint
import yaml


def load_data(file):
    data = None
    with open(file) as resource:
        data = yaml.load(resource, Loader=yaml.FullLoader)
        
    tags = list(map(
        lambda t: Tag(t.get('name'), t.get('input_sentences')), 
        data['tags']
    ))
    
    intents = list(map(
        lambda i: Intent(
            name=i.get('name'),
            answers=i.get('answers'),
            event=i.get('event'),
            input_sentences=i.get('input_sentences', []),
            required_footprints=i.get('required_footprints', []),
            required_tags=i.get('required_tags', []),
            footprints=list(map(
                lambda f: Footprint(f.get('name'), f.get('ttl')),
                i.get('footprints', '')
                ))
        ),
        data['intents']
    ))

    return (tags, intents)

def run_bot(tags, intents):
    conversation = Conversation(tags, intents)
    
    while not conversation.is_finished():
        sentence = str(input("Human: "))
        answer = conversation.input_sentence(sentence)
        print('Bot  :', answer)


if __name__ == '__main__':
    tags, intents = load_data('./resources/conversation.yml')
    run_bot(tags, intents)