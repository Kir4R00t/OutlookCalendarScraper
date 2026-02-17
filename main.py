from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
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

    # TODO: finds all events but in the current month
    def find_all_events(self, driver, timeout: int = 15):
        wait = WebDriverWait(driver, timeout)
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-itemindex]")))
        
        return driver.find_elements(By.CSS_SELECTOR, "div[data-itemindex]")
    
    def run(self):
        driver = self.init_driver()
        driver.get(self.url)
        
        events = self.find_all_events(driver)
        
        driver.quit()

if __name__ == "__main__":
    scraper = CalendarScraper()
    scraper.run()
