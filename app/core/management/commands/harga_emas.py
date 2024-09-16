from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from django.core.management.base import BaseCommand
# from emas_org import HargaEmasSpider
from emas_xe import HargaEmasXESpider
# from app.emas_xe import harga_emas_spider

class Command(BaseCommand):
    help = 'Run Scrapy spider'

    def handle(self, *args, **kwargs):
        process = CrawlerProcess(get_project_settings())
        
        # add spider to process
        # process.crawl(HargaEmasSpider)
        process.crawl(HargaEmasXESpider)  
        
        process.start()
        
        