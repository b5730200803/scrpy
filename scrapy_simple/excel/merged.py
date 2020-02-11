from pandas import DataFrame
from bs4 import BeautifulSoup
import json
import os.path
import datetime
news = {
    'news_link': [],
    'date': [],
    'time_zone':[],
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
            temp = line['date'].replace(" CST", "")
            line['date'] = datetime.datetime.strptime(temp ,' %b %d, %Y, %I:%M %p')

            news['news_link'].append(str(line['news_link']))
            news['date'].append(str(line['date']))
            news['time_zone'].append('CST')
            news['title'].append(str(line['title']))
            news['content'].append(str(line['content']))

    with open(os.path.abspath('virtual_env\demo_project\data2.json')) as f2:
        data = json.load(f2)
        sorted_data = sorted(data, key=lambda x: datetime.datetime.strptime(x['date'].split(" ",1)[0] , '%d/%m/%Y'), reverse = True)
        
        for line in sorted_data:
            temp = line['date'].split(" ")
            line['date'] = temp[0]+" "+temp[2]
            line['date'] = datetime.datetime.strptime(line['date'], '%d/%m/%Y %H.%M.%S')
            
            news['news_link'].append(str(line['news_link']))
            news['date'].append(str(line['date']))
            news['time_zone'].append('CIT')
            news['title'].append(str(line['title']))
            news['content'].append(str(line['content']))

    

def toExcel():
    df =  DataFrame(news,columns=['news_link', 'date','time_zone', 'title', 'content'])
    export_excel = df.to_excel (r'C:\Users\supaK\Desktop\scrapy_simple\excel\excelfile\excel_detail('+date_time+').xlsx', index = None, header=True)
    

def main(): 
    getNews()
    toExcel()

main()