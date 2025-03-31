# Written by Stephen Elliott
# (c) Conta Digital Pty Ltd
# Config file for event data tagger
# v0.1 - 4/11/23


infatica_api_key = 'dummy_key'

url_stub_placeholder = 'https://www.scrape_me.com/'
another_dummy_url_stub = r'https://www.another_dummy.com/'
google_forms_url_stub1 = r'https://forms.gle/'
google_forms_url_stub2 = r'https://docs.google.com/forms/'
google_drive_url_stub = r'https://drive.google.com/'
humanitix_url_stub = r'https://events.humanitix.com/'
eventbrite_url_stub = r'https://www.eventbrite.com.au/'
linkedin_url_stub = r'https://www.linkedin.com/'
tribespot_url_stub = r'https://app.tribespot.co/'

prompts = {
    'academic'      : 'If this event has a focus on academics, answer 1. Otherwise, answer 0.',
    'social'        : 'If this event has a focus on socialising, answer 1. Otherwise, answer 0.',
    'hobby'         : 'If this event has a focus on hobbies which are not professional or academic, answer 1. Otherwise, answer 0.',
    'party'         : 'If this event has a focus on partying, answer 1. Otherwise, answer 0.',
    'professional'  : 'If this event has a focus on employment, networking or other professional things, answer 1. Otherwise, answer 0.',
    'sport'         : 'If this event has a focus on sport, answer 1. Otherwise, answer 0.',
    'politics'      : 'If this event has a focus on politics, answer 1. Otherwise, answer 0.',
    'technology'    : 'If this event has a focus on technology, answer 1. Otherwise, answer 0.',
    'guest_speakers': 'If this event has guest speakers with strong credentials, answer 1. Otherwise, answer 0.'
}