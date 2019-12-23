# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

class RankSpider(scrapy.Spider):
    name = 'rank'
    allowed_domains = ['www.reclameaqui.com.br']


    script = '''
    	function main(splash, args)
		  splash.private_mode_enabled = false
		  splash:set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36")
		  url = args.url
		  assert(splash:go(url))
		  assert(splash:wait(1))
		  splash:set_viewport_full()
		  return {
		    html = splash:html()    
		  }
		end
'''
    def start_requests(self):
    	yield SplashRequest(url='https://www.reclameaqui.com.br/ranking/', callback=self.parse, endpoint="execute", args={
    		'lua_source': self.script
    		})

    def parse(self, response):
        for rank in response.xpath('//div[@class="col-md-4 col-sm-6 flexbox-col ng-scope"]'):
        	yield {
        		'title': rank.xpath('.//div/h2/text()').get(),
        	}
