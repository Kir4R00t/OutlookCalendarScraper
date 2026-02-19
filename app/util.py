from datetime import datetime

class Util:
    def __init__(self):
        pass

    # Format date into ics library compatible format
    def format_date(date) -> datetime:
        start_date, end_time_str = date.split(" - ")
        event_start = datetime.strptime(start_date, "%a %m/%d/%Y %I:%M %p")
        end_time    = datetime.strptime(end_time_str,   "%I:%M %p").time()
        event_end   = datetime.combine(event_start.date(), end_time)

        formatted_start_date = datetime.strftime(event_start, "%Y-%m-%d %H:%M:%S")
        formatted_end_date   = datetime.strftime(event_end,   "%Y-%m-%d %H:%M:%S")

        return formatted_start_date, formatted_end_date
    