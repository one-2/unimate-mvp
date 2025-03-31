from src.Env import *
from src.scraper import Scraper
from src.processor import Tagger
from src.io import Filesystem, Input, Output
import Interface

##### DEBUG INTERFACE
def debug():
    Tagger.tag_all_events(r'urlpath_placeholder.csv')



##### MAIN INTERFACE
def run():
    my_filesystem = Filesystem.Filesystem()
    my_output = Output.Output(my_filesystem)

    options = [
        'Scrape club pages',
        'Scrape DG',
        'Scrape event pages',
        'Scrape club and event pages',
        'Tag events',
    ]
    choice = numeric_choice_template(options)

    if choice == 0:
        Scraper.scrape_club_pages(my_filesystem, my_output)
    elif choice == 1:
        run_dg_scraper(my_filesystem, my_output)
    elif choice == 2: 
        Scraper.scrape_all_events(my_filesystem, my_output)
    elif choice == 3:
        Scraper.scrape_club_pages(my_filesystem, my_output)
        Scraper.scrape_all_events(my_filesystem, my_output)
    elif choice == 4:
        tag_events(my_filesystem)



##### CLUBS
def should_skip_pages():
    while True:
        answer = input('Would you like to skip some entries? y/n ').lower()
        if answer == 'y':
            skip_count = input('How many entries would you like to skip? ')
            while True:
                try:
                    return int(skip_count)
                except:
                    print('Invalid answer. Please try again.')
        elif answer == 'n':
            return 0

def get_clubs_database(filesystem):  # TODO - move part of this to Interface class
    # return pd df from club database csv
    club_database_input_path = filesystem.clubs_database_path()
    if club_database_input_path.exists():
        print(f'Fetched club database from {club_database_input_path}')
        return pd.read_csv(club_database_input_path)
    else:
        print('Enter club database .csv path:')
        return Interface.get_df_from_csv()

##### EVENTS
def get_images():
    question = 'Would you like to download images?'
    response = yes_no_template(question)
    return response

def scrape_failure(url, attempt_number, exception):
    print(f'Scrape @ {url} failed {attempt_number} times due to {exception}. ')
    return retry_template()

def get_events_url_generator(filesystem):
    """
    Generates event URLs from a user-specified text file.

    Returns:
        generator: A URL generator.
    """
    path = filesystem.get_event_list_path()
    
    if path.exists():
        print(f'> Fetched events from {path} .')
        yes = yes_no_template('Do you want to scrape events from this list?')
        if not yes:
            print('Please select a return-delimited .txt list of event links:')
            path = choose_path(filesystem, extension='.txt')
    else:
        print(f'No event list found at path {path}.')
        print('Please select a return-delimited .txt list of event links:')
        path = choose_path(filesystem, extension='.txt')

    return Input.get_generator_from_txt_path(path)



##### DG EVENTS LIST
def run_dg_scraper(filesystem, output):
    # get path
    print('Please select a discussion group html file.')
    path = choose_path(filesystem, extension='.html')

    # call extraction
    Scraper.scrape_discussion_group(path, output)



##### TAGGER
def tag_events(filesystem):
    # warning
    print('WARNING: Input csv must have field "unix_start_timestamp", or this program is going to waste money.')
    input('Press any key to continue')
    
    # get path
    print('\n')
    print('Please select a csv containing event data.')
    path = choose_path(filesystem, extension='.csv')

    # call tag loop
    tagged_df = Tagger.tag_all_events(path)

    # save the tagged df to a csv
    tagged_df.to_csv(filesystem.todays_tagged_csv_path)




##### FILESYSTEM
def choose_path(filesystem, extension='.*'):
    print('1. Select a file from the input folder.')
    print('2. Select a file from the (untagged) output folder.')
    print('3. Select a file from the (tagged) output folder.')
    print('4. Enter a path.')
    path = None
    while True:
        choice = input()
        if choice == '1':
            path = choose_file_from_directory(filesystem.input_data_dir, extension)
            return path
        elif choice == '2':
            path = choose_file_from_directory(filesystem.scraper_output_data_dir, extension)
            return path
        elif choice == '3':
            path = choose_file_from_directory(filesystem.tagger_output_data_dir, extension)
            return path
        elif choice == '4':
            while True:
                print('Please enter a path: ', end='')
                path = Path(input())
                if path.exists() and path.is_file():
                    return path
        print('Invalid input. Please try again.')

def choose_file_from_directory(directory, extension='.*'):
    print_files_in_directory(directory, extension)
    file_list = get_files_in_directory(directory, extension)
    while True:
        try:
            user_input = input("Select a file (0 to exit): ")
            choice = int(user_input)
            if choice == 0:
                exit(0)
            elif 1 <= choice <= len(file_list):
                selected_file = directory / file_list[choice - 1]
                print(f"You selected: {selected_file}")
                return selected_file
            else:
                print("Invalid input. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def print_files_in_directory(directory, extension='.*'):
    # extension takes '.xyz'. set to all extnsns (*) by default.
    if not directory.exists():
        print(f"The directory '{directory}' does not exist.")
        return

    file_list = get_files_in_directory(directory, extension)

    if len(file_list) == 0:
        print(f'No {extension} files found in directory "{directory}".')
    else:
        print(f'{extension} files in the directory:')
        for i, filename in enumerate(file_list, 1):
            print(f"{i}: {filename}")

def get_files_in_directory(directory, extension='.*'):
    # extension takes '.xyz'. set to all extnsns (*) by default.
    if not directory.exists():
        print(f"The directory '{directory}' does not exist.")
        return

    dir_contents = directory.glob(f'*{extension}')
    file_list = [x for x in dir_contents if x.is_file()]
    return file_list



##### GENERIC
def numeric_choice_template(options):
    print('Choose an option:')
    for idx, option in enumerate(options):
        print_idx = idx + 1
        print(f'{print_idx}. {option}')

    while True:
        try:
            choice = int(input()) - 1
            if (choice < 0 or choice > len(options)):
                print('Invalid answer. Please try again.')
            else:
                return choice
        except:
            continue

def retry_template():
    while True:
        choice = input('Do you want to retry? y/n').lower()
        print('\n')
        if choice == 'y':
            return True
        if choice == 'n':
            return False
        else:
            print('Invalid answer. Please try again.')

def yes_no_template(question):
    while True:
        yes = input(question + ' y/n ').lower()
        if yes == 'y':
            return True
        if yes == 'n':
            return False
        else:
            print('Invalid answer. Please try again.')

def get_df_from_csv():
    while True:
        try:
            club_database_input_path = input()
            df = pd.read_csv(club_database_input_path)
            if df is not None:
                break
            else:
                print('Invalid path. Try again.')
        except KeyboardInterrupt:
            print('KeyboardInterrupt detected. Exiting...')
            exit(1)
        except:
            print('Invalid input. Try again.')
    return df

if __name__ == '__main__':
    run()
    # debug()