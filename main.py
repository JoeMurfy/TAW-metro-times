#
# Script Name: TAW Metro Times
# Author: Joe Murphy - 19/04/2022
#

from datetime import datetime
import re
import requests
from bs4 import BeautifulSoup


class TrainsProcessor:
    # Get train times for STATION from Nexus.org using requests, parse HTML and return.
    def get_train_times(self, departs_from, terminates_at):
        url = f'https://www.nexus.org.uk/metro/timetables-and-stations/{departs_from}'
        response = requests.get(url)
        raw_train_times = BeautifulSoup(response.text, 'html.parser')

        # TODO Change IDs for different directions of travel and platforms.
        # Find train times by their HTML ID. The second 'g' variable may not exist on the page if
        # no more trains are running to that destination.
        if terminates_at == 'south-hylton':
            train_times_text = raw_train_times.find(id='platform_1_g').get_text()
        elif terminates_at == 'south-shields':
            train_times_text = raw_train_times.find(id='platform_1_y').get_text()
        elif terminates_at == 'any':
            train_times_text_g = raw_train_times.find(id='platform_1_g').get_text()
            train_times_text_y = raw_train_times.find(id='platform_1_y').get_text()
            train_times_text = train_times_text_g + train_times_text_y
        return train_times_text

    # This strips 'this train terminates at X' and any other characters/symbols from being added
    # to the list of train times. Converts times to datetime format for easier sorting and modification.
    def format_train_times(self, train_times_text):
        time_24h_format_pattern = "[0-9][0-9]:[0-9][0-9]"
        stripped_time_list = re.findall(time_24h_format_pattern, train_times_text)
        for i, time in enumerate(stripped_time_list):
            datetime_formatted = datetime.strptime(time, '%H:%M')
            stripped_time_list[i] = datetime_formatted.strftime('%H:%M')
        return stripped_time_list

    def closest_time(self, train_times):
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        return min(time for time in train_times if time > current_time)

    def retrieve(self, departs_from, terminates_at):
        unformatted = self.get_train_times(departs_from, terminates_at)
        formatted = self.format_train_times(unformatted)
        return formatted

def get_current_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    return current_time

if __name__ == '__main__':

    train_times = TrainsProcessor()
    train_time_list = train_times.retrieve('central-station', 'any')

    print('Current Time: ' + get_current_time())
    print('The next train is at: ' + train_times.closest_time(train_time_list))
