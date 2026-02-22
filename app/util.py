from datetime import datetime

class Util:
    def __init__(self):
        pass

    # Format date into ics library compatible format
    @staticmethod
    def format_date(date) -> datetime:
        start_date, end_time_str = date.split(" - ")
        event_start = datetime.strptime(start_date, "%a %m/%d/%Y %I:%M %p")
        end_time    = datetime.strptime(end_time_str,   "%I:%M %p").time()
        event_end   = datetime.combine(event_start.date(), end_time)

        return event_start, event_end
    
    @staticmethod
    def timestamp() -> str:
        ts = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        return ts