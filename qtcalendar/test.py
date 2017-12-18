'''
    Test module, so that you know how this works. Look at it, read the comments and
    work out your way to your own implementation.

    Note: imports should be at the beginning of the file, I will put them through out it
    just so you know explicitly what is used for what, and what you can avoid.
'''

from example.holder.minimal import MinimalHolder
from entities import Calendar

ui = MinimalHolder()

'''
    Lets create a calendar, suppose we want a calendar with sunday as the lead day
    and with Colombian holidays. We do not want to modify anything else so, leave
    the datatree as the default one.
    Normally you need to supply the holiday list, lucky for you, a module in examples
    already does the work for you.
'''
from example.connector import HolidayDownloader
from models import Calendar__Model

holidays = HolidayDownloader().getHolidayDates()
lead_day = Calendar__Model.TYPE_SUNDAY_LEADING

# Create the calendar instance
cal = Calendar(holidays=holidays, leading_day=lead_day)


'''
    The previous code should give you a working calendar with no events (already
    displayed). Now lets add an event in a date
    of our choice. For that we will have to assign a minimal description for our
    event, the description contains:
     * place: the name of the place
     * people: amount of people going
     * init-date: datetime
     * end-date: datetime
     * fulfillment: how ready is the event
'''
import datetime as dt

date_selected = dt.date.today()
next_day = date_selected + dt.timedelta(1)

# Suppose our event starts at 17:00 and ends at 3:00 of the next day
description = {
    'place': 'Disney',
    'people': 202,
    'init-date': dt.datetime.combine(date_selected, dt.time(17, 0, 0)),
    'end-date': dt.datetime.combine(next_day, dt.time(1, 0, 0)),
    'fulfillment': 1.0
}

cal.createEvent(description)

# Add the calendar widget to your application holder
ui.getMainLayout().addWidget(cal.getView())

# Start UI
ui()
