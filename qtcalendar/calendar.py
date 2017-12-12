import models
import views


class EventInCalendar:
    def __init__(self):
        self._model = models.EventInCalendar__Model()
        self._view = views.EventInCalendar__View(self)

    def getView(self):
        return self._view

    def getModel(self):
        return self._model
