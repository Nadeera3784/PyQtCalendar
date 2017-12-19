'''
    Models for QtWidgets
'''
from collections import deque
from math import ceil
import datetime as dt
import calendar


class EventInCalendar__Model:
    class Text:
        @staticmethod
        def getDefault():
            return EventInCalendar__Model.Text()

        def __init__(self, event=None, overflow=False):
            if event is None:
                self.init_date = dt.datetime(1, 1, 1)
                self.end_date = dt.datetime(9999, 12, 31)
                self.place = Event__Model.Place()
            else:
                if overflow:
                    self.init_date = dt.datetime.combine(
                        event.getInitDate().date(), dt.time(0, 0, 0))
                else:
                    self.init_date = event.getInitDate()
                self.end_date = event.getEndDate()
                self.place = event.getPlace()

        def __str__(self):
            init_time, end_time = self.init_date.time(), self.end_date.time()

            return '  '.join([str(i) for i in [init_time, end_time, self.place]])

    @staticmethod
    def colorOf(val):
        range_list = [
            (0.0, 0.2, 'rgb(178, 0, 0)'),
            (0.2, 0.5, 'rgb(255, 40, 40)'),
            (0.5, 0.7, 'rgb(191, 165, 0)'),
            (0.7, 1.0, 'rgb(252, 224, 45)'),
            (1.0, 1.1, 'rgb(46, 234, 81)'),
        ]

        for lw, hi, c in range_list:
            if lw <= val and hi > val:
                return c

    def __init__(self, master, overflow):
        self._fulfillment = 0.0
        self._overflow = overflow
        self._master = master
        self._event = None

    def getFulFillmentStatus(self, numeric=False):
        if not numeric:
            return EventInCalendar__Model.colorOf(self._fulfillment)
        return self._fulfillment

    def setEvent(self, event):
        self._event = event.getModel()
        self._fulfillment = self._event.getFulFillmentStatus()

    def __str__(self):
        if self._event is None:
            return EventInCalendar__Model.Text().__str__()
        return EventInCalendar__Model.Text(self._event, self._overflow).__str__()


class Event__Model:
    class Place:
        def __init__(self, name='NA', people=0):
            self.name = name
            self.people = people

        def __str__(self):
            return self.name

    def __init__(self, init_date, end_date, place, fulfillment=0.0):
        self._init_date = init_date
        self._end_date = end_date
        self._place = place
        self._fulfillment = fulfillment

    def getFulFillmentStatus(self):
        return self._fulfillment

    def getInitDate(self):
        return self._init_date

    def getEndDate(self):
        return self._end_date

    def getPlace(self):
        return self._place


class Date__Model:
    TYPE_WEEKDAY = 0
    TYPE_WEEKEND = 1
    TYPE_HOLYDAY = 2
    TYPE_FREEDAY = 3
    TYPE_GRAYDAY = 4

    @staticmethod
    def colorOf(val):
        color_list = [
            (Date__Model.TYPE_WEEKDAY, (219, 219, 219)),
            (Date__Model.TYPE_WEEKEND, (183, 183, 183)),
            (Date__Model.TYPE_HOLYDAY, (183, 183, 183)),
            (Date__Model.TYPE_FREEDAY, (0, 216, 255)),
            (Date__Model.TYPE_GRAYDAY, (255, 255, 255)),
        ]

        for d, c in color_list:
            if d == val:
                return c
        return color_list[0][1]

    def __init__(self, master, date):
        self._master = master

        self._events = list()
        self._date = date
        self._date_type = Date__Model.TYPE_WEEKDAY

    def setDate(self, date, datetype=TYPE_WEEKDAY):
        self._date = date
        self._date_type = datetype

    def getDate(self):
        return self._date

    def getDateType(self, numeric=False):
        if numeric is False:
            return Date__Model.colorOf(self._date_type)
        return self._date_type

    def addEvent(self, event):
        self._events.append(event)

    def getEvents(self):
        return self._events


class Calendar__Model:
    TYPE_MONDAY_LEADING = 0
    TYPE_TUESDAY_LEADING = 1
    TYPE_WEDNESDAY_LEADING = 2
    TYPE_THURSDAY_LEADING = 3
    TYPE_FRIDAY_LEADING = 4
    TYPE_SATURDAY_LEADING = 5
    TYPE_SUNDAY_LEADING = 6

    MAX_DIM_X = 7
    MAX_DIM_Y = 6

    WEEKENDS = [5, 6]

    @staticmethod
    def dayOf(date, init, datatree):
        '''
            Returns the day of the week of a given date and the position
            of that day in the calendar grid.
            The returned text value of the day is recovered from the stringer module.
        '''
        days = datatree['str']['days']

        # Get the day of the week of the selected date
        datetuple = tuple([int(s) for s in str(date).split(' ')[0].split('-')])
        day = days[list(zip(*days))[0].index(calendar.weekday(*datetuple))][1]

        # Horizontal position in the grid is deduced from the selected leading day
        days_dq = deque(days)
        days_dq.rotate(7 - init)
        pos_x = list(zip(*days_dq))[0].index(calendar.weekday(*datetuple))

        # Vertical position is deduced from the selected leading day and the
        # day of the first date of that month
        firstmonthday = (datetuple[0], datetuple[1], 1)
        fday = list(zip(*days_dq))[0].index(calendar.weekday(*firstmonthday))

        pos_y = ceil((fday + date.day) / 7) - 1

        # Return the place in the calendar grid depending on the offset
        return day, pos_x, pos_y

    def __init__(self, master, datatree, ctype=TYPE_SUNDAY_LEADING, holidays=list()):
        '''
            Calendar constructor, a calendar is an array of dates that should
            always be full, thus, initialy an array of empty dates (6x7), is
            array is called holders;  a second empty array of dates is created
            and will replace eventually the dates of the respective holder date.

            Both arrays are validated through a snapshot array, the snapshot refers
            to the dates that fill the Calendar grid for a current month, be those
            dates from the actual month or the adjacent months
        '''
        self._master = master
        self._type = ctype

        self._holidays = holidays

        # Get data source
        self._datatree = datatree

        # Assume month as current month
        self._month = tuple([dt.date.today().year, dt.date.today().month])

        # Generate the snapshot for the current month
        self._snapshot = self.generateSnapshot()

        # Create empty dates from the snapshot
        self._dates = self.generateDefaultDates()

    def generateSnapshot(self):
        rt = list()

        if self._month is None:
            return rt

        # First day of month
        first_day = dt.date(self._month[0], self._month[1], 1)

        # Find day of first position in calendar grid
        offset = Calendar__Model.dayOf(first_day, self._type, self._datatree)[1]
        first_day -= dt.timedelta(offset)

        # Once first position is encountered, fill the holder array
        for i in range(Calendar__Model.MAX_DIM_X * Calendar__Model.MAX_DIM_Y):
            rt.append(first_day)
            first_day += dt.timedelta(1)

        return rt

    def generateDefaultDates(self):
        rt = list()
        for date in self._snapshot:
            created_date = self._master.createDate(date)
            self.setDateType(created_date)
            rt.append(created_date)
        return rt

    def addDate(self, date):
        if self._month is not None:
            if date.getModel().getDate() in self._snapshot:
                index = self._snapshot.index(date.getModel().getDate())
                self.setDateType(date)
                self._dates[index] = date

    def addEventInCalendar(self, date, eic):
        if self._month is not None:
            if date in self._snapshot:
                index = self._snapshot.index(date)
                self._dates[index].addCalendarEvent(eic)

    def setDateType(self, date):
        current_type = date.getModel().getDateType(numeric=True)
        deduced_type = Date__Model.TYPE_WEEKDAY

        dt_date = date.getModel().getDate()
        dt_tuple = (dt_date.year, dt_date.month, dt_date.day)

        if calendar.weekday(*dt_tuple) in Calendar__Model.WEEKENDS:
            deduced_type = Date__Model.TYPE_WEEKEND
        if dt_date in self._holidays:
            deduced_type = Date__Model.TYPE_HOLYDAY
        if (dt_date.year, dt_date.month) != self._month:
            deduced_type = Date__Model.TYPE_GRAYDAY

        if current_type < deduced_type:
            current_type = deduced_type

        date.changeDateType(current_type)

    def _update(self):
        self._snapshot = self.generateSnapshot()
        self._dates = self.generateDefaultDates()

        # Add the required events
        events = self._master.getEvents()
        events_to_add = list()
        for event in events:
            if event.getModel().getInitDate().date() in self._snapshot:
                events_to_add.append(event)

        self._master.createEvents(events_to_add)

    def setMonth(self, month):
        self._month = month
        self._update()

    def getMonth(self):
        return self._month

    def monthSubtract(self):
        month = self._month
        if month[1] == 1:
            if month[0] == 1:
                return month
            else:
                return (month[0] - 1, 12)
        else:
            return (month[0], month[1] - 1)

    def monthAdd(self):
        month = self._month
        if month[1] == 12:
            if month[0] == 9999:
                return month
            else:
                return (month[0] + 1, 1)
        else:
            return (month[0], month[1] + 1)

    def setDataTree(self, datatree):
        self._datatree = datatree
        self._update()

    def getDataTree(self):
        return self._datatree

    def posInSnapshot(self, date):
        i = self._snapshot.index(date)
        return ceil((i + 1) / 7) - 1, (i) % 7

    def getHolderDimensions(self):
        return Calendar__Model.MAX_DIM_X, Calendar__Model.MAX_DIM_Y

    def getDates(self):
        return self._dates

    def getType(self):
        return self._type
