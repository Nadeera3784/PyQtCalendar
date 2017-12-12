'''
    Views for calendar Widgets
'''

from PyQt5 import QtWidgets


class EventInCalendar(QtWidgets.QLabel):
    '''
        Event description that appears in a calendar cell. It has the following format:
         ----------------------
        | HH:mm - HH:mm  Place |
         ----------------------
        That is: init time, end time and the place where the event will hold. Label
        color can be adjusted via a fulfillment criteria that ranges from 0 to 1,
        colors are:
        dark red:    0.0 - 0.2
        red:         0.3 - 0.5
        dark yellow: 0.6 - 0.7
        yellow:      0.7 - 0.9
        green:       1.0
        The fulfillment criteria comes from the model function getFulFillmentStatus()
    '''

    def __init__(self):
        super(EventInCalendar, self).__init__()
        self.setText('Holi')
