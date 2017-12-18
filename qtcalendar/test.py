'''
    Test module, so that you know how this works. Look at it, read the comments and
    work out your way to your own implementation.

    Note: imports should be at the beginning of the file, I will put them through out it
    just so you now explicitly what is used for what, and what you can avoid.
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

# Add the calendar widget to your application holder
ui.getMainLayout().addWidget(cal.getView())

# Start UI
ui()
