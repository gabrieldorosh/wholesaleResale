import scrapy
from scrapy.crawler import CrawlerProcess
from selectorlib import Extractor


class AlibabaSpider(scrapy.Spider):
    name = "alibaba"

    def __init__(self, query1=None, query2=None, *args, **kwargs):
        super(AlibabaSpider, self).__init__(*args, **kwargs) 
        self.start_urls = [
        f'https://www.alibaba.com/trade/search?tab=all&searchText={query1}',
        f'https://www.alibaba.com/trade/search?tab=all&searchText={query2}'
    ]
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
    query1 = input("Enter query 1: ").replace(" ", "+") # Format for URL
    query2 = input("Enter query 2: ").replace(" ", "+")

    process = CrawlerProcess(settings={
        'FEEDS': {
            'items.json': {'format': 'json'}    # Scraped data will be stored here
        }
    })

    process.crawl(AlibabaSpider, query1=query1, query2=query2)
    process.start()