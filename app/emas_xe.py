
import scrapy
from core.models import gold_price_rate

class HargaEmasXESpider(scrapy.Spider):
    name = "harga_emas_xe"
    allowed_domains = ["xe.com"]
    start_urls = ["https://www.xe.com/currencyconverter/convert/?Amount=1&From=XAU&To=IDR"]

    def parse(self, response):
        
        rows = response.css('table tbody tr')
        xau_idr_value = None
        for row in rows:
            xau_value = row.css('td:nth-child(1) a::text').get()
            print(f"XAU: {xau_value}")
            if xau_value == '1':
                idr_value = row.css('td:nth-child(2)::text').get()
                
                print(f"XAU: {xau_value}, IDR: {idr_value}")
                xau_idr_value = {
                    'XAU': xau_value,
                    'IDR': idr_value
                }
                break  # Exit loop after finding the 1 XAU value

        if xau_idr_value:
            gold_price = gold_price_rate(gold_price_rate_source='XE', gold_price_rate_base=xau_idr_value['IDR'], gold_price_rate_weight=1)
            gold_price.save()
            print(f"Saved XAU to IDR rate: {xau_idr_value['IDR']}")
            # yield xau_idr_value
            
    # name = "gold_price"

    # def __init__(self, *args, **kwargs):
    #     super(HargaEmasXESpider, self).__init__(*args, **kwargs)
    #     # Set up Selenium WebDriver
    #     chrome_options = webdriver.ChromeOptions()
    #     chrome_options.add_argument("--headless")  # run in headless mode (without opening a browser)
    #     self.driver = webdriver.Remote(
    #         command_executor='http://app.selenium:4444/wd/hub',  # Updated URL with SELENIUM_URL
    #         options=chrome_options
    #     )
    
    # def start_requests(self):
    #     # URL of the XE gold to IDR conversion page
    #     url = 'https://www.xe.com/currencyconverter/convert/?Amount=1&From=XAU&To=IDR'
    #     yield scrapy.Request(url=url, callback=self.parse)
    
    # def parse(self, response):
    #     self.driver.get(response.url)  # Load the page with Selenium

    #     try:
    #         # Wait for the conversion result to be visible (timeout after 10 seconds)
    #         wait = WebDriverWait(self.driver, 10)
           
    #         # Use a more general XPath to get the conversion result
    #         conversion_element = wait.until(EC.presence_of_element_located((By.XPATH, '//p[contains(text(), "Indonesian Rupiahs")]/preceding-sibling::p')))
            
    #         # Extract the text (e.g., "39,804,840.80 Indonesian Rupiahs")
    #         conversion_rate = conversion_element.text
            
    #         # Extract only the numeric part (if needed)
    #         gold_price_idr = conversion_rate.split(' ')[0]  # Extracts "39,804,840.80"

    #         # Return the scraped data
    #         yield {
    #             'gold_price_idr': gold_price_idr,
    #         }

    #     except Exception as e:
    #         self.logger.error(f"Error during scraping: {e}")
        
    # def close(self, reason):
    #     self.driver.quit()  # Close the Selenium browser when spider finishes
