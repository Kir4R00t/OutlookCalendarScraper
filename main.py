from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver

from dotenv import load_dotenv # type: ignore
import os

class CalendarScraper:
    def __init__(self):
        load_dotenv(".env")
        self.url = os.getenv('CALENDAR_URL')

    def init_driver(self) -> webdriver:        
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        
        driver = webdriver.Chrome(options=options)
        return driver

    def find

    def run(self):
        driver = self.init_driver()
        driver.get(self.url)
        
        print(driver.title)
        driver.quit()

if __name__ == "__main__":
    scraper = CalendarScraper()
    scraper.run()
