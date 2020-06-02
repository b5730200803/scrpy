import scrapy
import datetime
from scrapy.http import FormRequest, Request
import json
import os.path
import unidecode 

list_json = []
with open(os.path.abspath('data.json')) as file:
    data = json.load(file)
    sorted_data = sorted(data, key=lambda x: datetime.datetime.strptime(x['date'].replace(" CST", "") , ' %b %d, %Y, %I:%M %p'), reverse = True)
    
    for line in sorted_data:
        list_json.append(line) #ใส่ list ที่ sort แล้ว

    temp = str(sorted_data[0]['date']).split(",",2)
    lastDate = temp[0]+","+temp[1]
    lastDate_convert = datetime.datetime.strptime(lastDate, " %b %d, %Y").date()
    # lastDate_convert = datetime.datetime(lastDate_convert.year, lastDate_convert.month, lastDate_convert.day)
    lastTime = temp[2]
    
class newsSpider (scrapy.Spider):
    name = 'oilnews'
    start_urls = ['https://oilprice.com/Latest-Energy-News/World-News']
    count = 0
    isContinue = False
    def parse(self, response):
        for n in response.xpath("//div[@class='categoryArticle']"):
            date = n.xpath(".//div[@class='categoryArticle__content']/p[@class='categoryArticle__meta']/text()").extract_first().split("|",1)[0]
            date_convert = datetime.datetime.strptime(date, "%b %d, %Y at %H:%M ").date()
            # sdate = datetime.datetime(date_convert.year, date_convert.month, date_convert.day) #วันในข่าวปัจจุบัน
            # edate = datetime.datetime.now() #วันในปัจจุบัน
            # delta = edate - sdate 
            # count = int(str(delta).split('day',1)[0]) #จำนวนวันที่ห่างกันของเวลาข่าวกับเวลาปัจุบัน
            
            # checkDateGetData = edate - lastDate_convert
            # checkCount = int(str(checkDateGetData).split('day',1)[0]) #จำนวนที่ต่างกันของข่าวที่เก็ทมาล่าสุด กับเวลาปัจจุบัน

            url  = n.xpath(".//div[@class='categoryArticle__content']/a/@href").extract_first() # link เข้าไปในเนื้อหาข่าว
            isContinue = False
            if lastDate_convert < date_convert:
                isContinue = True
                yield FormRequest(url, callback=self.parse_getdetail)

            
        next_page = response.xpath("//div[@class='pagination']/a[@class='next']/@href").extract_first()
        if next_page is not None and isContinue:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)
    
    def parse_getdetail(self,response):
        temp = ""
        for i in response.css('div#news-content > p:nth-child(n+1)'):
            temp = temp + unidecode.unidecode(str(''.join(i.xpath('descendant-or-self::text()').extract())).replace('\n', ""))
                
        title = unidecode.unidecode(response.xpath("//div[@class='singleArticle__content']/h1/text()").extract_first())
        date = str(response.xpath("//div[@class='singleArticle__content']/span/text()").extract()).split("-")[1].replace("']", "")
        content = temp
        link = str(response).split(" ")[1].replace(">", "")
        obj = {'news_link':"",'date':"",'title':"",'content':""}
        obj['news_link'] = link
        obj['date'] = date
        obj['title'] = title            
        obj['content'] = content

        with open(os.path.abspath('data.json'),"r") as jsonFile:
            data = json.load(jsonFile)
            data.insert(0,obj)

        with open(os.path.abspath('data.json'),"w")as jsonFile2:
            json.dump(data,jsonFile2)

        yield obj        
    
            
  
        