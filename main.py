#
# Script Name: TAW Metro Times
# Author: Joe Murphy - 19/04/2022
#

import re
import requests
from bs4 import BeautifulSoup

# Get train times for STATION from Nexus.org using requests, parse HTML and return.
def get_train_times(station):
    url = f'https://www.nexus.org.uk/metro/timetables-and-stations/{station}'
    response = requests.get(url)
    raw_train_times = BeautifulSoup(response.text, 'html.parser')

    # TODO Change IDs for different directions of travel and platforms.
    # Find train times by their HTML ID. The second 'g' variable may not exist on the page if
    # no more trains are running to that destination.
    train_times_y_text = raw_train_times.find(id='platform_1_y').get_text()
    train_times_g_text = raw_train_times.find(id='platform_1_g').get_text()
    return train_times_y_text, train_times_g_text

# Return requested train times in a human readable format. This removes 'this train terminates at X' from
# being added to the list of train times.
def format_train_times(train_times):
    time_24h_format_pattern = "([01]?[0-9]|2[0-3]):([0-5][0-9])?"
    formatted_train_times = re.findall(time_24h_format_pattern, train_times)
    return formatted_train_times

if __name__ == '__main__':
    unformatted_ilford_road_train_times = get_train_times('ilford-road')
    formatted_ilford_road_train_times = format_train_times(unformatted_ilford_road_train_times)
    print(formatted_ilford_road_train_times)
