from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
import jsonlines


class someSpider(CrawlSpider):
    name = 'getquestions'
    allowed_domains = ['datascience.stackexchange.com']
    start_urls = ['https://datascience.stackexchange.com/questions/6107/what-are-deconvolutional-layers']
    rules = (Rule (LinkExtractor(allow="/questions/*"), callback="parse_obj", follow=True),)
    
    def parse_obj(self,response):
        with jsonlines.open('data.jsonl', mode='a') as writer:

            url = response.url
            question_head = response.xpath('//div[@id="question-header"]/h1/a/text()').get()
            question_body = ' '.join(response.xpath('//div[@class="s-prose js-post-body"]/p/text()').getall())
            
            soup = BeautifulSoup(response.text, 'lxml')
            html = [x.text for x in soup.find_all("div",attrs={"class":"answer accepted-answer"})]
            html = ' '.join(html)
            html = " ".join(line.strip() for line in html.split("\n"))
            if html:
                answer_body = html
            else:
                html = [x.text for x in soup.find_all("div",attrs={"class":"answer"})]
                html = ' '.join(html)
                html = " ".join(line.strip() for line in html.split("\n"))
                answer_body = html
                
            obj = {
                'url' : url,
                'question_head': question_head,
                'question_body': question_body,
                'answer_body': answer_body
            }
            writer.write(obj)