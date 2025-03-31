import json
import re
import string

import src.Config as Config

def extract_html_as_dict(html, start_string) -> dict:
    """
    Extracts a dictionary from an HTML string starting from a specified point.

    Args:
        html (str): The HTML string to extract data from.
        start_string (str): The string indicating the start of extraction.

    Returns:
        dict: A dictionary containing the extracted data.
    """
    start_idx = html.index(start_string)
    extracted = extract_matching_braces(html[start_idx:])
    return json.loads(extracted)

def extract_matching_braces(input_string):
    """
    Extracts content enclosed in curly braces '{}' from a given string.

    Args:
        input_string (str): The string from which to extract content.

    Returns:
        str or None: The content enclosed in braces, or None if no braces are found.
    """
    open_brace_index = -1
    close_brace_index = -1
    stack = []

    for i, char in enumerate(input_string):
        if char == '{':
            if not stack:
                open_brace_index = i
            stack.append('{')
        elif char == '}' and stack:
            stack.pop()
            if not stack:
                close_brace_index = i
                break

    if open_brace_index != -1 and close_brace_index != -1:
        return input_string[open_brace_index:close_brace_index + 1]
    else:
        return None

def extract_id_from_url(url) -> str:
    numeric_chars = re.findall(r'\d', url)
    numeric_string = ''.join(numeric_chars)
    return str(numeric_string)

def extract_event_links(html, is_for_dg):
    # returns a list of event links contained in the html
    if is_for_dg:
        matches = get_matching_substrings_dg(html, Config.url_stub_placeholder, 21)
    else:
        matches = get_matching_substrings(html, Config.url_stub_placeholder, 21)  # look for an event url
    matches = [retrieve_good_page_link(match) for match in matches] # make links good
    matches = list(set(matches))  # use set's constructor to remove duplicates
    return matches

def get_matching_substrings(string, substring, trailing_string_length=0):
    # used by clubscraper
    # TODO - why are these different !!!?
    matches = find_substring_indices(string, substring)
    links = []
    for start in matches:
        end = start + len(substring) + trailing_string_length
        links.append(string[start:end])
    return links

def find_substring_indices(string, substring):
    # find occurences of substring in a string
    # used by clubscraper
    start = 0
    indices = []
    while start < len(string):
        index = string.find(substring, start)
        if index == -1:
            break  # no more such substrings
        indices.append(index)
        start = index + 1
    return indices

def get_matching_substrings_dg(string, substring, trailing_string_length=0):
    # used by dgscraper
    # TODO - why are these different !!!?
    matches = re.finditer(substring, string)
    links = []
    for match in matches:
        start = match.start()  # Get the characters from the start of the match
        end = start + len(substring) + trailing_string_length
        links.append(string[start:end])
    return links

def retrieve_good_page_link(input_link):
    processed = input_link.replace('\\', '')
    while not processed.endswith('/'):
        processed = processed[0:-1]
    return processed