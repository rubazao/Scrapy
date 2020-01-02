# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest, SplashFormRequest


class SplashAffiliateSpider(scrapy.Spider):
    name = 'splash_affiliate'
    #allowed_domains = ['https://www.crossfit.com/affiliate-list']


    script = '''
	    function main(splash, args)
	  			assert(splash:go(args.url))
	  			assert(splash:wait(0.5))
	  			return splash:html() 
		end
	'''
    
    def start_requests(self):
    	yield SplashRequest(url='https://www.crossfit.com/affiliate-list', endpoint='execute',
    						 args={'wait': 1, 'lua_source': self.script}, callback=self.parse_list_countries)


    def parse_list_countries(self, response):
    	countries = []
    	all_country = response.xpath("//div[@class='form-group']/select[@id='countryFilter']")
    	for country in all_country:
    		yield {
        		'country': country.xpath(".//option[@value]/text()").get()
        	}
    		countries.append(country)
    	
    	yield SplashRequest(url='https://www.crossfit.com/affiliate-list', endpoint='execute',
    						 args={'wait': 0.5, 'lua_source': self.script}, callback=self.parse_affiliates)

    def parse_affiliates(self, response):
    	countries
    	for country in countries:
    		yield SplashFormRequest(url='https://www.crossfit.com/affiliate-list', formxpath="//div[@class='form-group']/select[@id='countryFilter']",
    						 formdata={'option': country} )
    		paises = response.xpath("//table[@id='affiliateTable']/tbody/tr")
    		for pais in paises:
    			yield {
    				'gym name': country.xpath('.//td/a/text()').get(),
        			'local': country.xpath('.//td/text()').get(),
        			'country': country
               	}

     #    next_page = response.xpath('//tfoot//a[last()][@class="btn btn-default btn-xs"]/@href').get()
     #    if next_page is not None:
     #    	next_page = response.urljoin(next_page)
     #    	yield SplashRequest(next_page, callback=self.parse_affiliates)
    	# pass
    	
       
