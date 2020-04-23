#!/usr/bin/env python3
#
# purpose: Create sample data by hitting auth-api sample endpoints
#          Update auth_api_url and jwt
# usage: python3 ./refresh.py

import requests
import time


def main():
    create_sample_data()


def create_sample_data():
    storefront_api_url = 'http://8404pals.azurewebsites.net/'
    sample_urls = [
        'competition-overview',
        'team-info',
        'match-info',
        'pre-game-scouting',
        'match-scouting',
        'home']

    for sample_url in sample_urls:
        request_endpoint = auth_api_url + '/' + sample_url
        r = requests.get(request_endpoint)

        print(request_endpoint + '\n' + r.text + '\n' + '---')
        time.sleep(3)


if __name__ == "__main__":
    main()
