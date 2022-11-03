from PyQt6.QtWidgets import QMainWindow, QLineEdit, QLabel
from PyQt6 import QtCore
from PyQt6 import QtGui


class LogWindow(QMainWindow):

    loggedSignal = QtCore.pyqtSignal()

    def __init__(self):
        super(LogWindow, self).__init__()
        self.setWindowTitle("Log in")
        self.__login_window = QLineEdit(self)
        self.__login_window.setFixedWidth(120)
        self.__login_window.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.__password_window = QLineEdit(self)
        self.__password_window.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.resize(720, 480)

    def login(self):
        pass


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("App")
        self.resize(1280, 720)
        self.__current_user = None
        self.__access_window = LogWindow()
        self.__access_window.loggedSignal.connect(self.showMaximized)
        self.__access_window.show()
