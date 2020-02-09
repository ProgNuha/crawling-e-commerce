# -*- coding: utf-8 -*-
import scrapy
import os

class EightwoodspiderSpider(scrapy.Spider):
    name = 'eightwoodSpider'
    allowed_domains = ['8wood.id']
    start_urls = ['http://www.8wood.id']

    def start_requests(self):
         """Read category_text from eightwood_categories file and construct the URL"""

        with open(os.path.join(os.path.dirname(__file__), "../resources/eightwood_categories.csv")) as categories:
            for category in csv.DictReader(categories):
                category_text=category["category"]
                url=str(EightwoodspiderSpider.start_urls[0])+"/pakaian/"+category_text+"/"
                # The meta is used to send our search text into the parser as metadata
                yield scrapy.Request(url, callback = self.parse, meta = {"category_text": category_text})

