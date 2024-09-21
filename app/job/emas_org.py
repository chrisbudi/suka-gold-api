import scrapy
from core.models import gold_price
from datetime import datetime


class HargaEmasSpider(scrapy.Spider):
    name = "harga_emas_org"
    allowed_domains = ["harga-emas.org"]
    start_urls = ["https://harga-emas.org/1-gram/"]

    def parse(self, response):
        # Locate the table with class "in_table" and target the specific row for IDR
        idr_price = response.xpath('//table[@class="in_table"]//tr[td[text()="IDR"]]//td[2]/text()').get()
        
        # Clean the extracted price text
        if idr_price:
            idr_price = idr_price.strip()
            print(f"Extracted IDR Price: {idr_price}")
            gprice = gold_price(gold_price_source='HE',
                                gold_price_sell =float(idr_price.replace('.', '').replace(',', '.')),
                                gold_price_buy=float(idr_price.replace('.', '').replace(',', '.')) ,
                                gold_price_base=float(idr_price.replace('.', '').replace(',', '.')), 
                                gold_price_weight=1,
                                timestamps=datetime.now(), ) 
            gprice.save()
            print(f"Succesfully saved IDR Price: {idr_price}")
