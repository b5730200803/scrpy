import json
import scrapy
from scrapy.http import FormRequest, Request
import os.path
import datetime

now = datetime.datetime.now()
date_time = now.strftime("%Y-%m-%d %H.%M.%S")

with open(os.path.abspath('C:\\Users\\MiniPair\\Desktop\\scrpy\\scrapy_simple\\virtual_env\demo_project\\data2.json')) as file:
    data = json.load(file)
    sorted_data = sorted(data, key=lambda x: datetime.datetime.strptime(
        x['date'].split(" ", 1)[0], '%d/%m/%Y'), reverse=True)

    lastDate = str(sorted_data[0]['date']).split(" ", 1)[0]
    lastDate_convert = datetime.datetime.strptime(lastDate, "%d/%m/%Y").date()


class getDetail (scrapy.Spider):
    name = 'hellenic'
    start_urls = [
        'https://www.hellenicshippingnews.com/category/oil-energy/oil-companies-news']
    isContinue = False

    def parse(self, response):
        for i in range(1, 16):
            for n in response.xpath("//article[@class='item-list item_"+str(i)+"']"):
                url = n.xpath(
                    ".//h2[@class='post-title']/a/@href").extract_first()
                date = n.xpath(
                    ".//p[@class='post-meta']/span/text()").extract_first()
                date_convert = datetime.datetime.strptime(
                    date, "%d/%m/%Y").date()
                isContinue = False
                if lastDate_convert < date_convert:
                    isContinue = True
                    yield FormRequest(url, callback=self.parse_getdetail)

        next_page = response.xpath(
            "//div[@class='pagination']/span[@id='tie-next-page']/a/@href").extract_first()
        if next_page is not None and isContinue:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)
        else:
            page_num = int(str(response).split("/", 5)[5].split("/")[2])
            page_num = page_num + 1
            next_page_link = response.urljoin(
                "https://www.hellenicshippingnews.com/category/oil-energy/oil-companies-news/page/"+str(page_num)+"/")
            print(next_page_link)
            yield scrapy.Request(url=next_page_link, callback=self.parse)

    def parse_getdetail(self, response):
        temp = ""
        temp = temp + \
            str(response.xpath("//div[@class='entry']/p/text()").extract())
        title = response.xpath(
            "//h1[@class='name post-title entry-title']/span/text()").extract_first()
        date = response.xpath(
            ".//span[@class='tie-date']/text()").extract_first()
        link = str(response).split(" ")[1].replace(">", "")
        content = temp
        obj = {'news_link': "", 'date': "", 'title': "", 'content': ""}
        obj['news_link'] = link
        obj['date'] = date+" "+str(date_time)
        obj['title'] = title
        obj['content'] = content

        with open(os.path.abspath('data2.json'), "r") as jsonFile:
            data = json.load(jsonFile)
            data.insert(0, obj)

        with open(os.path.abspath('data2.json'), "w") as jsonFile2:
            json.dump(data, jsonFile2)

        yield obj
