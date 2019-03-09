import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy import log
#from scrapy import *
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
#from scrapy.spider import BaseSpider
from scrapy.http import Request


class QuotesSpider(scrapy.Spider):
    name = "DukeMain"

    def start_requests(self):
        urls = [
            'https://www.duke.edu'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'dukepage-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)


        le = LinkExtractor()  # empty for getting everything, check different options on documentation
        links = le.extract_links(response)
        filename = 'duke_homepagelinks.txt'
        with open(filename, 'w') as f:
            for link in links:
                f.write(str(link)+ '\n')
        self.log('Saved file %s' % filename)
process = CrawlerProcess({
    'USER_AGENT': 'Chrome'
    #'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(QuotesSpider)
process.start()


