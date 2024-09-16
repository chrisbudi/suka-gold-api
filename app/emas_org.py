import scrapy


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
            yield {
            'IDR_price': idr_price,
            }