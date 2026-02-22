from dotenv import load_dotenv
import logging
import os

from scraper import CalendarScraper
from ics_generator import IcsGenerator
from util import Util

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class App:
    def __init__(self):
        load_dotenv(".env")
        self.url = os.getenv('CALENDAR_URL')

    def runApp(self) -> None:
        events  = CalendarScraper(self.url).run()
        ics_gen_inst = IcsGenerator()

        for event in events:
            e_title = event[0]
            e_date  = event[1]
            e_desc  = event[2]
        
            ics_gen_inst.create_event(e_title, e_date, e_desc)


if __name__ == "__main__":
    app = App()
    app.runApp()
    logger.info(f"[{Util.timestamp()}] - Scraping finished :)")