from scrapy.spider import BaseSpider
from farmworker.items import FarmworkerItem
from scrapy.selector import Selector
import re
import unicodedata
import ast
from ast import literal_eval

class Myspider(BaseSpider):
    name = "fwspider"
    allowed_domains = ["https://libraries.ucsd.edu"]
    start_urls = ["https://libraries.ucsd.edu/farmworkermovement/essay/essays-by-author/"]

    def parse(self, response):
        hxs = Selector(response).xpath('//*[@id="box-2"]/article')
	#titles = hxs.xpath('//*[@id="70s"]/ul/[contains(li,'\d')]/a')
        titles = hxs.xpath('//a[contains(@href,".pdf")]')
	items = []
        for title in titles:
            item = FarmworkerItem()
            item["title"] = title.xpath('text()').extract()
	    item["link"] = title.xpath('@href').extract()
	    item["year"] = str(re.findall(r"(\d{4}s)|(\d{4}.*\d{4})|(\d{4})", ''.join(title.extract())))
	    item["year"] = re.sub(r"\[|\]|u|\,|\(|\)|\"|\'",'',item["year"])
	    items.append(item)
        return items
