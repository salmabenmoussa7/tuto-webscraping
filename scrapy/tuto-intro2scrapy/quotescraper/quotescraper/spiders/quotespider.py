import scrapy

from quotescraper.items import QuotescraperItem

     
class QuotespiderSpider(scrapy.Spider):
    name = "quotespider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]

    def parse(self, response):
        quotes = response.css('div.quote')
        for quote in quotes:
            item = QuotescraperItem()
            item['text'] = quote.xpath('span[@class="text"]/text()').get()
            item['author'] = quote.xpath('span/small[@class="author"]/text()').get()
            item['tags'] = quote.xpath('div[@class="tags"]/a[@class="tag"]/text()').getall()
            yield item

        next_page = response.css('li.next a ::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
            
# ----------------------------------------- SCRAPING AND PRINTING IN TERMINAL, NOT USING ITEMS
# class QuotespiderSpider(scrapy.Spider):
#     name = "quotespider"
#     allowed_domains = ["quotes.toscrape.com"] #the spider is going to go through a lot of links, it a sort of protection for the spider
#     start_urls = ["http://quotes.toscrape.com/"]

#     def parse(self, response):
#         quotes = response.css('div.quote')
#         for quote in quotes:
#             yield {
#                 'citation': quote.xpath('span[@class="text"]/text()').get(), #CMD F + CMD V TO TEST THE GENERALIZED XPATH
#                 'author': quote.xpath('span/small[@class="author"]/text()').get(),
#                 'tag': quote.xpath('div[@class="tags"]/a[@class="tag"]/text()').getall(),
#             }
#         next_page = response.css('li.next a ::attr(href)').get()
#         if next_page:
#             yield response.follow(next_page, callback=self.parse)