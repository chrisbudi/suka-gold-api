import scrapy
import calendar

from core.models import gold_price
from datetime import datetime
from core.models import gold_price_config, gold_price_source 
from asgiref.sync import sync_to_async



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
            
            day_index = calendar.day_name[datetime.now().weekday()] 
            print(f"Day Index: {day_index}")
            
            # define price buy and sell from from base price
            price_buy_config = gold_price_config.objects.get(gpc_code=f'BUYDAY1') # BUYDAY[day_index]
            price_sell_config = gold_price_config.objects.get(gpc_code=f'SELLDAY1') # SELLDAY[day_index]
            
            
            
            price_buy = price_buy_config.calculate_price(float(idr_price.replace('.', '').replace(',', '.')))
            price_sell = price_sell_config.calculate_price(float(idr_price.replace('.', '').replace(',', '.')))
            print(f"Price Buy: {price_buy}")
            print(f"Price Sell: {price_sell}")
            gps =  gold_price_source(gold_price_source='HE',
                                    gold_price_weight=1,
                                    gold_price_base=float(idr_price.replace('.', '').replace(',', '.')))
            gps.save()
        
            gprice = gold_price(gold_price_source='HE',
                                gold_price_sell=price_sell,
                                gold_price_buy=price_buy ,
                                gold_price_base=float(idr_price.replace('.', '').replace(',', '.')), 
                                gold_price_weight=1,
                                timestamps=datetime.now(), ) 
            gprice.save()
            print(f"Succesfully saved IDR Price: {idr_price}")
