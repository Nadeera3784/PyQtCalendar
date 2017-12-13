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
