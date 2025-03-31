# Stephen Elliott
# (c) Conta Digital Pty Ltd
# v0.9 - 2/11/23

import datetime
import math
import random
import time

import src.Config as Config

def print_dict_structure(d, indent=0):
    """
    Recursively prints the structure of a nested dictionary with indentation.

    Args:
        d (dict): The dictionary to be printed.
        indent (int, optional): The level of indentation. Defaults to 0.
    """
    for key, value in d.items():
        if isinstance(value, dict):
            print(' ' * indent + f'Key: {key}')
            print_dict_structure(value, indent + 4)
        else:
            print(' ' * indent + f'Key: {key}, Value: {value}')

def get_today_str():
    return datetime.datetime.today().strftime('%Y-%m-%d')

def event_is_past(event):
    timestamp = event['unix_start_timestamp']
    if timestamp is not None and not math.isnan(timestamp):
        timestamp = int(timestamp)
        converted_timestamp = datetime.datetime.fromtimestamp(round(timestamp / 1000))
        current_time_utc = datetime.datetime.utcnow()
        return (converted_timestamp <= current_time_utc)
    return None

def random_sleep(min_sleep=1, max_sleep=10):
    # sleep for a uniformly random period of time
    sleep_interval = random.uniform(min_sleep, max_sleep)
    time.sleep(sleep_interval)
    print(f"> Slept for {sleep_interval:.2f} seconds.")

def is_valid_page_link(url):  # TODO - move up - doesn't need its own func
    # check whether the given url matches the required page url expression
    return url.__class__ is str and url.__contains__(Config.url_stub_placeholder)

def add_closing_slash(url):
    # add closing slash to the url if it's not present
    if url[-1:] != '/':
        url += '/'
    return url