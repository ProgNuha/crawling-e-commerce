# -*- coding: utf-8 -*-
import scrapy
import os

class EightwoodspiderSpider(scrapy.Spider):
    name = 'eightwoodSpider'
    allowed_domains = ['8wood.id']
    start_urls = ['http://www.8wood.id']

    def start_requests(self):
        
