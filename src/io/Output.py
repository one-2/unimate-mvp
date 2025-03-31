# Written by Stephen Elliott
# (c) Conta Digital Pty Ltd

from src.Env import *
import src.utils.Utils as Utils

class Output:
    '''
    '''
    def __init__(self, filesystem):
        """
        Initializes the Output class with a reference to the file system.

        Args:
            my_filesystem: An instance of the Filesystem class.
        """
        self.filesystem = filesystem

        # save file structure
        self.event_csv_exists = self.filesystem.todays_event_csv_path.exists()

    def event_to_csv(self, event) -> None:
        """
        Writes event data to a CSV file.

        Args:
            event: An Event object containing the data to be written.
        """
        with open(self.filesystem.todays_event_csv_path, 'a', newline='', 
                  encoding='utf-8') as f:
            event_data = event.data

            writer = csv.DictWriter(f, fieldnames=event_data.keys())

            if not self.event_csv_exists:
                writer.writeheader()
                self.event_csv_exists = True

            writer.writerow(event_data)

    def event_to_binary(self, event) -> None:
        """
        Dumps event data to a binary file.

        Args:
            event: An Event object containing the data to be dumped.
        """
        data = event.data
        path = self.filesystem.dumps_event_data_dir / event.dump_filename
        dump_to_binary(data, path)

    def event_summary_to_binary(self, event_summary):
        """
        Dumps an event summary to a binary file.

        Args:
            event_summary: A list of event summary data.
        """
        idx = 0
        file_name = f'events-summary-{str(Utils.get_today_str())}-{idx}.bin'
        path_root = self.filesystem.dumps_event_data_dir
        path = path_root / file_name

        while True: # get a unique filename, so as not to write over previous summaries
            if path.exists():
                idx += 1
                file_name = f'events-summary-{str(Utils.get_today_str())}-{idx}.bin'
                path = path_root / file_name
            else:
                break
        
        dump_to_binary(event_summary, path)

    def save_event_list(self, all_links):
        # write to the day's master list, skipping duplicates
        file_name = 'events-' + Utils.get_today_str() + '.txt'
        path = self.filesystem.input_data_dir / file_name
        self.save_list(path, all_links)

        # write to a new file, for backup, skipping duplicates
        file_name = 'dg-events-' + Utils.get_today_str() + '.txt'
        path = self.filesystem.input_data_dir / file_name
        self.save_list(path, all_links)

    def save_list(self, path, all_links):
        with open(path, 'a', encoding='utf-8') as f:
            for link in all_links:
                if not self.duplicate_in_file(path, link):
                    f.write(link + '\n')
        print(f'Discussion group event links saved to {path}')

    def duplicate_in_file(self, path, text):
        with open(path, 'r', encoding='utf-8') as check:
            for line in check: # skip duplicating entries
                if text in line:
                    return True
            return False

    def write_event_urls(self, urls):
        with open(self.filesystem.get_pages_txt_output_path(), 'a', encoding='utf-8') as f:
            for url in urls:
                f.write(url + '\n')



def dump_to_binary(obj, path):
    '''
    '''
    # dumps the object, to the path, in binary
    with open(path, 'wb') as file:
        pickle.dump(obj, file)
