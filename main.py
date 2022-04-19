import re

import requests
import json
from bs4 import BeautifulSoup

url = 'https://www.nexus.org.uk/metro/timetables-and-stations/ilford-road'

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

train_times_south_y_text = soup.find(id='platform_1_y').get_text()
train_times_south_g_text = soup.find(id='platform_1_g').get_text()

time_format_pattern = "([01]?[0-9]|2[0-3]):([0-5][0-9])?"
times = re.findall(time_format_pattern, train_times_south_y_text)

if __name__ == '__main__':
    # print(train_times_south_y_text)
    # print(train_times_south_g_text)
    print(times)

