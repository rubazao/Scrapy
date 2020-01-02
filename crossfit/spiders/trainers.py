# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest


class TrainersSpider(scrapy.Spider):
    name = 'trainers'
    #allowed_domains = ['crossfit.com']
    

    script = '''
	    function main(splash, args)
			  assert(splash:go(args.url))
			  assert(splash:wait(0.5))
			  
			  input_box = assert(splash:select(".form-control"))
			  input_box:focus()
			  input_box:send_keys("<Tab>")
			  input_box:send_keys("<Tab>")
			  input_box:send_keys("<Tab>")
			  input_box:send_keys("<Tab>")
			  input_box:send_text("Brazil")
			  assert(splash:wait(0.5))
			  
			  input_box:send_keys("<Enter>")
			  assert(splash:wait(5))
			  
			  return splash:html()
		end
	'''
	

    def start_requests(self):
        yield SplashRequest(url='https://trainerdirectory.crossfit.com/', endpoint='execute', args={'wait': 0.5, 'lua_source': self.script}, callback=self.parse)

    def parse(self, response):
        all_trainers = response.xpath('//table[@class="table table-condensed trainer-results"]/tbody/tr')
        for trainers in all_trainers:
        	yield {
        		'trainer': trainers.xpath('.//td/ul/li/text()').get(),
        		'local': trainers.xpath('.//td/ul/li[2]/text()').get(),
        		'credential': trainers.xpath('.//td[3]/ul/li/b/text()').get(),
        		'credentials_add': trainers.xpath('.//td[3]/ul/li/text()').getall()
        	}

        next_page = response.xpath('//tfoot//a[last()][@class="btn btn-default btn-xs"]/@href').get()
        if next_page is not None:
        	next_page = response.urljoin(next_page)
        	yield SplashRequest(next_page, callback=self.parse)

