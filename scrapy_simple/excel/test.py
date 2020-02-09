from pandas import DataFrame
from bs4 import BeautifulSoup
import json
import os.path
import datetime
news = {
    'news_link': [],
    'date': [],
    'title': [],
    'content':[],
}
now = datetime.datetime.now()
date_time = now.strftime("%Y-%m-%d %H.%M.%S")

def getNews():
    with open(os.path.abspath('virtual_env\demo_project\data.json')) as f:
        data = json.load(f)
        sorted_data = sorted(data, key=lambda x: datetime.datetime.strptime(x['date'].replace(" CST", "") , ' %b %d, %Y, %I:%M %p'), reverse = True)
        for line in sorted_data:
            news['news_link'].append(str(line['news_link']))
            news['date'].append(str(line['date']))
            news['title'].append(str(line['title']))
            news['content'].append(str(line['content']))
def toExcel():
    print(len(news['news_link']))
    print(len(news['date']))
    print(len(news['title']))
    print(len(news['content']))

    df =  DataFrame(news,columns=['news_link', 'date', 'title', 'content'])
    export_excel = df.to_excel (r'C:\Users\supaK\Desktop\scrapy_simple\excel\excelfile\excel_detail('+date_time+').xlsx', index = None, header=True)

def main(): 
    getNews()
    toExcel()

main()