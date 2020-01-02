# -*- coding: utf-8 -*-
import scrapy
import json


class AffiliateSpider(scrapy.Spider):
    name = 'affiliate'

    #alternative_url = 'https://cms-api.crossfit.com/affiliates/me?page_size=420&page=2'
    # 'https://www.crossfit.com/cf/find-a-box.php?page=1'

    # Initialize the first URL

    def start_requests(self):
        yield scrapy.Request(url='https://cms-api.crossfit.com/affiliates/me?page_size=420&page=1',
                             callback=self.parse,
                             meta={
                                 'current_page': 1
                             }
                             )
    # Parse data from url (JSON / API)

    def parse(self, response):
        data = json.loads(response.body)
        affiliates = data.get("affiliates")
        for affiliate in affiliates:
            try:
                name = affiliate.get('name')
                city = affiliate.get('city')
                state = affiliate.get('full_state')
                country = affiliate.get('country')
                yield {
                    'name': name,
                    'city': city,
                    'state': state,
                    'country': country
                }
            except:
                pass
                print("No more pages to scrape.")

        # Give access to next pages of the JSON / API file
        current_page = response.request.meta['current_page'] + 1
        yield scrapy.Request(
            url=f'https://cms-api.crossfit.com/affiliates/me?page_size=420&page={current_page}',
            callback=self.parse,
            meta={
                'current_page': current_page
            }
        )