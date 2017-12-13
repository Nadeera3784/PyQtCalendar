import models
import views


class Element:
    pass


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
        self._view


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
