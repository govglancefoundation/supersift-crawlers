import scrapy
import json
from scrapy.spiders import SitemapSpider
import re

class RoboticsSpider(SitemapSpider):
    name = "robotics"
    
    def __init__(self):
        with open(f'/Users/santiagosaldivar/Coding/govGlaceCrawler/src/crawl/crawl/websites_to_index/{RoboticsSpider.name}.json', encoding = 'utf-8') as data_file:
            self.data = json.load(data_file)
        self.sitemap_follow = [""]
        self._cbs = []
        for r, c in self.sitemap_rules:
            if isinstance(c, str):
                c = getattr(self, c)
            self._cbs.append((regex(r), c))
        self._follow = [regex(x) for x in self.sitemap_follow]

    def start_requests(self):
        for item in self.data:
            request = scrapy.Request(item['robots_url'], callback=self._parse_sitemap, meta={'stuff':item})
            yield request

    def parse(self, response):
        item = response.meta['stuff']
        title = response.css('title ::text').get()
        if title:
            if "Not Found" not in title:
                yield {
                    'title': response.css('title ::text').get(),
                    'content': response.css('meta[name*=description]::attr(content)').get(),
                    'keywords': response.css('meta[name*=keywords]::attr(content)').get(),
                    'url': response.url,
                    'engine_result_title': item['name'],
                    'engine_result_description': item['description'],
                    'credibility': item['credibility'],
                    'home_url': item['website'],
                    'robots_url': item['robots_url'],
                    'topic': 'Robotics'
                }   

def regex(x):
    if isinstance(x, str):
        return re.compile(x)
    return x