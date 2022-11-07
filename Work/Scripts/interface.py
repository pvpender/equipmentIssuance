from PyQt6.QtWidgets import QMainWindow, QLineEdit, QPushButton, QLabel
from PyQt6 import QtCore
from user_collections import *


class LogWindow(QMainWindow):
    loggedSignal = QtCore.pyqtSignal()

    def __init__(self, user_list: UserCollection):
        super(LogWindow, self).__init__()
        self.__main_window = MainWindow
        self.__user_list = user_list
        self.setFixedSize(720, 480)
        self.setWindowTitle("Log in")
        self.__label = QLabel(self)
        self.__label.setFixedWidth(300)
        self.__label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.__label.move((self.frameGeometry().width() - self.__label.width()) // 2,
                          (self.frameGeometry().height() - self.__label.height()) // 2 - 50)
        self.__label.setStyleSheet("color: red")
        self.__login_window = QLineEdit(self)
        self.__login_window.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.__login_window.setFixedWidth(200)
        self.__login_window.move((self.frameGeometry().width() - self.__login_window.width()) // 2,
                                 (self.frameGeometry().height() - self.__login_window.height()) // 2 -
                                 self.__login_window.height() // 2)
        self.__password_window = QLineEdit(self)
        self.__password_window.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.__password_window.setFixedWidth(200)
        self.__password_window.move((self.frameGeometry().width() - self.__login_window.width()) // 2,
                                    (self.frameGeometry().height() - self.__login_window.height()) // 2 +
                                    self.__login_window.height() // 2 + 10)
        self.__button = QPushButton(self)
        self.__button.setText("Вход")
        self.__button.move((self.frameGeometry().width() - self.__button.width()) // 2,
                           (self.frameGeometry().height() - self.__button.height()) // 2
                           + self.__login_window.height() * 2 + 10)
        self.__login_label = QLabel("Логин:", self)
        self.__login_label.move(
            (self.frameGeometry().width() - self.__login_window.width() - self.__login_label.width()) // 2,
            (self.frameGeometry().height() - self.__login_window.height()) // 2 -
            self.__login_window.height() // 2)
        self.__password_label = QLabel("Пароль:", self)
        self.__password_label.move(
            (self.frameGeometry().width() - self.__login_window.width() - self.__password_label.width()) // 2,
            (self.frameGeometry().height() - self.__login_window.height()) // 2 +
            self.__login_window.height() // 2 + 10)
        self.__button.clicked.connect(self.login)
        self.show()

    def login(self):
        user = self.__user_list.get_user_by_mail(self.__login_window.text())
        if user and user.password == self.__password_window.text():
            self.hide()
            self.__main_window = MainWindow(self.__user_list, user)
        else:
            self.__label.setText("Введены неверные данные!")
            self.__password_window.setText("")


class MainWindow(QMainWindow):

    def __init__(self, user_list: UserCollection, current_user):
        super(MainWindow, self).__init__()
        self.setWindowTitle("App")
        self.resize(1280, 720)
        self.__current_user = current_user
        self.__user_list = user_list
        self.show()
