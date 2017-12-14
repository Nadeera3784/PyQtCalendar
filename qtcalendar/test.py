from holder.minimal import MinimalHolder
from entities import EventInCalendar, Date, Event
import datetime as dt

ui = MinimalHolder()

# Create an Event
event = Event(
    dt.datetime(2017, 12, 13, 9, 0, 0),
    dt.datetime(2017, 12, 13, 21, 0, 0))
event2 = Event(
    dt.datetime(2017, 12, 13, 10, 0, 0),
    dt.datetime(2017, 12, 13, 19, 0, 0),
    fulfillment=1.0)
event3 = Event(
    dt.datetime(2017, 12, 13, 7, 0, 0),
    dt.datetime(2017, 12, 13, 15, 0, 0),
    fulfillment=1.0)

# Create an event entry (EventInCalendar)
ecalendar = EventInCalendar()
ecalendar.setEvent(event)
ecalendar2 = EventInCalendar()
ecalendar2.setEvent(event2)
ecalendar3 = EventInCalendar()
ecalendar3.setEvent(event3)

# Create a Date object and add the previously created calendar entry
date = Date(dt.datetime.today())
date.addCalendarEvent(ecalendar)
date.addCalendarEvent(ecalendar2)
date.addCalendarEvent(ecalendar3)

# Add the date to the layout
ui.getMainLayout().addWidget(date.getView())

# Start UI
ui()
