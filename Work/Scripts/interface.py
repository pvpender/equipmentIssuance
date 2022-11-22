from PyQt6.QtWidgets import QMainWindow, QLineEdit, QPushButton, QLabel, QFrame
from PyQt6 import QtCore, QtGui
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
        self.__login_field = QLineEdit(self)
        self.__login_field.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.__login_field.setFixedWidth(200)
        self.__login_field.move((self.frameGeometry().width() - self.__login_field.width()) // 2,
                                (self.frameGeometry().height() - self.__login_field.height()) // 2 -
                                self.__login_field.height() // 2)
        self.__password_field = QLineEdit(self)
        self.__password_field.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.__password_field.setFixedWidth(200)
        self.__password_field.move((self.frameGeometry().width() - self.__login_field.width()) // 2,
                                   (self.frameGeometry().height() - self.__login_field.height()) // 2 +
                                   self.__login_field.height() // 2 + 10)
        self.__button = QPushButton(self)
        self.__button.setText("Вход")
        self.__button.move((self.frameGeometry().width() - self.__button.width()) // 2,
                           (self.frameGeometry().height() - self.__button.height()) // 2
                           + self.__login_field.height() * 2 + 10)
        self.__login_label = QLabel("Логин:", self)
        self.__login_label.move(
            (self.frameGeometry().width() - self.__login_field.width() - self.__login_label.width()) // 2,
            (self.frameGeometry().height() - self.__login_field.height()) // 2 -
            self.__login_field.height() // 2)
        self.__password_label = QLabel("Пароль:", self)
        self.__password_label.move(
            (self.frameGeometry().width() - self.__login_field.width() - self.__password_label.width()) // 2,
            (self.frameGeometry().height() - self.__login_field.height()) // 2 +
            self.__login_field.height() // 2 + 10)
        self.__password_field.returnPressed.connect(self.__button.click)
        self.__button.clicked.connect(self.login)
        self.__button.setAutoDefault(True)
        self.show()

    def login(self):
        user = self.__user_list.get_user_by_mail(self.__login_field.text())
        if user and user.password == self.__password_field.text():
            self.hide()
            self.__main_window = MainWindow(self.__user_list, user)
        else:
            self.__label.setText("Введены неверные данные!")
            self.__password_field.setText("")


class MainWindow(QMainWindow):

    def __init__(self, user_list: UserCollection, current_user):
        super(MainWindow, self).__init__()
        self.setWindowTitle("App")
        self.setFixedSize(1280, 720)
        self.setStyleSheet("background-color:#F0F8FF;")
        self.__current_user = current_user
        self.__user_list = user_list
        self.__sidePanel = QFrame(self)
        self.__sidePanel.setFixedSize(200, 720)
        self.__sidePanel.setStyleSheet("background-color:#FFFFFF;")
        self.__button = QPushButton(self.__sidePanel)
        self.__button.setFixedSize(180, 30)
        self.__button.setText("Test")
        self.__button.setStyleSheet("QPushButton { border-radius: 10; border : 1px solid white; color: #808080;}"
                                    "QPushButton:hover { background-color: #000000; color: white;} ")
        self.show()
