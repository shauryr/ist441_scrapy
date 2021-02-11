import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class someSpider(CrawlSpider):
    name = 'stackcrawl'
    item = []

    allowed_domains = ['datascience.stackexchange.com']
    start_urls = ['https://datascience.stackexchange.com/questions/88488/deep-learning-test-loss-curve-wont-go-down']

    rules = (Rule (LinkExtractor(allow="/questions/*"), callback="parse_obj", follow=True),)

    def parse_obj(self,response):
        filename = 'links.txt'
        with open(filename, 'a') as f:
            f.write(str(response.url)+'\n')
        self.log('Saved file %s' % filename)