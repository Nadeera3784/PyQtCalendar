import models
import views


DEFAULT_DATATREE = dict()


class Element:
    pass


class Event:
    def __init__(self, init_date, end_date, fulfillment=0.0):
        self._model = models.Event__Model(
            init_date, end_date, models.Event__Model.Place(), fulfillment)

    def getModel(self):
        return self._model


class EventInCalendar(Element):
    '''
        EventInCalendar interface intended for usage in Date class, or for subclassing.
        It contains model, view and controller of EventInCalendar:
        * model: holds the information of EventInCalendar (displayed or not)
        * view: visual classes and mechanisms
        * controller: user interaction
    '''

    def __init__(self):
        self._model = models.EventInCalendar__Model(self)
        self._view = views.EventInCalendar__View(self)
        self._event = None

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

    def __init__(self, date):
        self._model = models.Date__Model(self, date)
        self._view = views.Date__View(self)

    def getView(self):
        return self._view

    def getModel(self):
        return self._model

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
        self._model = models.Calendar__Model(self, ctype=leading_day, holidays=holidays)
        self._view = views.Calendar__View(self)

        self._view.updateFromModel()

    def getView(self):
        return self._view.getContainer()

    def getModel(self):
        return self._model

    def addDate(self, date):
        self._model.addDate(date)
        self._view.updateFromModel()

    def createDate(self, date):
        return Date(date)
