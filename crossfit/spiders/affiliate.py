# -*- coding: utf-8 -*-
import scrapy
import json


class AffiliateSpider(scrapy.Spider):
    name = 'affiliate'
    #allowed_domains = ['cms-api.crossfit.com']
    page_number = 2

    #alternative_url = 'https://cms-api.crossfit.com/affiliates/me?page_size=420&page=2'
    # 'https://www.crossfit.com/cf/find-a-box.php?page=1'
    def start_requests(self):
        yield scrapy.Request('https://cms-api.crossfit.com/affiliates/me?page_size=420&page=1', callback=self.parse)

    def parse(self, response):
        data = json.loads(response.body)
        affiliates = data.get("affiliates")
        for affiliate in affiliates:
            yield {
                'name': affiliate.get('name'),
                'city': affiliate.get('city'),
                'state': affiliate.get('full_state'),
                'country': affiliate.get('country')
                # 'active' : affiliate.get('active')
            }

        # if 'name' == 50:
        #     page = 1
        #     for i in range(1000000):
        #         page = i+1

        next_page = 'https://cms-api.crossfit.com/affiliates/me?page_size=420&page=' + \
            str(AffiliateSpider.page_number)
        if AffiliateSpider.page_number < 25:
            AffiliateSpider.page_number += 1
            yield scrapy.Request(next_page, callback=self.parse)
