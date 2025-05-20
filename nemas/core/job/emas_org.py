import scrapy

from core.domain import gold_price
from datetime import datetime
from core.domain import gold_price_config, gold_price_source
from asgiref.sync import sync_to_async
from core.services.price_service import price_service
from shared_kernel.services.redis_service import redis_service
import math


class HargaEmasSpider(scrapy.Spider):
    name = "harga_emas_org"
    allowed_domains = ["harga-emas.org"]
    start_urls = ["http://harga-emas.org/1-gram/"]

    def parse(self, response):
        # Locate the table with class "in_table" and target the specific row for IDR
        idr_price = response.xpath(
            '//table[@class="in_table"]//tr[td[text()="IDR"]]//td[2]/text()'
        ).get()

        # Clean the extracted price text
        if idr_price:
            idr_price = idr_price.strip()
            print(f"Extracted IDR Price: {idr_price}")

            week_param = ""
            # get day index

            # define price buy and sell from from base price
            price_config = gold_price_config.objects.get(gpc_active=True)

            day_index = datetime.today().weekday()
            print(f"Day Index: {day_index}")
            if day_index == 5 or day_index == 6:
                week_param = "WEEKEND"
            else:
                week_param = "WEEKDAY"

            price_buy = price_config.calculate_price(
                f"BUY{week_param}", float(idr_price.replace(".", "").replace(",", "."))
            )
            price_sell = price_config.calculate_price(
                f"SELL{week_param}", float(idr_price.replace(".", "").replace(",", "."))
            )

            print(f"Price Buy: {price_buy}")
            print(f"Price Sell: {price_sell}")

            gps = gold_price_source(
                gold_price_source="HE",
                gold_price_weight=1,
                gold_price_base=float(idr_price.replace(".", "").replace(",", ".")),
            )
            gps.save()

            # update all price where status is active to not active
            gold_price.objects.filter(gold_price_active=True).update(
                gold_price_active=False
            )

            # save new price
            gprice = gold_price(
                gold_price_source="HE",
                gold_price_sell=math.ceil(price_sell),
                gold_price_buy=math.ceil(price_buy),
                gold_price_base=float(idr_price.replace(".", "").replace(",", ".")),
                gold_price_weight=1,
                timestamps=datetime.now(),
            )
            gprice.save()

            # create object in with price buy and sell then publish it into websocket consumer
            price = {
                "price_buy": price_buy,
                "price_sell": price_sell,
            }

            # redis = redis_service()
            # redis.set("price", str(price))

            print(f"Succesfully saved IDR Price: {idr_price}")
