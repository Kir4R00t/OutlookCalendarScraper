from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import StaleElementReferenceException

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
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
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        options.add_argument("--start-maximized")
        options.add_argument(
            "user-agent=Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/121.0.0.0 Safari/537.36"
        )
        driver = webdriver.Chrome(options=options)
        driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        return driver

    # TODO: finds all events but in the current month
    #       Need to click to like +3months ahead

    def find_all_events(self, driver, timeout: int = 10 ):
        wait = WebDriverWait(driver, timeout)
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-itemindex]")))
        
        return driver.find_elements(By.CSS_SELECTOR, "div[data-itemindex]")
    
    def get_event_data(self, driver, event, timeout: int = 10):
        wait = WebDriverWait(driver, timeout)

        # Try clicking on an event
        event_el = wait.until(EC.element_to_be_clickable(event))
        try:
            event_el.click()
        except (StaleElementReferenceException, Exception):
            event_el = wait.until(EC.element_to_be_clickable(event))
            driver.execute_script("arguments[0].click();", event_el)
        
        popup = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[role="dialog"], div[role="region"]'))
        )
        
        # After popup opens -> try getting title & desc
        try:
            title = WebDriverWait(popup, 3).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'span[aria-label="Title"]'))
            ).text.strip()
        except TimeoutException:
            title = ""
        
        try:
            desc= WebDriverWait(popup, 3).until( 
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[visibility="hidden"]')) 
            ).text.strip()
        except TimeoutException:
            desc = ""    


        driver.switch_to.active_element.send_keys(Keys.ESCAPE)
        return title, desc


    def run(self):
        driver = self.init_driver()
        driver.get(self.url)
        
        events = self.find_all_events(driver)
        
        parsed_events = [] # TODO: parse events here -> extract links
        for event in events:
            parsed_events.append(self.get_event_data(driver, event))

        for e in parsed_events:
            print(e)
        
        driver.quit()

if __name__ == "__main__":
    scraper = CalendarScraper()
    scraper.run()
