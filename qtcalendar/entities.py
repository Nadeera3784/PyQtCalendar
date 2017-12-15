import models
import views


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
    '''

    def __init__(self):
        self._model = models.Calendar__Model(self)
        self._view = views.Calendar__View(self)

        self._view.updateFromModel()

    def getView(self):
        return self._view

    def getModel(self):
        return self._model

    def addDate(self, date):
        self._model.addDate(Date(date))
        self._view.updateFromModel()

    def createDate(self, date):
        return Date(date)
