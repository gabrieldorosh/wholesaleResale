import scrapy
from scrapy.crawler import CrawlerProcess
from selectorlib import Extractor


class AlibabaSpider(scrapy.Spider):
    name = "alibaba"
    start_urls = [   # Load CSV in future
        'https://www.alibaba.com/trade/search?tab=all&searchText=ram',
        'https://www.alibaba.com/trade/search?tab=all&searchText=LEGO'
    ]

    def __init__(self, *args, **kwargs):
        super(AlibabaSpider, self).__init__(*args, **kwargs)
        self.e = Extractor.from_yaml_file('Alibaba.yml')    # Load config YAML file

    def parse(self, response):
        data = self.e.extract(response.text)    # Use YAML config to yield
        
        # Uncomment the following block to extract specific fields
        '''
        for product in data['Products']:
            yield {
                'Name': product['Name'],
                'Price': product ['Price'],
                'Shipping': product['Shipping'],
                'MinQuantity': product['MinQuantity']
            }
        '''

        yield data


# Run the spider
if __name__ == "__main__":
    process = CrawlerProcess(settings={
        'FEEDS': {
            'items.json': {'format': 'json'}    # Scraped data will be stored here
        }
    })

    process.crawl(AlibabaSpider)
    process.start()