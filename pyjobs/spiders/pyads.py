# -*- coding: utf-8 -*-
import scrapy


class PyadsSpider(scrapy.Spider):
    name = 'pyads'
    allowed_domains = ['pyjobs.com.br']
    start_urls = ['https://pyjobs.com.br']

    def parse(self, response):
        links = response.xpath('//div[@class="card-body"]/a/@href').getall()
        for link in links:
            yield scrapy.Request(response.urljoin(link), callback=self.parse_category)


        pages_url = response.xpath('//div//ul//li/a[@class="page-link"]/@href').getall()
        for page in pages_url:
            yield scrapy.Request(
                response.urljoin(page),
                callback=self.parse,
            )

    def parse_category(self, response):
         title = response.xpath('//div//h1[@class="text-info"]/text()').get()
         place = response.xpath('//div[@class="block-heading"]/p[position()=1]/text()').get()
         company = response.xpath('//div[@class="block-heading"]/p[position()=2]/text()').get()
         date = response.xpath('//div[@class="block-heading"]/p[position()=3]/text()').get()
         tags = response.xpath('//div[@class="answer"]/span/text()').getall()
         description = response.xpath('//div[@class="faq-item"][position()=2]/div/p/text()').getall()
         requisites = response.xpath('///div[@class="faq-item"][position()=3]/div/p/text()').getall()

         yield{
                 'title': title,
                 'place': place,
                 'company': company,
                 'date': date,
                 'tags': tags,
                 'description': description,
                 'requisites': requisites,
                 'url': response.url

             }
             