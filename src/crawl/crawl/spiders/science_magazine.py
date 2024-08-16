import scrapy
import json
from scrapy.spiders import SitemapSpider
import re

class ScienceMagazineSpider(SitemapSpider):
    name = "science_magazine"

    def __init__(self):
        with open('/Users/santiagosaldivar/Coding/govGlaceCrawler/src/crawl/crawl/science_magazine.json', encoding = 'utf-8') as data_file:
            self.data = json.load(data_file)
        self.sitemap_follow = ["article"]
        self._cbs = []
        for r, c in self.sitemap_rules:
            if isinstance(c, str):
                c = getattr(self, c)
            self._cbs.append((regex(r), c))
        self._follow = [regex(x) for x in self.sitemap_follow]

    def start_requests(self):
        for item in self.data[:1]:
            request = scrapy.Request(item['robots_url'], callback=self._parse_sitemap, meta={'stuff':item})
            yield request

    def parse(self, response):
        item = response.meta['stuff']
        print(item)
        yield {
            'title': response.css('title ::text').get(),
            'engine_result_description': item['description'],
            'content': response.css('meta[name*=description]::attr(content)').get(),
            'url': response.url,
            'keywords': response.css('meta[name*=keywords]::attr(content)').get(),
            'home_url': item['website'],
            'credibility': item['credibility'],
            'robots_url': item['robots_url'],
            'topic': item['topic']
        }   

def regex(x):
    if isinstance(x, str):
        return re.compile(x)
    return x