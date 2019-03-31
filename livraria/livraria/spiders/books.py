# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest


class BooksSpider(scrapy.Spider):
    name = 'books'
    #allowed_domains = ['livraria.seminariodefilosofia.org']
    #start_urls = ['https://livraria.seminariodefilosofia.org/']
    
    #Very important set a correct time to wait in order to get the page loaded completely.
    script = '''
        function main(splash, args)
        assert(splash:go(args.url))
        assert(splash:wait(5))
        return splash:html()
        end
    '''
    current_page = 1

    def start_requests(self):
        yield SplashRequest(url='https://livraria.seminariodefilosofia.org/', endpoint='execute', args={'wait': 0.5, 'lua_source': self.script}, callback=self.parse)

    def parse(self, response):
        all_books_urls = response.xpath("//div[@class='name']/a")
        for book in all_books_urls:
            yield SplashRequest(url=book.xpath(".//@href").extract_first(), callback=self.parse_data, endpoint='execute', args={'wait': 0.5, 'lua_source': self.script})

    def parse_data(self, response):
        yield {
            'Autor': response.xpath("//div[@class='details']/h3/a/text()").get(),
            'Livro': response.xpath("//div[@class='details']/h1/text()").get(),
            'ISBN': response.xpath("//div[@class='detail'][position()=3]/span/text()").get(),
            'Editora': response.xpath("//div[@class='detail'][position()=5]/span/a/text()").get()
        }
