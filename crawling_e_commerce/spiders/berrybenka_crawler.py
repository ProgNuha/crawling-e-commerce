# -*- coding: utf-8 -*-
import scrapy
import csv
import os


class BerrybenkaCrawlerSpider(scrapy.Spider):
    name = 'berrybenka_crawler'
    allowed_domains = ['berrybenka.com']
    start_urls = ['https://berrybenka.com']

    def start_requests(self):
        """Read category_text from categories file amd construct the URL"""

        with open(os.path.join(os.path.dirname(__file__), "../resources/categories.csv")) as categories:
            for category in csv.DictReader(categories):
                category_text=category["category"]
                url=str(BerrybenkaCrawlerSpider.start_urls[0])+"/clothing/"+category_text+"/women"
                # The meta is used to send our search text into the parser as metadata
                yield scrapy.Request(url, callback = self.parse, meta = {"category_text": category_text})

