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

    def parse(self, response):
        """Function to process 8wood category results page"""
        product_category=response.meta["category_text"]
        products=response.xpath("//div[@class='p-list']")
        
        # iterating over search results
        for product in products:
            # get produck outstock tag
            XPATH_PRODUCT_OUTSTOCK_TAG=".//div[@class='img']//span[@class='outstock']"
            is_onstock = len(product.xpath(XPATH_PRODUCT_OUTSTOCK_TAG)) == 0

            # get data if product is onstock
            if is_onstock: 
                # Defining the XPaths
                XPATH_PRODUCT_NAME=".//div[@class='desc']//h5/a/text()"
                XPATH_PRODUCT_PRICE=".//div[@class='desc']//div[@class='price-box']//span[@class='regular-price']//span[@class='price']/text()"
                XPATH_PRODUCT_IMAGE_LINK=".//div[@class='img']//a[@class='product-image-custom']//img[contains(@class,'imgThumProduct')]/@data-original"
                XPATH_PRODUCT_LINK=".//div[@class='desc']//h5/a/@href"

                raw_product_name=product.xpath(XPATH_PRODUCT_NAME).extract()
                raw_product_price=product.xpath(XPATH_PRODUCT_PRICE).extract()
                raw_product_image_link=product.xpath(XPATH_PRODUCT_IMAGE_LINK).extract()
                raw_product_link=product.xpath(XPATH_PRODUCT_LINK).extract()
                
                # cleaning the data
                product_name=''.join(raw_product_name).strip(
                ) if raw_product_name else None
                product_price=''.join(raw_product_price).strip(
                ) if raw_product_price else None
                product_image_link=''.join(raw_product_image_link).strip(
                ) if raw_product_image_link else None
                product_link=str(EightwoodspiderSpider.start_urls[0])+''.join(raw_product_link).strip(
                ) if raw_product_link else None
                
