from holder.minimal import MinimalHolder
from calendar import EventInCalendar, Event
import datetime as dt

ui = MinimalHolder()

# Create an Event
event = Event(
    dt.datetime(2017, 12, 13, 9, 0, 0),
    dt.datetime(2017, 12, 13, 21, 0, 0))

# Create an event entry (EventInCalendar)
ecalendar = EventInCalendar()
ecalendar.setEvent(event)
ui.getMainLayout().addWidget(ecalendar.getView())

# Start UI
ui()
