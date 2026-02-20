from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    StaleElementReferenceException, 
    TimeoutException
)
from selenium import webdriver
import logging
import re

from time import sleep

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class CalendarScraper:
    def __init__(self, url):
        self.url = url

    def init_driver(self) -> webdriver:        
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=2560,1440")
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


    def get_event_data(self, driver, event, timeout: int = 10) -> str:
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
        
        # Get title
        try:
            title = WebDriverWait(popup, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'span[aria-label="Title"]'))
            ).text.strip()
        except TimeoutException:
            title = ""
        
        # Get date
        try:
            date = WebDriverWait(popup, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[class="WWT_Z"]'))
            ).text.strip()
        except TimeoutException:
            date = ""
        
        # Get meet link
        try:
            desc= WebDriverWait(popup, 5).until( 
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[visibility="hidden"]')) 
            )
            desc = (desc.get_attribute("textContent") or "").strip()

            meet_url_base = r"https://teams\.microsoft\.com/meet/\S+"

            match = re.search(meet_url_base, desc)
            if match: meet_link = match.group(0)

        # Since there is no meet link -> Get location
        except TimeoutException:
            meet_link = None

            try:
                loc = WebDriverWait(popup, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'span[class="QI7ov"]'))
                ).text.strip()
            
                classroom_pattern = r"Sala:\s*\d+"
                match = re.search(classroom_pattern, loc)
                if match: classroom = match.group(0)

            except TimeoutException:
                classroom = ""

        driver.switch_to.active_element.send_keys(Keys.ESCAPE) # close popup

        # Mark events as Remote or OnSite classes
        event_data = []
        if meet_link:   event_data  = ["[Remote] " + title, date, meet_link]
        else:   event_data          = ["[OnSite] " + title, date, classroom] 

        logger.info(f"Event scraped: {event_data}")
        return event_data

    def parse_all_events(self, driver, timeout: int = 10 ) -> list[WebElement]:
        event_locator   = "div[data-itemindex]"
        button_locator  = 'i[data-icon-name="Down"]'

        wait = WebDriverWait(driver, timeout)
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, event_locator)))
        
        parsed_events_data = []

        # Initial collection
        events = driver.find_elements(By.CSS_SELECTOR, event_locator)
        for event in events:
            parsed_events_data.append(self.get_event_data(driver, event))

        # Collect 3 months ahead
        for i in range(3):
            driver.find_element(By.CSS_SELECTOR, button_locator).click()
            sleep(10) # TODO: This is just a temporary solution -> wait for old elements to become 'stale' ?
            events = driver.find_elements(By.CSS_SELECTOR, event_locator)
            for event in events:
                parsed_events_data.append(self.get_event_data(driver, event))


        return parsed_events_data
    
    
    def run(self) -> list:
        driver = self.init_driver()
        driver.get(self.url)
        
        parsed_events = self.parse_all_events(driver)

        return parsed_events
