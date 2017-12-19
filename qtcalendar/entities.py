import datetime as dt
import controllers
import models
import views


DEFAULT_DATATREE = {
    'str': {
        'days':
            [
                (0, 'Lunes'),
                (1, 'Martes'),
                (2, 'Miércoles'),
                (3, 'Jueves'),
                (4, 'Viernes'),
                (5, 'Sábado'),
                (6, 'Domingo'),
            ]
    }
}


class Element:
    pass


class Event:
    @staticmethod
    def createEventFromDescription(description):
        event = Event(
            description['place'],
            description['people'],
            description['init-date'],
            description['end-date'],
            description['fulfillment'])

        return event

    def __init__(self, name, people, init_date, end_date, fulfillment=0.0):

        place = models.Event__Model.Place(name=name, people=people)
        self._model = models.Event__Model(
            init_date, end_date, place, fulfillment)

        self._calendar_events = self.createCalendarEvents()

    def getModel(self):
        return self._model

    def getCalendarEvents(self):
        return self._calendar_events

    def getDateSpan(self):
        init_date = self.getModel().getInitDate()
        end_date = self.getModel().getEndDate()

        # Find the day span
        diff = end_date - init_date
        diff = diff.days

        # The days before are counted in intervals of 24 hours, if the situation occurs
        # that init_date.time() > end_date.time() but the difference is less than
        # 24 hours, we know we missed a day, this situation occurs when an event starts
        # at night and end early in the morning.
        time1 = dt.datetime.combine(dt.date.today(), init_date.time())
        time2 = dt.datetime.combine(dt.date.today(), end_date.time())

        difference = time1 - time2
        overflow = False
        if init_date.time() > end_date.time() and abs(difference.days) < 1:
            overflow = True
            diff += 1

        # Build the span array
        span = []
        for i in range(diff + 1):
            span.append(init_date.date() + dt.timedelta(i))

        return overflow, span

    def createCalendarEvents(self):
        overflow, span = self.getDateSpan()
        eics = list()

        for d in span:
            eics.append((d, EventInCalendar(self)))

        eics[-1] = (eics[-1][0], EventInCalendar(self, overflow=overflow))

        return eics


class EventInCalendar(Element):
    '''
        EventInCalendar interface intended for usage in Date class, or for subclassing.
        It contains model, view and controller of EventInCalendar:
        * model: holds the information of EventInCalendar (displayed or not)
        * view: visual classes and mechanisms
        * controller: user interaction
    '''

    def __init__(self, event, overflow=False):
        self._model = models.EventInCalendar__Model(self, overflow)
        self._view = views.EventInCalendar__View(self)

        self.setEvent(event)

    def getView(self):
        return self._view

    def getModel(self):
        return self._model

    def getEvent(self):
        return self._event

    def setEvent(self, event):
        self._event = event

        # Recursively set the event
        self._model.setEvent(event)
        self._view.updateFromModel()

    def __lt__(self, other):
        return self.getEvent().getModel().getInitDate() \
            < other.getEvent().getModel().getInitDate()


class Date(Element):
    '''
        Date class for the calendar. A calendar is basically a grid layout of multiple
        date objects organized in a particular manner.
        Date class holds the events that occur in a particular date and displays them
        one on top of the other, organized by init_time.
    '''

    def __init__(self, date, datatree=DEFAULT_DATATREE):
        self._model = models.Date__Model(self, date)
        self._view = views.Date__View(self)
        self._datatree = datatree

    def getView(self):
        return self._view

    def getModel(self):
        return self._model

    def getDataTree(self):
        return self._datatree

    def addCalendarEvent(self, eic):
        self._model.addEvent(eic)
        self._view.updateFromModel()

    def changeDate(self, new_date):
        '''
            Changes date of Date, this also resets the datetype to workdate, the inverse
            (by datetype) does not occur
        '''
        self._model.setDate(new_date)
        self._view.updateFromModel()

    def changeDateType(self, datetype):
        self._model.setDate(self._model.getDate(), datetype)
        self._view.updateFromModel()


class Calendar(Element):
    '''
        Calendar superclass, manages Dates and the overall language pack.
        To get the best behavour, you should expose this interface to the following
        information:
          * Holiday list: list of dates (datetime.date) of the holidays of your country
                          (an example to generate such a list is given in controllers.py)
          * Leading day of your calendar: by default leading day is sunday, use the
                                          variables Calendar__Model.TYPE_XX_LEADING to
                                          set up the leading day in a uniform manner.
          * Datatrees: the information the user is exposed to is given via a datatree,
                       we are not responsible by it, we only give you the datatree
                       format and the required keys.
    '''

    def __init__(
            self,
            holidays=list(),
            leading_day=models.Calendar__Model.TYPE_SUNDAY_LEADING,
            datatree=DEFAULT_DATATREE):

        # Save events for latter
        self._events = list()

        # Set the datatree
        self._datatree = datatree

        self._model = models.Calendar__Model(self, ctype=leading_day, holidays=holidays)
        self._view = views.Calendar__View(self)
        self._controller = controllers.Calendar__Controller(self)

        self._view.updateFromModel()

    def getView(self):
        return self._view.getContainer()

    def getDataTree(self):
        return self._datatree

    def getModel(self):
        return self._model

    def addDate(self, date):
        self._model.addDate(date)
        self._view.updateFromModel()

    def addEventInCalendar(self, d, eic):
        self._model.addEventInCalendar(d, eic)
        self._view.updateFromModel()

    def createDate(self, date):
        return Date(date, datatree=self._datatree)

    def getEvents(self):
        return self._events

    def createEvents(self, events):
        for event in events:
            for d, eic in event.getCalendarEvents():
                self.addEventInCalendar(d, eic)
        self._view.updateFromModel()

    def createEvent(self, description):
        '''
            Creates Event, EventInCalendar, Date and assigns the EventInCalendar to
            the Date. If the event spans more than one day, two Date objects are
            assigned the Event.
        '''

        # Create the event in calendar
        event = Event.createEventFromDescription(description)

        # An event may hold several calendar events if it spans across multiple dates
        for d, eic in event.getCalendarEvents():
            self.addEventInCalendar(d, eic)

        self._events.append(event)

    def delegate(self, e):
        self._controller.handleEvent(e)
