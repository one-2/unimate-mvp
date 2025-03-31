# Written by Stephen Elliott
# (c) Conta Digital Pty Ltd
# Scrapes events for data
# v0.9 - 2/11/23

from src.Env import *
import src.scraper.Scripts as Scripts
import src.scraper.InfaticaRequests as InfaticaRequests
import Interface
import src.utils.Utils as Utils
import src.utils.Parser as Parser



def scrape_discussion_group(path, output):
    with open(path, 'r', encoding='utf-8') as f:
        html = str(f.read())
    all_links = Parser.extract_event_links(html, True)
    output.save_event_list(all_links)

def scrape_all_events(my_filesystem, my_output):
    '''
    '''
    # loop setup
    event_urls = Interface.get_events_url_generator(my_filesystem)
    skip_count = Interface.should_skip_pages()
    all_events = []

    for idx, url in enumerate(event_urls):
        for _ in range(skip_count):
            continue

        print(f'> Scrape {idx + 1} @ {url}')

        # get the data
        current = Event(url)

        start_time = time.time()
        current.response, tries = InfaticaRequests.get_response(current.url)
        end_time = time.time()
        print(f'\tReturned status code {current.response["status_code"]} in {end_time - start_time:.1f}s after {tries} attempts.')
        
        # extract the data
        record = current.scrape(my_output)

        # save summary data
        all_events.append(record)

        # sleep for a random period
        Utils.random_sleep(max_sleep=10)

    # dump summary info
    my_output.event_summary_to_binary(all_events)
    
    print(f'Event scrape loop finished. Output saved to {my_filesystem.todays_event_csv_path}')  # finish print

def scrape_club_pages(my_filesystem, my_output):
    # get the data
    df = Interface.get_clubs_database(my_filesystem)

    # loop setup
    skip_count = Interface.should_skip_pages()
    print(f'Skipping {skip_count} rows...')
    for idx, club in df.iterrows():
        if (idx < skip_count):
            continue

        print(f'Scrape {idx + 1}: {club["name"]} @ {club["site"]}')
        
        if not Utils.is_valid_site_page_link(club['site']):  # bad links
            print(f"\tInvalid club link: {club['site']}")
            continue

        # get data
        club = Club(name=club['name'],
                    url=club['site'])
        club.get_data()

        # extract the data
        club.get_event_links()  # extract links
        num_found = len(club.event_links)

        if num_found == 0:
            # no events found
            continue

        # events found
        print('\tFound event(s): ', *club.event_links)
        my_output.write_event_urls(club.event_links)

    print('Scrape completed.')



class Club:
    def __init__(self, name, url) -> None:
        self.name = name
        self.url = url
        self.html = ''
        self.event_links = []

    def get_data(self):
        # get page data
        response = InfaticaRequests.make_infatica_request(self.url)
        self.html = str(response.json()['html'])

    def get_event_links(self):
        self.event_links = Parser.extract_event_links(self.html, False)



class Event():
    def __init__(self, url) -> None:
        """
        Initializes an Event object with data and metadata.

        Args:
            url: The URL of the event.
        """
        self.url = url
        self.id = Parser.extract_id_from_url(url)
        self.scrape_date = Utils.get_today_str()

        self.response = {}
        self.html = ''
        self.data = {
            'event_url'           : self.url,
            'event_id'            : self.id,
            'event_scrape_date'   : self.scrape_date,
        }
        
        self.dump_filename = f'event-{self.id}.bin'

    def scrape(self, my_output):
        """
        Scrapes event data from specified URLs and saves it to CSV and binary files.
        """    
        # process data
        self.set_html()
        s1 = Scripts.Script1(self.html)
        s1.process()
        self.data.update(s1.output)

        s2 = Scripts.Script2(self.html)
        s2.process()
        self.data.update(s2.output)

        # save data
        my_output.event_to_csv(self)
        my_output.event_to_binary(self)

        summary = {
            'type'   :  'event',
            'id'     :  self.id,
            'url'    :  self.url
        }
        return summary

    def set_html(self):
        # saves response object html to instance html field
        self.html = self.response['html']
