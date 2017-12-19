'''
    User input management for Calendar Widgets
'''
from PyQt5 import QtGui, QtCore


class Calendar__Controller:
    '''
        Controller for defining actions upon user interaction. The calendar itself
        allows the user 3 kinds of actions (as of yet):
         * snapshot switching
         * date selection
         * event creation
    '''

    def __init__(self, master):
        self._master = master

    def handleEvent(self, event):
        if isinstance(event, QtGui.QMouseEvent):
            if event.button() == QtCore.Qt.LeftButton:
                self.displaceCalendarSnapshot(-1)
            elif event.button() == QtCore.Qt.RightButton:
                self.displaceCalendarSnapshot(1)

    def displaceCalendarSnapshot(self, direction):
        if direction is -1:
            new_month = self._master.getModel().monthSubtract()
            self._master.getModel().setMonth(new_month)
        elif direction is 1:
            new_month = self._master.getModel().monthAdd()
            self._master.getModel().setMonth(new_month)
