from dotenv import load_dotenv
import os

from scraper import CalendarScraper
from ics_generator import IcsGenerator


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
    print("Scraping complete :)")
