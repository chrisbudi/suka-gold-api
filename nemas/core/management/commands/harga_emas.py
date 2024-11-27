from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from django.core.management.base import BaseCommand

from core.job import HargaEmasSpider


class Command(BaseCommand):
    help = "Run Scrapy spider"

    def handle(self, *args, **kwargs):
        process = CrawlerProcess(get_project_settings())
        process.settings.set("FEED_FORMAT", "json")
        process.settings.set("HTTPCACHE_ENABLED", False)

        # add spider to process
        process.crawl(HargaEmasSpider)

        process.start()
