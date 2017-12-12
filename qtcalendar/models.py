'''
    Models for QtWidgets
'''
import datetime as dt


class EventInCalendar__Model:
    class Text:
        @staticmethod
        def getDefault():
            return EventInCalendar__Model.Text()

        def __init__(self):
            self.init_date = dt.datetime(1, 1, 1)
            self.end_date = dt.datetime(9999, 12, 31)
            self.place = Event__Model.Place()

        def __str__(self):
            init_time, end_time = self.init_date.time(), self.end_date.time()

            return '  '.join([str(i) for i in [end_time, init_time, self.place]])

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

    def __init__(self):
        self._fulfillment = 1.0

    def getFulFillmentStatus(self, numeric=False):
        if not numeric:
            return EventInCalendar__Model.colorOf(self._fulfillment)
        return self._fulfillment


class Event__Model:
    class Place:
        def __init__(self):
            self.name = 'NA'
            self.people = 0

        def __str__(self):
            return self.name
