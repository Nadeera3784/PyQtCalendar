'''
    Simple class for widget visualization
'''
from PyQt5 import QtWidgets
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

    def getMainLayout(self):
        return self.main_layout

    def setupUI(self, window):
        window.setObjectName('MinimalHolder')
        window.resize(200, 200)  # w, h

        # Create a central widget to place calendar
        self.central_holder = QtWidgets.QWidget(window)
        self.central_holder.setObjectName('centralholder')

        self.main_layout = QtWidgets.QVBoxLayout()
        self.central_holder.setLayout(self.main_layout)

        window.setCentralWidget(self.central_holder)
