import os, tempfile, json
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class FlipkartspiderSpider(CrawlSpider):
    name = 'flipkartspider'
    # start_urls = ['https://www.flipkart.com/search?q=home%20decor&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off']


    rules = (
        Rule(LinkExtractor(restrict_xpaths=("//div[@class='_2kHMtA' or @class='_4ddWXP']/a")), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths="(//nav[@class='yFHi8N']/a)[last()]")),
        )

    with open(os.path.join(tempfile.gettempdir(),'start_urls.json')) as tempurlfilepointer:
        start_urls = json.loads(tempurlfilepointer.read())['urls']
        print(f'here be the start urls {start_urls}')

    def parse_item(self, response):
        item = {}
        item['parent_url'] = response.request.headers['referer'].decode('utf-8'),
        item['product mame'] = response.xpath("//h1[@class='yhB1nd']/span[1]/text()").extract_first().replace("\xa0\xa0", ""),
        item['price'] = response.xpath("//div[@class='_30jeq3 _16Jk6d']/text()").extract(),
        item['description'] = response.xpath("//div[@class='_2418kt']//li/text()").extract(),
        item['Url'] = response.url
        return item


        #//*[@id="container"]/div/div[3]/div/div[2]/div[26]/div/div/nav/a[12]
        #//*[@id="container"]/div/div[3]/div/div[2]/div[26]/div/div/nav/a[12]
