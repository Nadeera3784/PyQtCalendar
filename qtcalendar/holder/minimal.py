'''
    Simple class for widget visualization
'''
from PyQt5 import QtWidgets, QtCore
import sys


class MinimalHolder:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.frame = QtWidgets.QMainWindow()

        self.setupUI(self.frame)

    def __call__(self):
        self.frame.show()
        sys.exit(self.app.exec_())
        self.frame.end()

    def setupUI(self, window):
        window.setObjectName('MinimalHolder')
        window.resize(876, 600)  # w, h

        # Create a central widget to place calendar
        self.central_holder = QtWidgets.QWidget(window)
        self.central_holder.setObjectName('centralholder')

        window.setCentralWidget(self.central_holder)

        # Apply translations
        self.retranslateUI(window)
        QtCore.QMetaObject.connectSlotsByName(window)

    def retranslateUI(self, window):
        _translate = QtCore.QCoreApplication.translate
        window.setWindowTitle(_translate('MinimalHolder', 'PyQtCalendar Test'))
