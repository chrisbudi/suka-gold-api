from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from django.core.management.base import BaseCommand
# from emas_org import HargaEmasSpider

from job import HargaEmasXESpider, HargaEmasSpider
# from app.emas_xe import harga_emas_spider

class Command(BaseCommand):
    help = 'Run Scrapy spider'

    def handle(self, *args, **kwargs):
        process = CrawlerProcess(get_project_settings())
        process.settings.set('FEED_FORMAT', 'json')
        
        # format disable cache
        process.settings.set('HTTPCACHE_ENABLED', False)


        
        
        # process.settings.set('FEED_URI', 'output.json) 
        # add spider to process
        process.crawl(HargaEmasSpider)
        # process.crawl(HargaEmasXESpider)  
        
        process.start()
        
        