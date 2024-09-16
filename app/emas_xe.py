import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class HargaEmasXESpider(scrapy.Spider):
    name = "gold_price"

    def __init__(self, *args, **kwargs):
        super(HargaEmasXESpider, self).__init__(*args, **kwargs)
        # Set up Selenium WebDriver
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")  # run in headless mode (without opening a browser)
        self.driver = webdriver.Remote(
            command_executor='http://app.selenium:4444/wd/hub',  # Updated URL with SELENIUM_URL
            options=chrome_options
        )
    
    def start_requests(self):
        # URL of the XE gold to IDR conversion page
        url = 'https://www.xe.com/currencyconverter/convert/?Amount=1&From=XAU&To=IDR'
        yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        self.driver.get(response.url)  # Load the page with Selenium

        try:
            # Wait for the conversion result to be visible (timeout after 10 seconds)
            wait = WebDriverWait(self.driver, 10)
           
            # Use a more general XPath to get the conversion result
            conversion_element = wait.until(EC.presence_of_element_located((By.XPATH, '//p[contains(text(), "Indonesian Rupiahs")]/preceding-sibling::p')))
            
            # Extract the text (e.g., "39,804,840.80 Indonesian Rupiahs")
            conversion_rate = conversion_element.text
            
            # Extract only the numeric part (if needed)
            gold_price_idr = conversion_rate.split(' ')[0]  # Extracts "39,804,840.80"

            # Return the scraped data
            yield {
                'gold_price_idr': gold_price_idr,
            }

        except Exception as e:
            self.logger.error(f"Error during scraping: {e}")
        
    def close(self, reason):
        self.driver.quit()  # Close the Selenium browser when spider finishes
