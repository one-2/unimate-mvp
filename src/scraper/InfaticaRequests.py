
import time
import requests
import json

import Interface
import src.Config as Config

def get_response(url):
    """
    Sends requests to Infatica API for event data and handles retries.

    Args:
        event: An Event object containing the URL to request.

    Returns:
        dict: The response in json
        int: The number of attempts made to get a successful response.
    """
    tries = 0
    while True:
            response = make_infatica_request(url)
            tries += 1
            
            if response.status_code == 200:
                break
            else:
                print(f'\t\tRequest failed with {response.status_code} response.')
                time.sleep(5)
                continue
    return response.json(), tries

def make_infatica_request(url):
    """
    Sends a request to the Infatica API and returns the response.

    Args:
        url: The URL to request data from.

    Returns:
        Response: The response from the Infatica API.
    """
    attempt_number = 0
    while True:
        try:
            response = requests.post('https://scrape.infatica.io/', data = json.dumps({
                'url': str(url),
                'api_key': Config.infatica_api_key,
                'country_code':'au',
            }))
            if response.status_code != 200:
                raise Exception('Bad response: {response}.')
            return response
        except Exception as E:
            print(f'Request failed due to exception "{E}"')
            print("Retrying...")
            time.sleep(5)

            if attempt_number % 3 == 0:
                retry = Interface.Events.scrape_failure(url, attempt_number, E)
                if not retry:
                    print('Skipping @ {url} on attempt {attempt_number}')
                    break

            attempt_number += 1
