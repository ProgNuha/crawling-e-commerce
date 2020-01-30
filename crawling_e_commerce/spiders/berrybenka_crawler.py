# -*- coding: utf-8 -*-
import scrapy
import csv
import os

from ..items import CrawlingECommerceItem

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

    def parse(self, response):
        """Function to process clothes category results page"""
        product_category=response.meta["category_text"]
        products=response.xpath("//*[(@id='li-catalog')]")
        
        # item containers for storing product
        items = CrawlingECommerceItem()

        # iterating over search results
        for product in products:
            # Defining the XPaths
            XPATH_PRODUCT_LINK=".//a/@href"
            XPATH_PRODUCT_NAME=".//div[@class='catalog-detail']//div[@class='detail-left']//h1/text()"
            XPATH_PRODUCT_PRICE=".//div[@class='catalog-detail']//div[@class='detail-right']//p/text()"
            XPATH_PRODUCT_IMAGE_LINK=".//div[@class='catalog-image']//img/@src"

            # print(product)

            raw_product_name=product.xpath(XPATH_PRODUCT_NAME).get()
            raw_product_price=product.xpath(XPATH_PRODUCT_PRICE).get()
            raw_product_image_link=product.xpath(XPATH_PRODUCT_IMAGE_LINK).get()
            raw_product_link=product.xpath(XPATH_PRODUCT_LINK).get()
            
            # cleaning the data
            product_name=''.join(raw_product_name).strip(
            ) if raw_product_name else None
            product_price=''.join(raw_product_price).strip(
            ) if raw_product_price else None
            product_image_link=''.join(raw_product_image_link).strip(
            ) if raw_product_image_link else None
            product_link=''.join(raw_product_link).strip(
            ) if raw_product_link else None

            # storing item
            items['product_name']=product_name
            items['product_price']=product_price
            items['product_link_url']=product_link
            items['product_image_url']=raw_product_image_link
            items['product_image']=product_name
            items['product_category']=product_category

            yield items
            
