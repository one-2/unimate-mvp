# Stephen Elliott
# (c) Conta Systems Pty Ltd
# v0.9 - 28/10/23

from src.Env import *
from src.utils.Utils import *
import src.utils.Parser as Parser



class Scripts:
    def __init__(self, name, identifier, funcs, html):
        """
        Initializes a Scripts object to handle raw and processed data.
        """
        self.name = name
        self.identifier = identifier

        self.funcs = funcs

        self.html = html
        self.script = {}
        self.output = {}

    def process(self):
        """
        Processes event data and extracts information.
        """
        # extract the scripts of interest
        self.extract_full_script()
        
        if self.script is None:
            print(f'ALERT: {self.name} extraction failed.')
        else:
            self.call_extraction_functions()

    def extract_full_script(self):
        all_scripts = self.all_scripts_as_strings()
        scripts_of_interest = search_by_tag(self.identifier, all_scripts)
        
        try:
            # if len(scripts_of_interest) > 1 or scripts_of_interest is None: # unexpected result
            #     print('Unexpected html structure in {self}. Raising exception.')
            #     raise Exception('Unexpected html structure.')
        
            # extract data from the script
            script_html = scripts_of_interest[0].text
            container_string = '"event":{'
            self.script = Parser.extract_html_as_dict(script_html, container_string)
        except Exception as e:
            self.script = None
            print(f'\tSomething weird happened in extract_full_script, throwing exception {e}.')
            print('> Skipping...')

    def call_extraction_functions(self):
        """
        Calls each parsing get method, updates the processed data, and handles any failures.
        """
        for x in self.funcs:
            out = x()
            try:
                self.output.update(out)
            except Exception as e:
                print(f'\tCall {x} failed, throwing exception {e}.')

    def all_scripts_as_strings(self):
        # returns list of scripts in the html as strings
        soup = BeautifulSoup(self.html, 'html.parser')
        scripts = soup.find_all('script')
        content = []
        for x in scripts:
            content.append(x)
        print(f'\tFound {len(content)} scripts in {self}.')
        return content



class Script1(Scripts):
    def __init__(self, html):
        """
        Initializes a Script1 object with raw script data.

        Args:
            script_dict: A dictionary containing raw script data.
        """
        name='Script1'
        identifier='"result":{"data":{"event":{"is_online":'
        funcs = [
            self.get_description,
            self.get_is_online,
            self.get_event_location_name,
            self.get_event_location_coordinates,
            self.get_event_id,
            self.get_parent_name,
            self.get_parent_id,
            self.get_parent_url,
            self.get_display_duration,
            self.get_external_links,
            self.get_tribespot_links,
            self.get_linkedin_links,
            self.get_eventbrite_links,
            self.get_humanitix_links,
            self.get_google_drive_links,
            self.get_google_forms_links,
            self.get_another_dummy_links,
        ]

        super().__init__(name,
                         identifier,
                         funcs,
                         html)

    def get_description(self):
        val = self.script.get('event_description').get('text')
        return {'event_description' : val}

    def get_is_online(self):
        val = self.script.get('is_online')
        return {'is_online' : val}

    def get_event_location_name(self):
        tag = self.script.get('event_place')
        if tag is None:
            val = 'Online'
        else:
            val = tag.get('name')
        return {'location_name' : val}

    def get_event_location_coordinates(self):
        val = ''
        tag = self.script.get('event_place')
        if tag is None:
            val = 'Online'
        else:
            val = tag.get('location')
            if val is not None:
                val.pop('reverse_geocode')
        return {'location_coordinates' : val}

    def get_event_id(self):
        val = self.script.get('id')
        return {'event_id' : val} 
    
    def get_parent_name(self):
        val = self.script.get('event_creator').get('name')
        return {'event_creator_name' : val}
    
    def get_parent_id(self):
        val = self.script.get('event_creator').get('id')
        return {'event_creator_id' : val}

    def get_parent_url(self):
        this_id = self.get_parent_id().get('event_creator_id')
        return {'event_parent_url' : f'https://www.site.com/{this_id}'}

    def get_display_duration(self):
        val = self.script.get('display_duration')
        return {'display_duration' : val}

    def get_external_links(self):
        links = []
        field = self.script.get('event_description').get('ranges')
        if field is not None:
            for x in field:
                url = x.get('entity').get('external_url')
                links.append(url)
        links = get_unique_links(links)
        return {'external_links' : links}

    def get_another_dummy_links(self):
        all_links = self.get_external_links()['external_links']
        found = get_links_by_substring(all_links, Config.another_dummy_url_stub)
        found = get_string_or_list_of_links(found)
        return {'another_dummy_links' : found}

    def get_google_forms_links(self):
        all_links = self.get_external_links()['external_links']
        found = get_links_by_substring(all_links, Config.google_forms_url_stub1)
        found += get_links_by_substring(all_links, Config.google_forms_url_stub2)
        found = get_string_or_list_of_links(found)
        return {'google_forms_links' : found}

    def get_google_drive_links(self):
        all_links = self.get_external_links()['external_links']
        found = get_links_by_substring(all_links, Config.google_drive_url_stub)
        found = get_string_or_list_of_links(found)
        return {'google_drive_links' : found}

    def get_humanitix_links(self):
        all_links = self.get_external_links()['external_links']
        found = get_links_by_substring(all_links, Config.humanitix_url_stub)
        found = get_string_or_list_of_links(found)
        return {'humanitix_links' : found}

    def get_eventbrite_links(self):
        all_links = self.get_external_links()['external_links']
        found = get_links_by_substring(all_links, Config.eventbrite_url_stub)
        found = get_string_or_list_of_links(found)
        return {'eventbrite_links' : found}

    def get_linkedin_links(self):
        all_links = self.get_external_links()['external_links']
        found = get_links_by_substring(all_links, Config.linkedin_url_stub)
        found = get_string_or_list_of_links(found)
        return {'linkedin_links' : found}

    def get_tribespot_links(self):
        all_links = self.get_external_links()['external_links']
        found = get_links_by_substring(all_links, Config.tribespot_url_stub)
        found = get_string_or_list_of_links(found)
        return {'tribespot_links' : found}


class Script2(Scripts):
    def __init__(self, html):
        """
        Initializes a Script2 object with raw script data.

        Args:
            script_dict: A dictionary containing raw script data.
        """
        name='Script 2'
        identifier='"event":{"page_as_parent":{"id":'
        funcs = [
            self.get_event_name,
            self.get_is_cancelled,
            self.get_event_frequency,
            self.get_unix_start_timestamp,
            self.get_english_start_timestamp,
        ]

        super().__init__(name,    # DEBUG: fix tag below
                         identifier, # PREVIOUSLY '"event":{"unified_tournament"'
                         funcs,
                         html)

    def get_is_cancelled(self):
        val = self.script.get('is_canceled')
        return {'is_cancelled' : val}
    
    def get_cover_photo_url(self):
        val = self.script.get('cover_media_renderer').get('cover_photo').get('photo').get('full_image').get('url')
        return {'cover_photo_url' : val}
    
    def get_event_frequency(self):
        val = self.script.get('parent_if_exists_or_self').get('event_frequency')
        return {'event_frequency' : val}
    
    def get_event_name(self):
        val = self.script.get('name')
        return {'event_name' : val}
    
    def get_unix_start_timestamp(self):
        # returns start epoch
        val = self.script.get('start_timestamp')
        return {'unix_start_timestamp' : val}
    
    def get_english_start_timestamp(self):
        unix_timestamp = self.get_unix_start_timestamp()['unix_start_timestamp']
        local_datetime = datetime.datetime.fromtimestamp(unix_timestamp)
        local_timestamp = local_datetime.strftime('%H:%M %d-%m-%y')
        return {'aedt_start_timestamp' : local_timestamp}



def search_by_tag(search_string, all_scripts):
    found = []
    for i, x in enumerate(all_scripts):
        if search_string in x.text:
            print(f"\tScript #{i} contains search string '{search_string}'.")
            found.append(x)
    return found

def get_unique_links(links):
    return list(set(links))

def get_links_by_substring(links, substring):
    found = []
    for link in links:
        if link is None:
            continue
        if link.__contains__(substring):
            found.append(link)
            break
    return found

def get_string_or_list_of_links(found):
    if len(found) == 0:
        return ''
    elif len(found) == 1:
        return found[0]
    else:
        return found
