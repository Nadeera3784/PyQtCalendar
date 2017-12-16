from holder.minimal import MinimalHolder
from entities import EventInCalendar, Date, Event, Calendar
import datetime as dt


test_num = 1

ui = MinimalHolder()

if test_num == 0:
    print('Test 0')

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
elif test_num == 1:
    print('Test 1')

    cal = Calendar()

    # Create events
    init_date = dt.date(2017, 11, 30)
    for i in range(31):
        init_date += dt.timedelta(1)
        event = Event(
            dt.datetime(init_date.year, init_date.month, init_date.day, 1, 0, 0),
            dt.datetime(init_date.year, init_date.month, init_date.day, 10, 0, 0))
        event2 = Event(
            dt.datetime(init_date.year, init_date.month, init_date.day, 3, 0, 0),
            dt.datetime(init_date.year, init_date.month, init_date.day, 12, 0, 0),
            fulfillment=0.5)
        event3 = Event(
            dt.datetime(init_date.year, init_date.month, init_date.day, 5, 0, 0),
            dt.datetime(init_date.year, init_date.month, init_date.day, 20, 0, 0),
            fulfillment=0.9)
        ecalendar = EventInCalendar()
        ecalendar.setEvent(event)
        ecalendar2 = EventInCalendar()
        ecalendar2.setEvent(event2)
        ecalendar3 = EventInCalendar()
        ecalendar3.setEvent(event3)

        date = Date(init_date)
        date.addCalendarEvent(ecalendar)
        date.addCalendarEvent(ecalendar2)
        date.addCalendarEvent(ecalendar3)

        date.changeDateType(0)

        cal.addDate(date)
    ui.getMainLayout().addWidget(cal.getView())

# Start UI
ui()
