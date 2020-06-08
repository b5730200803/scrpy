from pandas import DataFrame
from bs4 import BeautifulSoup
import json
import os.path
import datetime
import sys

news = {
    'news_link': [],
    'date': [],
    'time_zone': [],
    'title': [],
    'content': [],

}
now = datetime.datetime.now()
date_time = now.strftime("%Y-%m-%d %H.%M.%S")


def getNews(path):
    with open(os.path.abspath( path + '\\virtual_env\\demo_project\\data.json')) as f:
        data = json.load(f)
        for line in data:
            dateInfo = line['date'].split(" ")
            line['date'] = line['date'].replace(dateInfo[len(dateInfo)-1], "")

        sorted_data = sorted(data, key=lambda x: datetime.datetime.strptime(
            x['date'], ' %b %d, %Y, %I:%M %p '), reverse=True)
        for line in sorted_data:
            news['news_link'].append(str(line['news_link']))
            news['date'].append(str(line['date']))
            news['time_zone'].append('CST')
            news['title'].append(str(line['title']))
            news['content'].append(str(line['content']))


def toJson(path):
    fileName = path + '\\virtual_env\\demo_project\\' + 'news'+'.json'
    with open(fileName, 'w') as f:
        json.dump(news, f)


def main():
    path = sys.path[0].replace('\\pythonfile', '')
    getNews(path)
    toJson(path)


main()
