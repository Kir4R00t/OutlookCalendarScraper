from icalendar import Calendar, Event

from util import Util

class IcsGenerator:
    def __init__(self):
        self.calendar = Calendar()
    
    def create_event(self, title, date, desc) -> None:
        e = Event()

        ics_compatible_date = Util.format_date(date)
        event_start_date = ics_compatible_date[0]
        event_end_date   = ics_compatible_date[1]
        
        e.add("summary", title)
        e.add("description", desc)
        e.add("dtstart", event_start_date)
        e.add("dtend", event_end_date)
        
        self.calendar.add_component(e)

        with open("outlook.ics", "wb") as f:
            f.write(self.calendar.to_ical())

