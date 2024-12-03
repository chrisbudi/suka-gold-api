from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from django.core.management.base import BaseCommand

from core.job import HargaEmasSpider
from shared_kernel.services.redis_service import redis_service
from core.services.price_service import price_service


class Command(BaseCommand):
    help = "Run Scrapy spider"

    def handle(self, *args, **kwargs):
        process = CrawlerProcess(get_project_settings())
        process.settings.set("FEED_FORMAT", "json")
        process.settings.set("HTTPCACHE_ENABLED", False)

        # add spider to process
        process.crawl(HargaEmasSpider)

        process.start()
        process.stop()

        self.stdout.write(self.style.SUCCESS("Scrapy spider successfully executed"))

        # update price web socket
        # run_harga_emas_update()

        redis = redis_service()
        price = redis.get("price")

        if price:
            priceService = price_service()
            priceService.publish_price(price)

        return "Execute process harga emas success"
