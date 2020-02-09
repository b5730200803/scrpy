import scrapy
import datetime
from scrapy.http import HtmlResponse , FormRequest, Request

class newsSpider (scrapy.Spider):
    name = 'news'
    start_urls = ['https://oilprice.com/Latest-Energy-News/World-News']
    count = 0

    def parse(self, response):
        for n in response.xpath("//div[@class='categoryArticle']"):
            date = n.xpath(".//div[@class='categoryArticle__content']/p[@class='categoryArticle__meta']/text()").extract_first().split("|",1)[0]
            date = date.split("at",1)[0]
            date_convert = datetime.datetime.strptime(date, "%b %d, %Y ").date()
            sdate = datetime.datetime(date_convert.year, date_convert.month, date_convert.day)
            edate = datetime.datetime.now()
            delta = edate - sdate
            count = int(str(delta).split('day',1)[0])
            url  = n.xpath(".//div[@class='categoryArticle__content']/a/@href").extract_first()
            yield FormRequest(url, callback=self.parse_getdetail)
            
        next_page = response.xpath("//div[@class='pagination']/a[@class='next']/@href").extract_first()
        if next_page is not None and count <= 41:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)
    
    def parse_getdetail(self,response):
        temp = ""
        temp = temp + str(response.xpath("//div[@id='news-content']/p/text()").extract())
        if len(temp) <= 2  :
            temp = temp + str(response.xpath("//div[@id='news-content']/p/span/text()").extract())
        title = response.xpath("//div[@class='singleArticle__content']/h1/text()").extract_first()
        date = str(response.xpath("//div[@class='singleArticle__content']/span/text()").extract()).split("-")[1].replace("']", "")
        content = temp
        link = str(response).split(" ")[1].replace(">", "")
        obj = {'news_link':"",'date':"",'title':"",'content':""}
        obj['news_link'] = link
        obj['date'] = date
        obj['title'] = title
        obj['content'] = content
        
        yield obj        
        
  
        