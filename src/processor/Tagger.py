# Written by Stephen Elliott
# (c) Conta Digital Pty Ltd
# Tags event data
# v0.1 - 4/11/23

from src.Env import *
import src.Config as Config
import openai
import src.utils.Utils as Utils

openai.api_key = r'dummy_key'

def tag_all_events(path):
    with open(path, 'r', encoding='utf-8') as f:
        df = pd.read_csv(f, encoding='utf-8')

    # tag loop
    for row_idx, event in df.iterrows():
        # skip past events
        if Utils.event_is_past(event):
            continue
        
        # skip tagged events
        if event['is_academic'] is not None:
            continue

        # tag current event
        prompter = Prompter(event['event_description'])
        print(f'> Tagging event "{event["event_name"]}".')
        for prompt in prompter.funcs:
            response = prompt()
            add_response(df, row_idx, response)
            label = next(iter(response.keys()))
            val = next(iter(response.keys()))
            print(f'\tTagged {label} as {val}.')
    return df

def add_response(df, row_index, response_dict):
    # adds a {key : val} to the df
    # creates a field 'key' if needed
    column_name = list(response_dict.keys())[0]
    df[column_name] = None
    df.at[row_index, column_name] = response_dict[column_name]



class Prompter():
    def __init__(self, description):
        self.event_description = description
        self.funcs = [
            self.is_academic,
            self.is_social,
            self.is_hobby,
            self.is_party,
            self.is_professional,
            self.is_sport,
            self.is_politics,
            self.is_technology,
            self.is_guest_speakers,
        ]

    def is_academic(self):
        return {'is_academic'           : self.classify_event(Config.prompts['academic'])}

    def is_social(self):
        return {'is_social'             : self.classify_event(Config.prompts['social'])}

    def is_hobby(self):
        return {'is_hobby'              : self.classify_event(Config.prompts['hobby'])}

    def is_party(self):
        return {'is_party'              : self.classify_event(Config.prompts['party'])}
    
    def is_professional(self):
        return {'is_professional'       : self.classify_event(Config.prompts['professional'])}

    def is_sport(self):
        return {'is_sport'              : self.classify_event(Config.prompts['sport'])}
    
    def is_politics(self):
        return {'is_politics'           : self.classify_event(Config.prompts['politics'])}
    
    def is_technology(self):
        return {'is_technology'         : self.classify_event(Config.prompts['technology'])}

    def is_guest_speakers(self):
        return {'has_guest_speakers'    : self.classify_event(Config.prompts['guest_speakers'])}

    def classify_event(self, prompt):
        response = chattyboi_response(prompt, self.event_description)
        processed = process_chattyboi_response(response)
        while processed is None: # TODO: handle as exception
            print('Classification failure. Calling the API again...')
            response = chattyboi_response(prompt, self.event_description)
            processed = process_chattyboi_response(response)
        return processed

def chattyboi_response(prompt, event_description):
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role"      : "system",
            "content"   : "You are a binary classifier, and you only answer with '1' or '0'."
        },
        {
            "role"      : "user",
            "content"   : f'{prompt}. Event description is {event_description}.',
        }
    ]
    )
    return response

def process_chattyboi_response(response):
    # returns None, 0 or 1
    answer = get_content_from_chattyboi_response(response)
    answer = int(answer)
    if answer != 0 and answer != 1:
        return None
    else:
        return bool(answer)

def get_content_from_chattyboi_response(response):
    content = response.get('choices')[0].get('message').get('content')
    if content == "Invalid":
        return None
    else:
        return content
