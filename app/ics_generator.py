from ics import Calendar, Event
from app import util

class IcsGenerator:
    def __init__(self):
        self.calendar = Calendar()
    
    def create_event(self, title, date, desc) -> None:
        e = Event()

        ics_compatible_date = util.format_date(date)
        event_start_date = ics_compatible_date[0]
        event_end_date   = ics_compatible_date[1]
        
        e.name          = title
        e.begin         = event_start_date
        e.end           = event_end_date 
        e.description   = desc # Either meet link or the classroom nr
        
        self.calendar.events.add(e)
