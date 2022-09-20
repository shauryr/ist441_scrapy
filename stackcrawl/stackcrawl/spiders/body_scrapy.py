"""
This spider will crawl all the questions on datascience stack exchange

to run `scrapy crawl getquestions`

This is a follow spider and it will keep adding urls to the queue which have subdomain as /questions/
Question heading, question body and answers are extracted from the html
BeautifulSoup is used to extract the accepted answer.
"""


from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
import jsonlines


class someSpider(CrawlSpider):
    # name of spider
    name = "getquestions"

    # make the crawler stick to this domain
    allowed_domains = ["datascience.stackexchange.com"]

    # picking the most aswered question so that there are a lot of next URLs to crawl
    start_urls = [
        "https://datascience.stackexchange.com/questions/6107/what-are-deconvolutional-layers"
    ]

    # Rule - to crawl only subdomains which have "questions" in them and follow them
    rules = (
        Rule(LinkExtractor(allow="/questions/*"), callback="parse_obj", follow=Trues),
    )

    def parse_obj(self, response):
        
        # open file to write the crawled data
        with jsonlines.open("data.jsonl", mode="a") as writer:

            url = response.url # get the url from response object
            
            # get question heading
            question_head = response.xpath(
                '//div[@id="question-header"]/h1/a/text()'
            ).get()
            
            # get question body
            question_body = " ".join(
                response.xpath('//div[@class="s-prose js-post-body"]/p/text()').getall()
            )

            # when scrapy's inbuilt functions are not enough use BS4
            
            # get accepted answer
            soup = BeautifulSoup(response.text, "lxml")
            html = [
                x.text
                for x in soup.find_all("div", attrs={"class": "answer accepted-answer"})
            ]
            html = " ".join(html)
            html = " ".join(line.strip() for line in html.split("\n"))
            if html:
                answer_body = html
            
            # if there is no accepted answer just get the first answer
            else:
                html = [x.text for x in soup.find_all("div", attrs={"class": "answer"})]
                html = " ".join(html)
                html = " ".join(line.strip() for line in html.split("\n"))
                answer_body = html
                
            # arrange everything in a dictionary
            obj = {
                "url": url,
                "question_head": question_head,
                "question_body": question_body,
                "answer_body": answer_body,
            }
            
            # write dictionary to jsonl file
            writer.write(obj)
