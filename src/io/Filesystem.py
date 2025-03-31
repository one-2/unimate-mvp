from src.Env import *

import src.utils.Utils as Utils

class Filesystem:
    '''
    '''
    def __init__(self) -> None:
        """
        Initializes the Filesystem class and defines directory structures.
        """
        # save cwd path as attribute
        self.root_dir = Path.cwd()

        # save dumps directory paths as attributes and create the directories
        self.dumps_dir       = self.root_dir / 'dumps'
        self.dumps_dir.mkdir(exist_ok=True)

        self.dumps_today_dir = self.dumps_dir / Utils.get_today_str()
        self.dumps_today_dir.mkdir(exist_ok=True)

        self.dumps_event_data_dir = self.dumps_today_dir / 'event_data'
        self.dumps_event_data_dir.mkdir(exist_ok=True)

        # save data directory paths as attributes and create the directories
        self.data_dir = self.root_dir / 'data'
        self.data_dir.mkdir(exist_ok=True)

        self.input_data_dir  = self.data_dir / 'input'
        self.input_data_dir.mkdir(exist_ok=True)

        self.output_data_dir = self.data_dir / 'output'
        self.output_data_dir.mkdir(exist_ok=True)

        self.scraper_output_data_dir = self.output_data_dir / 'scraper'
        self.scraper_output_data_dir.mkdir(exist_ok=True)

        self.tagger_output_data_dir = self.output_data_dir / 'tagger'
        self.tagger_output_data_dir.mkdir(exist_ok=True)

        # save output file paths
        self.todays_event_csv_path = self.scraper_output_data_dir / ('events-' + str(Utils.get_today_str()) + '.csv')
        self.todays_tagged_csv_path = self.tagger_output_data_dir / ('events-tagged-' + str(Utils.get_today_str()) + '.csv')

    def get_event_list_path(self):
        '''
        '''
        # returns (Path) expected_path, (bool) expected_path_exists
        return self.input_dir_path(f'events-{Utils.get_today_str()}.txt')

    def clubs_database_path(self):
        '''
        '''
        # returns (Path) expected_path, (bool) expected_path_exists
        return self.input_dir_path('clubs-database.csv')

    def input_dir_path(self, filename):
        '''
        '''
        # returns (Path) expected_path, (bool) expected_path_exists
        expected_path = self.input_data_dir / filename
        return expected_path

    def get_pages_txt_output_path(self):
        '''
        '''
        return self.root_dir / f'events-{Utils.get_today_str()}.txt'
