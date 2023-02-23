from PyQt6.QtWidgets import QMainWindow, QLineEdit, QPushButton, QLabel, QFrame, QMessageBox, QHeaderView
from PyQt6.QtCore import Qt
from PyQt6 import QtCore, QtGui, QtWidgets

from Work.Scripts.interface import TableModel
from user_collections import *
from equipment import *
from database import *
from accesses import *
from users import *
from accesses import *
import pandas as pd


class LogWindow(QMainWindow):
    loggedSignal = QtCore.pyqtSignal()

    def __init__(self, user_list: UserCollection, db: DataBase):
        super(LogWindow, self).__init__()
        self.__main_window = MainWindow
        self.__db = db
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
        self.__password_field.setEchoMode(QLineEdit.EchoMode.Password)
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
        if isinstance(user, Admin) and user.password == self.__password_field.text():
            self.hide()
            self.__main_window = MainWindow(self.__user_list, user, self.__db, user.access)
        else:
            self.__label.setText("Введены неверные данные!")
            self.__password_field.setText("")


def show_message(title: str, info: str):
    msg_box = QMessageBox()
    msg_box.setText(info)
    msg_box.setWindowTitle(title)
    msg_box.exec()


class MainWindow(QMainWindow):
    def __init__(self, user_list: UserCollection, current_user, db: DataBase, admin_access: AdminAccess):
        super(MainWindow, self).__init__()
        self.setWindowTitle("App")
        self.setFixedSize(1550, 1000)
        self.setStyleSheet("background-color:#F0F8FF;")
        self.__current_user = current_user
        self.__user_list = user_list
        self.__db = db
        self.__eqTableContents = []
        self.__usTableContents = []
        self.__reqTableContents = []
        self.__admin_access = admin_access  # Права админа, зашедшего в приложение
        self.__reqs = self.__db.get_unsolved_requests()
        self.__reqnum = 0
        # self.__sidePanel = QFrame(self)
        # self.__sidePanel.setFixedSize(200, 720)
        # self.__sidePanel.setStyleSheet("background-color:#FFFFFF;")
        # self.__button = QPushButton(self.__sidePanel)
        # self.__button.setFixedSize(180, 30)
        # self.__button.setText("Test")
        # self.__button.setStyleSheet("QPushButton { border-radius: 10; border : 1px solid white; color: #808080;}"
        #                            "QPushButton:hover { background-color: #000000; color: white;} ")
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(parent=self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1411, 821))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.addSmthBox = QtWidgets.QGroupBox(parent=self.tab)
        self.addSmthBox.setGeometry(QtCore.QRect(10, 10, 461, 521))
        self.addSmthBox.setObjectName("addSmthBox")
        self.label_4 = QtWidgets.QLabel(parent=self.addSmthBox)
        self.label_4.setGeometry(QtCore.QRect(10, 30, 61, 21))
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.nameOrEmailLabel_2 = QtWidgets.QLabel(parent=self.addSmthBox)
        self.nameOrEmailLabel_2.setGeometry(QtCore.QRect(10, 30, 61, 16))
        self.nameOrEmailLabel_2.setObjectName("nameOrEmailLabel_2")
        self.eqNameOrEmailLineEdit = QtWidgets.QLineEdit(parent=self.addSmthBox)
        self.eqNameOrEmailLineEdit.setGeometry(QtCore.QRect(70, 30, 311, 22))
        self.eqNameOrEmailLineEdit.setObjectName("eqNameOrEmailLineEdit")
        self.rightsLabel_3 = QtWidgets.QLabel(parent=self.addSmthBox)
        self.rightsLabel_3.setGeometry(QtCore.QRect(60, 100, 151, 16))
        self.rightsLabel_3.setObjectName("rightsLabel_3")
        self.verticalLayoutWidget_5 = QtWidgets.QWidget(parent=self.addSmthBox)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(230, 90, 197, 126))
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.eqfirstRightsCheckBox = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget_5)
        self.eqfirstRightsCheckBox.setObjectName("eqfirstRightsCheckBox")
        self.verticalLayout_3.addWidget(self.eqfirstRightsCheckBox)
        self.eqsecondRightsCheckBox = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget_5)
        self.eqsecondRightsCheckBox.setObjectName("eqsecondRightsCheckBox")
        self.verticalLayout_3.addWidget(self.eqsecondRightsCheckBox)
        self.eqthirdRightsCheckBox = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget_5)
        self.eqthirdRightsCheckBox.setObjectName("eqthirdRightsCheckBox")
        self.verticalLayout_3.addWidget(self.eqthirdRightsCheckBox)
        self.eqfourthRightsCheckBox = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget_5)
        self.eqfourthRightsCheckBox.setObjectName("eqfourthRightsCheckBox")
        self.verticalLayout_3.addWidget(self.eqfourthRightsCheckBox)
        self.label_5 = QtWidgets.QLabel(parent=self.addSmthBox)
        self.label_5.setGeometry(QtCore.QRect(10, 60, 171, 16))
        self.label_5.setObjectName("label_5")
        self.eqIdCardLineEdit = QtWidgets.QLineEdit(parent=self.addSmthBox)
        self.eqIdCardLineEdit.setGeometry(QtCore.QRect(170, 60, 211, 22))
        self.eqIdCardLineEdit.setObjectName("eqIdCardLineEdit")
        self.inventoryWidgetsGroupBox = QtWidgets.QGroupBox(parent=self.addSmthBox)
        self.inventoryWidgetsGroupBox.setGeometry(QtCore.QRect(20, 220, 421, 191))
        self.inventoryWidgetsGroupBox.setTitle("")
        self.inventoryWidgetsGroupBox.setObjectName("inventoryWidgetsGroupBox")
        self.label_10 = QtWidgets.QLabel(parent=self.inventoryWidgetsGroupBox)
        self.label_10.setGeometry(QtCore.QRect(10, 40, 201, 16))
        self.label_10.setObjectName("label_10")
        self.descriptionTextEdit = QtWidgets.QTextEdit(parent=self.inventoryWidgetsGroupBox)
        self.descriptionTextEdit.setGeometry(QtCore.QRect(70, 70, 321, 51))
        self.descriptionTextEdit.setObjectName("descriptionTextEdit")
        self.ableNowSpinBox = QtWidgets.QSpinBox(parent=self.inventoryWidgetsGroupBox)
        self.ableNowSpinBox.setGeometry(QtCore.QRect(240, 10, 151, 22))
        self.ableNowSpinBox.setObjectName("ableNowSpinBox")
        self.label_11 = QtWidgets.QLabel(parent=self.inventoryWidgetsGroupBox)
        self.label_11.setGeometry(QtCore.QRect(50, 10, 141, 16))
        self.label_11.setObjectName("label_11")
        self.reservedSpinBox = QtWidgets.QSpinBox(parent=self.inventoryWidgetsGroupBox)
        self.reservedSpinBox.setGeometry(QtCore.QRect(240, 40, 151, 22))
        self.reservedSpinBox.setObjectName("reservedSpinBox")
        self.label_12 = QtWidgets.QLabel(parent=self.inventoryWidgetsGroupBox)
        self.label_12.setGeometry(QtCore.QRect(10, 70, 61, 16))
        self.label_12.setObjectName("label_12")
        self.label_26 = QtWidgets.QLabel(parent=self.inventoryWidgetsGroupBox)
        self.label_26.setGeometry(QtCore.QRect(10, 160, 101, 16))
        self.label_26.setObjectName("label_26")
        self.label_27 = QtWidgets.QLabel(parent=self.inventoryWidgetsGroupBox)
        self.label_27.setGeometry(QtCore.QRect(180, 160, 141, 16))
        self.label_27.setObjectName("label_27")
        self.heightSpinBox = QtWidgets.QSpinBox(parent=self.inventoryWidgetsGroupBox)
        self.heightSpinBox.setGeometry(QtCore.QRect(110, 160, 61, 22))
        self.heightSpinBox.setObjectName("heightSpinBox")
        self.posFromLeftSpinBox = QtWidgets.QSpinBox(parent=self.inventoryWidgetsGroupBox)
        self.posFromLeftSpinBox.setGeometry(QtCore.QRect(300, 160, 71, 22))
        self.posFromLeftSpinBox.setObjectName("posFromLeftSpinBox")
        self.radioButton_setPos = QtWidgets.QRadioButton(parent=self.inventoryWidgetsGroupBox)
        self.radioButton_setPos.setGeometry(QtCore.QRect(100, 130, 221, 20))
        self.radioButton_setPos.setObjectName("radioButton_setPos")
        self.eqaddUserOrInvButton = QtWidgets.QPushButton(parent=self.addSmthBox)
        self.eqaddUserOrInvButton.setGeometry(QtCore.QRect(20, 410, 401, 41))
        self.eqaddUserOrInvButton.setObjectName("eqaddUserOrInvButton")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.addSmthBox_2 = QtWidgets.QGroupBox(parent=self.tab_2)
        self.addSmthBox_2.setGeometry(QtCore.QRect(20, 10, 581, 541))
        self.addSmthBox_2.setObjectName("addSmthBox_2")
        self.label_6 = QtWidgets.QLabel(parent=self.addSmthBox_2)
        self.label_6.setGeometry(QtCore.QRect(10, 30, 61, 21))
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        self.nameOrEmailLabel_3 = QtWidgets.QLabel(parent=self.addSmthBox_2)
        self.nameOrEmailLabel_3.setGeometry(QtCore.QRect(10, 30, 61, 16))
        self.nameOrEmailLabel_3.setObjectName("nameOrEmailLabel_3")
        self.usnameOrEmailLineEdit = QtWidgets.QLineEdit(parent=self.addSmthBox_2)
        self.usnameOrEmailLineEdit.setGeometry(QtCore.QRect(80, 30, 311, 22))
        self.usnameOrEmailLineEdit.setObjectName("usnameOrEmailLineEdit")
        self.rightsLabel_5 = QtWidgets.QLabel(parent=self.addSmthBox_2)
        self.rightsLabel_5.setGeometry(QtCore.QRect(60, 100, 151, 16))
        self.rightsLabel_5.setObjectName("rightsLabel_5")
        self.verticalLayoutWidget_7 = QtWidgets.QWidget(parent=self.addSmthBox_2)
        self.verticalLayoutWidget_7.setGeometry(QtCore.QRect(230, 90, 171, 126))
        self.verticalLayoutWidget_7.setObjectName("verticalLayoutWidget_7")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_7)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.usfirstRightsCheckBox = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget_7)
        self.usfirstRightsCheckBox.setObjectName("usfirstRightsCheckBox")
        self.verticalLayout_5.addWidget(self.usfirstRightsCheckBox)
        self.ussecondRightsCheckBox = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget_7)
        self.ussecondRightsCheckBox.setObjectName("ussecondRightsCheckBox")
        self.verticalLayout_5.addWidget(self.ussecondRightsCheckBox)
        self.usthirdRightsCheckBox = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget_7)
        self.usthirdRightsCheckBox.setObjectName("usthirdRightsCheckBox")
        self.verticalLayout_5.addWidget(self.usthirdRightsCheckBox)
        self.usfourthRightsCheckBox = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget_7)
        self.usfourthRightsCheckBox.setObjectName("usfourthRightsCheckBox")
        self.verticalLayout_5.addWidget(self.usfourthRightsCheckBox)
        self.label_9 = QtWidgets.QLabel(parent=self.addSmthBox_2)
        self.label_9.setGeometry(QtCore.QRect(10, 60, 171, 16))
        self.label_9.setObjectName("label_9")
        self.usIdCardLineEdit = QtWidgets.QLineEdit(parent=self.addSmthBox_2)
        self.usIdCardLineEdit.setGeometry(QtCore.QRect(180, 60, 211, 22))
        self.usIdCardLineEdit.setObjectName("usIdCardLineEdit")
        self.addHuman_groupBox_2 = QtWidgets.QGroupBox(parent=self.addSmthBox_2)
        self.addHuman_groupBox_2.setGeometry(QtCore.QRect(10, 220, 411, 201))
        self.addHuman_groupBox_2.setTitle("")
        self.addHuman_groupBox_2.setObjectName("addHuman_groupBox_2")
        self.usradioButton_User = QtWidgets.QRadioButton(parent=self.addHuman_groupBox_2)
        self.usradioButton_User.setGeometry(QtCore.QRect(270, 20, 111, 20))
        self.usradioButton_User.setObjectName("usradioButton_User")
        self.usradioButton_Admin = QtWidgets.QRadioButton(parent=self.addHuman_groupBox_2)
        self.usradioButton_Admin.setGeometry(QtCore.QRect(270, 0, 121, 20))
        self.usradioButton_Admin.setObjectName("usradioButton_Admin")
        self.adminRightsGroupBox_2 = QtWidgets.QGroupBox(parent=self.addHuman_groupBox_2)
        self.adminRightsGroupBox_2.setGeometry(QtCore.QRect(0, 40, 411, 211))
        self.adminRightsGroupBox_2.setTitle("")
        self.adminRightsGroupBox_2.setObjectName("adminRightsGroupBox_2")
        self.verticalLayoutWidget_6 = QtWidgets.QWidget(parent=self.adminRightsGroupBox_2)
        self.verticalLayoutWidget_6.setGeometry(QtCore.QRect(100, 10, 354, 151))
        self.verticalLayoutWidget_6.setObjectName("verticalLayoutWidget_6")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_6)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.usadminRightsCheckBox = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget_6)
        self.usadminRightsCheckBox.setObjectName("usadminRightsCheckBox")
        self.verticalLayout_4.addWidget(self.usadminRightsCheckBox)
        self.usadmin2RightsCheckBox = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget_6)
        self.usadmin2RightsCheckBox.setObjectName("usadmin2RightsCheckBox")
        self.verticalLayout_4.addWidget(self.usadmin2RightsCheckBox)
        self.usadmin3RightsCheckBox = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget_6)
        self.usadmin3RightsCheckBox.setObjectName("usadmin3RightsCheckBox")
        self.verticalLayout_4.addWidget(self.usadmin3RightsCheckBox)
        self.usadmin4RightsCheckBox = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget_6)
        self.usadmin4RightsCheckBox.setObjectName("usadmin4RightsCheckBox")
        self.verticalLayout_4.addWidget(self.usadmin4RightsCheckBox)
        self.usadmin5RightsCheckBox = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget_6)
        self.usadmin5RightsCheckBox.setObjectName("usadmin5RightsCheckBox")
        self.verticalLayout_4.addWidget(self.usadmin5RightsCheckBox)
        self.rightsLabel_4 = QtWidgets.QLabel(parent=self.adminRightsGroupBox_2)
        self.rightsLabel_4.setGeometry(QtCore.QRect(20, 0, 81, 16))
        self.rightsLabel_4.setObjectName("rightsLabel_4")
        self.usaddUserOrInvButton = QtWidgets.QPushButton(parent=self.addSmthBox_2)
        self.usaddUserOrInvButton.setGeometry(QtCore.QRect(50, 440, 401, 41))
        self.usaddUserOrInvButton.setObjectName("usaddUserOrInvButton")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.viewInvOrUserBox = QtWidgets.QGroupBox(parent=self.tab_3)
        self.viewInvOrUserBox.setGeometry(QtCore.QRect(10, 10, 1151, 761))
        self.viewInvOrUserBox.setObjectName("viewInvOrUserBox")
        self.eqsearchByIdLabel = QtWidgets.QLabel(parent=self.viewInvOrUserBox)
        self.eqsearchByIdLabel.setGeometry(QtCore.QRect(10, 30, 21, 16))
        self.eqsearchByIdLabel.setObjectName("eqsearchByIdLabel")
        self.searchByEmailOrNameLabel = QtWidgets.QLabel(parent=self.viewInvOrUserBox)
        self.searchByEmailOrNameLabel.setGeometry(QtCore.QRect(10, 60, 51, 16))
        self.searchByEmailOrNameLabel.setObjectName("searchByEmailOrNameLabel")
        self.eqsearchByIdSpinBox = QtWidgets.QSpinBox(parent=self.viewInvOrUserBox)
        self.eqsearchByIdSpinBox.setGeometry(QtCore.QRect(30, 30, 161, 22))
        self.eqsearchByIdSpinBox.setObjectName("eqsearchByIdSpinBox")
        self.eqsearchByEmailOrNameLineEdit = QtWidgets.QLineEdit(parent=self.viewInvOrUserBox)
        self.eqsearchByEmailOrNameLineEdit.setGeometry(QtCore.QRect(60, 60, 191, 22))
        self.eqsearchByEmailOrNameLineEdit.setObjectName("eqsearchByEmailOrNameLineEdit")
        self.listLabel = QtWidgets.QLabel(parent=self.viewInvOrUserBox)
        self.listLabel.setGeometry(QtCore.QRect(450, 10, 111, 16))
        self.listLabel.setObjectName("listLabel")
        self.verticalLayoutWidget_13 = QtWidgets.QWidget(parent=self.viewInvOrUserBox)
        self.verticalLayoutWidget_13.setGeometry(QtCore.QRect(130, 90, 197, 119))
        self.verticalLayoutWidget_13.setObjectName("verticalLayoutWidget_13")
        self.searchByRightsVerticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_13)
        self.searchByRightsVerticalLayout.setContentsMargins(0, 0, 0, 0)
        self.searchByRightsVerticalLayout.setObjectName("searchByRightsVerticalLayout")
        self.eqsearchByFirstRightsCheckBox = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget_13)
        self.eqsearchByFirstRightsCheckBox.setObjectName("eqsearchByFirstRightsCheckBox")
        self.searchByRightsVerticalLayout.addWidget(self.eqsearchByFirstRightsCheckBox)
        self.eqsearchBySecondRightsCheckBox = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget_13)
        self.eqsearchBySecondRightsCheckBox.setObjectName("eqsearchBySecondRightsCheckBox")
        self.searchByRightsVerticalLayout.addWidget(self.eqsearchBySecondRightsCheckBox)
        self.eqsearchByThirdRightsCheckBox = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget_13)
        self.eqsearchByThirdRightsCheckBox.setObjectName("eqsearchByThirdRightsCheckBox")
        self.searchByRightsVerticalLayout.addWidget(self.eqsearchByThirdRightsCheckBox)
        self.eqsearchByFourthRightsCheckBox = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget_13)
        self.eqsearchByFourthRightsCheckBox.setObjectName("eqsearchByFourthRightsCheckBox")
        self.searchByRightsVerticalLayout.addWidget(self.eqsearchByFourthRightsCheckBox)
        self.SearchByRightsLabel = QtWidgets.QLabel(parent=self.viewInvOrUserBox)
        self.SearchByRightsLabel.setGeometry(QtCore.QRect(10, 90, 121, 20))
        self.SearchByRightsLabel.setObjectName("SearchByRightsLabel")
        self.searchByPosGroupBox = QtWidgets.QGroupBox(parent=self.viewInvOrUserBox)
        self.searchByPosGroupBox.setGeometry(QtCore.QRect(10, 210, 441, 61))
        self.searchByPosGroupBox.setObjectName("searchByPosGroupBox")
        self.label_36 = QtWidgets.QLabel(parent=self.searchByPosGroupBox)
        self.label_36.setGeometry(QtCore.QRect(20, 30, 101, 16))
        self.label_36.setObjectName("label_36")
        self.label_37 = QtWidgets.QLabel(parent=self.searchByPosGroupBox)
        self.label_37.setGeometry(QtCore.QRect(210, 30, 161, 16))
        self.label_37.setObjectName("label_37")
        self.searchByHeightSpinBox = QtWidgets.QSpinBox(parent=self.searchByPosGroupBox)
        self.searchByHeightSpinBox.setGeometry(QtCore.QRect(140, 30, 61, 22))
        self.searchByHeightSpinBox.setObjectName("searchByHeightSpinBox")
        self.searchByPosFromLeftSpinBox = QtWidgets.QSpinBox(parent=self.searchByPosGroupBox)
        self.searchByPosFromLeftSpinBox.setGeometry(QtCore.QRect(330, 30, 71, 22))
        self.searchByPosFromLeftSpinBox.setObjectName("searchByPosFromLeftSpinBox")
        self.eqsearchPushButton = QtWidgets.QPushButton(parent=self.viewInvOrUserBox)
        self.eqsearchPushButton.setGeometry(QtCore.QRect(20, 280, 351, 28))
        self.eqsearchPushButton.setObjectName("eqsearchPushButton")
        self.eqTableView = QtWidgets.QTableView(parent=self.viewInvOrUserBox)
        self.eqTableView.setGeometry(QtCore.QRect(450, 30, 701, 721))
        self.eqTableView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.eqTableView.setObjectName("eqTableView")
        self.eqViewRefreshPushButton = QtWidgets.QPushButton(parent=self.viewInvOrUserBox)
        self.eqViewRefreshPushButton.setGeometry(QtCore.QRect(20, 320, 351, 28))
        self.eqViewRefreshPushButton.setObjectName("eqViewRefreshPushButton")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.viewInvOrUserBox_2 = QtWidgets.QGroupBox(parent=self.tab_4)
        self.viewInvOrUserBox_2.setGeometry(QtCore.QRect(10, 10, 1151, 761))
        self.viewInvOrUserBox_2.setObjectName("viewInvOrUserBox_2")
        self.searchByIdLabel_2 = QtWidgets.QLabel(parent=self.viewInvOrUserBox_2)
        self.searchByIdLabel_2.setGeometry(QtCore.QRect(10, 30, 101, 16))
        self.searchByIdLabel_2.setObjectName("searchByIdLabel_2")
        self.searchByEmailOrNameLabel_2 = QtWidgets.QLabel(parent=self.viewInvOrUserBox_2)
        self.searchByEmailOrNameLabel_2.setGeometry(QtCore.QRect(10, 60, 71, 16))
        self.searchByEmailOrNameLabel_2.setObjectName("searchByEmailOrNameLabel_2")
        self.ussearchByEmailOrNameLineEdit = QtWidgets.QLineEdit(parent=self.viewInvOrUserBox_2)
        self.ussearchByEmailOrNameLineEdit.setGeometry(QtCore.QRect(40, 60, 161, 22))
        self.ussearchByEmailOrNameLineEdit.setObjectName("ussearchByEmailOrNameLineEdit")
        self.listLabel_2 = QtWidgets.QLabel(parent=self.viewInvOrUserBox_2)
        self.listLabel_2.setGeometry(QtCore.QRect(450, 10, 111, 16))
        self.listLabel_2.setObjectName("listLabel_2")
        self.verticalLayoutWidget_14 = QtWidgets.QWidget(parent=self.viewInvOrUserBox_2)
        self.verticalLayoutWidget_14.setGeometry(QtCore.QRect(130, 90, 197, 119))
        self.verticalLayoutWidget_14.setObjectName("verticalLayoutWidget_14")
        self.ussearchByRightsVerticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_14)
        self.ussearchByRightsVerticalLayout.setContentsMargins(0, 0, 0, 0)
        self.ussearchByRightsVerticalLayout.setObjectName("ussearchByRightsVerticalLayout")
        self.ussearchByFirstRightsCheckBox = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget_14)
        self.ussearchByFirstRightsCheckBox.setObjectName("ussearchByFirstRightsCheckBox")
        self.ussearchByRightsVerticalLayout.addWidget(self.ussearchByFirstRightsCheckBox)
        self.ussearchBySecondRightsCheckBox = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget_14)
        self.ussearchBySecondRightsCheckBox.setObjectName("ussearchBySecondRightsCheckBox")
        self.ussearchByRightsVerticalLayout.addWidget(self.ussearchBySecondRightsCheckBox)
        self.ussearchByThirdRightsCheckBox = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget_14)
        self.ussearchByThirdRightsCheckBox.setObjectName("ussearchByThirdRightsCheckBox")
        self.ussearchByRightsVerticalLayout.addWidget(self.ussearchByThirdRightsCheckBox)
        self.ussearchByFourthRightsCheckBox = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget_14)
        self.ussearchByFourthRightsCheckBox.setObjectName("ussearchByFourthRightsCheckBox")
        self.ussearchByRightsVerticalLayout.addWidget(self.ussearchByFourthRightsCheckBox)
        self.SearchByRightsLabel_2 = QtWidgets.QLabel(parent=self.viewInvOrUserBox_2)
        self.SearchByRightsLabel_2.setGeometry(QtCore.QRect(10, 90, 121, 20))
        self.SearchByRightsLabel_2.setObjectName("SearchByRightsLabel_2")
        self.usTableView = QtWidgets.QTableView(parent=self.viewInvOrUserBox_2)
        self.usTableView.setGeometry(QtCore.QRect(450, 30, 701, 721))
        self.usTableView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.usTableView.setObjectName("usTableView")
        self.ussearchByNameOrEmailLineEdit = QtWidgets.QLineEdit(parent=self.viewInvOrUserBox_2)
        self.ussearchByNameOrEmailLineEdit.setGeometry(QtCore.QRect(110, 30, 311, 22))
        self.ussearchByNameOrEmailLineEdit.setObjectName("ussearchByNameOrEmailLineEdit")
        self.ussearchPushButton = QtWidgets.QPushButton(parent=self.viewInvOrUserBox_2)
        self.ussearchPushButton.setGeometry(QtCore.QRect(20, 220, 351, 28))
        self.ussearchPushButton.setObjectName("ussearchPushButton")
        self.usViewRefreshPushButton = QtWidgets.QPushButton(parent=self.viewInvOrUserBox_2)
        self.usViewRefreshPushButton.setGeometry(QtCore.QRect(20, 250, 351, 28))
        self.usViewRefreshPushButton.setObjectName("usViewRefreshPushButton")
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.RequestsGroupBox = QtWidgets.QGroupBox(parent=self.tab_5)
        self.RequestsGroupBox.setGeometry(QtCore.QRect(0, 0, 1401, 621))
        self.RequestsGroupBox.setObjectName("RequestsGroupBox")
        self.textBrowser = QtWidgets.QTextBrowser(parent=self.RequestsGroupBox)
        self.textBrowser.setGeometry(QtCore.QRect(20, 50, 511, 141))
        self.textBrowser.setObjectName("textBrowser")
        self.AcceptReqPushButton = QtWidgets.QPushButton(parent=self.RequestsGroupBox)
        self.AcceptReqPushButton.setGeometry(QtCore.QRect(20, 190, 181, 28))
        self.AcceptReqPushButton.setObjectName("AcceptReqPushButton")
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.RequestsGroupBox)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 220, 181, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_2 = QtWidgets.QLabel(parent=self.RequestsGroupBox)
        self.label_2.setGeometry(QtCore.QRect(20, 30, 201, 16))
        self.label_2.setObjectName("label_2")
        self.label_7 = QtWidgets.QLabel(parent=self.RequestsGroupBox)
        self.label_7.setGeometry(QtCore.QRect(690, 30, 331, 16))
        self.label_7.setObjectName("label_7")
        self.pushButton = QtWidgets.QPushButton(parent=self.RequestsGroupBox)
        self.pushButton.setGeometry(QtCore.QRect(550, 50, 101, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_3 = QtWidgets.QPushButton(parent=self.RequestsGroupBox)
        self.pushButton_3.setGeometry(QtCore.QRect(550, 80, 101, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        self.label_8 = QtWidgets.QLabel(parent=self.RequestsGroupBox)
        self.label_8.setGeometry(QtCore.QRect(540, 110, 131, 16))
        self.label_8.setObjectName("label_8")
        self.tableView2 = QtWidgets.QTableView(parent=self.RequestsGroupBox)
        self.tableView2.setGeometry(QtCore.QRect(670, 50, 711, 551))
        self.tableView2.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.tableView2.setObjectName("tableView2")
        self.reqViewRefreshPushButton = QtWidgets.QPushButton(parent=self.RequestsGroupBox)
        self.reqViewRefreshPushButton.setGeometry(QtCore.QRect(150, 580, 351, 28))
        self.reqViewRefreshPushButton.setObjectName("reqViewRefreshPushButton")
        self.reqsearchPushButton = QtWidgets.QPushButton(parent=self.RequestsGroupBox)
        self.reqsearchPushButton.setGeometry(QtCore.QRect(150, 540, 351, 28))
        self.reqsearchPushButton.setObjectName("reqsearchPushButton")
        self.reqsearchByWhat = QtWidgets.QLineEdit(parent=self.RequestsGroupBox)
        self.reqsearchByWhat.setGeometry(QtCore.QRect(90, 380, 381, 22))
        self.reqsearchByWhat.setObjectName("reqsearchByWhat")
        self.reqsearchByEmail = QtWidgets.QLineEdit(parent=self.RequestsGroupBox)
        self.reqsearchByEmail.setGeometry(QtCore.QRect(160, 320, 311, 22))
        self.reqsearchByEmail.setObjectName("reqsearchByEmail")
        self.searchByIdLabel_4 = QtWidgets.QLabel(parent=self.RequestsGroupBox)
        self.searchByIdLabel_4.setGeometry(QtCore.QRect(40, 380, 101, 16))
        self.searchByIdLabel_4.setObjectName("searchByIdLabel_4")
        self.searchByEmailOrNameLabel_5 = QtWidgets.QLabel(parent=self.RequestsGroupBox)
        self.searchByEmailOrNameLabel_5.setGeometry(QtCore.QRect(40, 320, 101, 16))
        self.searchByEmailOrNameLabel_5.setObjectName("searchByEmailOrNameLabel_5")
        self.reqsearchByUsId = QtWidgets.QLineEdit(parent=self.RequestsGroupBox)
        self.reqsearchByUsId.setGeometry(QtCore.QRect(160, 350, 311, 22))
        self.reqsearchByUsId.setObjectName("reqsearchByUsId")
        self.reqsearchByPurpose = QtWidgets.QLineEdit(parent=self.RequestsGroupBox)
        self.reqsearchByPurpose.setGeometry(QtCore.QRect(90, 410, 381, 22))
        self.reqsearchByPurpose.setObjectName("reqsearchByPurpose")
        self.searchByIdLabel_5 = QtWidgets.QLabel(parent=self.RequestsGroupBox)
        self.searchByIdLabel_5.setGeometry(QtCore.QRect(40, 350, 91, 16))
        self.searchByIdLabel_5.setObjectName("searchByIdLabel_5")
        self.searchByEmailOrNameLabel_6 = QtWidgets.QLabel(parent=self.RequestsGroupBox)
        self.searchByEmailOrNameLabel_6.setGeometry(QtCore.QRect(40, 410, 31, 16))
        self.searchByEmailOrNameLabel_6.setObjectName("searchByEmailOrNameLabel_6")
        self.searchByIdLabel_6 = QtWidgets.QLabel(parent=self.RequestsGroupBox)
        self.searchByIdLabel_6.setGeometry(QtCore.QRect(40, 440, 71, 16))
        self.searchByIdLabel_6.setObjectName("searchByIdLabel_6")
        self.searchByEmailOrNameLabel_7 = QtWidgets.QLabel(parent=self.RequestsGroupBox)
        self.searchByEmailOrNameLabel_7.setGeometry(QtCore.QRect(40, 470, 91, 16))
        self.searchByEmailOrNameLabel_7.setObjectName("searchByEmailOrNameLabel_7")
        self.reqsearchByEqId = QtWidgets.QSpinBox(parent=self.RequestsGroupBox)
        self.reqsearchByEqId.setGeometry(QtCore.QRect(150, 470, 81, 22))
        self.reqsearchByEqId.setObjectName("reqsearchByEqId")
        self.reqsearchByCount = QtWidgets.QSpinBox(parent=self.RequestsGroupBox)
        self.reqsearchByCount.setGeometry(QtCore.QRect(150, 440, 81, 22))
        self.reqsearchByCount.setObjectName("reqsearchByCount")
        self.tabWidget.addTab(self.tab_5, "")
        self.setCentralWidget(self.centralwidget)

        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)
        _translate = QtCore.QCoreApplication.translate
        #   MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        #   self.burgerButton.setText(_translate("MainWindow", "Меню"))
        self.addSmthBox.setTitle(_translate("MainWindow", "Добавление инвентаря"))
        self.nameOrEmailLabel_2.setText(_translate("MainWindow", "Название"))
        self.rightsLabel_3.setText(_translate("MainWindow", "Кто может получить "))
        self.eqfirstRightsCheckBox.setText(_translate("MainWindow", "Обычный пользователь"))
        self.eqsecondRightsCheckBox.setText(_translate("MainWindow", "Редактор-модератор"))
        self.eqthirdRightsCheckBox.setText(_translate("MainWindow", "Инженер"))
        self.eqfourthRightsCheckBox.setText(_translate("MainWindow", "Главный инженер"))
        self.label_5.setText(_translate("MainWindow", "Идентификационный номер"))
        self.label_10.setText(_translate("MainWindow", "Зарезервированное  количество"))
        self.label_11.setText(_translate("MainWindow", "Доступное количество"))
        self.label_12.setText(_translate("MainWindow", "Описание"))
        self.label_26.setText(_translate("MainWindow", "Высота(от пола)"))
        self.label_27.setText(_translate("MainWindow", "Номер от левого края"))
        self.radioButton_setPos.setText(_translate("MainWindow", "Указать расположение в шкафу"))
        self.eqaddUserOrInvButton.setText(_translate("MainWindow", "Добавить"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Добавление инвентаря"))
        self.addSmthBox_2.setTitle(_translate("MainWindow", "Добавление пользователя"))
        self.nameOrEmailLabel_3.setText(_translate("MainWindow", "Email"))
        self.rightsLabel_5.setText(_translate("MainWindow", "Кто может получить "))
        self.usfirstRightsCheckBox.setText(_translate("MainWindow", "Обычный пользователь"))
        self.ussecondRightsCheckBox.setText(_translate("MainWindow", "Редактор-модератор"))
        self.usthirdRightsCheckBox.setText(_translate("MainWindow", "Инженер"))
        self.usfourthRightsCheckBox.setText(_translate("MainWindow", "Главный инженер"))
        self.label_9.setText(_translate("MainWindow", "ID карты сотрудника"))
        self.usradioButton_User.setText(_translate("MainWindow", "Пользователь"))
        self.usradioButton_Admin.setText(_translate("MainWindow", "Администратор"))
        self.usadminRightsCheckBox.setText(_translate("MainWindow", "Добавление пользователей"))
        self.usadmin2RightsCheckBox.setText(_translate("MainWindow", "Удаление или редактирование пользователей"))
        self.usadmin3RightsCheckBox.setText(_translate("MainWindow", "Добавление инвентаря"))
        self.usadmin4RightsCheckBox.setText(_translate("MainWindow", "Удаление или редактирование инвентаря"))
        self.usadmin5RightsCheckBox.setText(_translate("MainWindow", "Вынесение решений по запросам"))
        self.rightsLabel_4.setText(_translate("MainWindow", "Имеет права:"))
        self.usaddUserOrInvButton.setText(_translate("MainWindow", "Добавить"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2),
                                  _translate("MainWindow", "Добавление пользователей"))
        self.viewInvOrUserBox.setTitle(_translate("MainWindow", "Просмотр инвентаря"))
        self.eqsearchByIdLabel.setText(_translate("MainWindow", "ID"))
        self.searchByEmailOrNameLabel.setText(_translate("MainWindow", "Название"))
        self.listLabel.setText(_translate("MainWindow", "Все элементы"))
        self.eqsearchByFirstRightsCheckBox.setText(_translate("MainWindow", "Всем пользователям"))
        self.eqsearchBySecondRightsCheckBox.setText(_translate("MainWindow", "Искл. в рамках проекта"))
        self.eqsearchByThirdRightsCheckBox.setText(_translate("MainWindow", "только инженерам"))
        self.eqsearchByFourthRightsCheckBox.setText(_translate("MainWindow", "главным инженерам"))
        self.SearchByRightsLabel.setText(_translate("MainWindow", "Кому выдавать"))
        self.searchByPosGroupBox.setTitle(_translate("MainWindow", "Поиск по расположению в шкафу"))
        self.label_36.setText(_translate("MainWindow", "Высота(от пола)"))
        self.label_37.setText(_translate("MainWindow", "Номер от левого края"))
        self.eqsearchPushButton.setText(_translate("MainWindow", " Поиск"))
        self.eqViewRefreshPushButton.setText(_translate("MainWindow", "Обновить таблицу"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Просмотр инвентаря"))
        self.viewInvOrUserBox_2.setTitle(_translate("MainWindow", "Просмотр пользователей"))
        self.searchByIdLabel_2.setText(_translate("MainWindow", "ID карты пропуска"))
        self.searchByEmailOrNameLabel_2.setText(_translate("MainWindow", "Email"))
        self.listLabel_2.setText(_translate("MainWindow", "Все элементы"))
        self.ussearchByFirstRightsCheckBox.setText(_translate("MainWindow", "Обычный пользователь"))
        self.ussearchBySecondRightsCheckBox.setText(_translate("MainWindow", "Редактор-модератор"))
        self.ussearchByThirdRightsCheckBox.setText(_translate("MainWindow", "Инженер"))
        self.ussearchByFourthRightsCheckBox.setText(_translate("MainWindow", "Главный инженер"))
        self.SearchByRightsLabel_2.setText(_translate("MainWindow", "Права на выдачу"))
        self.ussearchPushButton.setText(_translate("MainWindow", " Поиск"))
        self.usViewRefreshPushButton.setText(_translate("MainWindow", "Обновить таблицу"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4),
                                  _translate("MainWindow", "Просмотр пользователей"))
        self.RequestsGroupBox.setTitle(_translate("MainWindow", "Принятие решений по запросам"))
        self.AcceptReqPushButton.setText(_translate("MainWindow", "Одобрить запрос"))
        self.pushButton_2.setText(_translate("MainWindow", "Отклонить запрос"))
        self.label_2.setText(_translate("MainWindow", "Информация по запросу"))
        self.label_7.setText(_translate("MainWindow", "Информация из базы данных"))
        self.pushButton.setText(_translate("MainWindow", "Предыдущий"))
        self.pushButton_3.setText(_translate("MainWindow", "Следующий"))
        self.label_8.setText(_translate("MainWindow", "Необработанных:"))
        self.reqViewRefreshPushButton.setText(_translate("MainWindow", "Обновить таблицу"))
        self.reqsearchPushButton.setText(_translate("MainWindow", " Поиск"))
        self.searchByIdLabel_4.setText(_translate("MainWindow", "Что"))
        self.searchByEmailOrNameLabel_5.setText(_translate("MainWindow", "Email запросившего"))
        self.searchByIdLabel_5.setText(_translate("MainWindow", "ID запросившего"))
        self.searchByEmailOrNameLabel_6.setText(_translate("MainWindow", "Цель"))
        self.searchByIdLabel_6.setText(_translate("MainWindow", "Количество"))
        self.searchByEmailOrNameLabel_7.setText(_translate("MainWindow", "ID оборудования"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("MainWindow", "Запросы"))
        self.ableNowSpinBox.setMinimum(0)
        self.searchByPosFromLeftSpinBox.setMinimum(1)
        self.searchByHeightSpinBox.setMinimum(1)
        self.usradioButton_Admin.clicked.connect(self.adminRightsGroupBox_2.show)
        self.usradioButton_User.clicked.connect(self.adminRightsGroupBox_2.hide)
        self.eqaddUserOrInvButton.clicked.connect(self.add_equipment)
        self.usaddUserOrInvButton.clicked.connect(self.add_user)
        self.pushButton.clicked.connect(self.previous_request)
        self.pushButton_3.clicked.connect(self.next_request)
        self.AcceptReqPushButton.clicked.connect(self.approve_request)
        self.pushButton_2.clicked.connect(self.reject_request)
        self.eqsearchPushButton.clicked.connect(self.searchEq)
        self.eqViewRefreshPushButton.clicked.connect(self.refresh_equipment_table)
        self.reqViewRefreshPushButton.clicked.connect(self.refresh_requests_table)
        self.usViewRefreshPushButton.clicked.connect(self.refresh_users_table)
        self.ussearchPushButton.clicked.connect(self.search_users)
        self.reqsearchPushButton.clicked.connect(self.search_request)
        self.heightSpinBox.setMinimum(-1)
        self.posFromLeftSpinBox.setMinimum(-1)
        self.heightSpinBox.setValue(-1)
        self.posFromLeftSpinBox.setValue(-1)
        self.eqsearchByIdSpinBox.setMinimum(-1)
        self.searchByPosFromLeftSpinBox.setMinimum(-1)
        self.searchByHeightSpinBox.setValue(-1)
        self.searchByHeightSpinBox.setMinimum(-1)
        self.searchByPosFromLeftSpinBox.setMinimum(-1)
        # self.searchPushButton.clicked.connect(self.searchUsOrEq)
        self.heightSpinBox.setMinimum(-1)
        self.posFromLeftSpinBox.setMinimum(-1)
        self.reqsearchByCount.setMinimum(-1)
        self.reqsearchByEqId.setMinimum(-1)
        self.reqsearchByCount.setValue(-1)
        self.reqsearchByEqId.setValue(-1)
        if not admin_access.can_get_request:
            self.tab_5.hide()
        if not admin_access.can_add_users:
            self.tab_2.hide()
        if not admin_access.can_add_inventory:
            self.tab.hide()
        self.adminRightsGroupBox_2.hide()

        self.refresh_requests_table()
        self.refresh_equipment_table()
        self.refresh_users_table()

        self.show()

    def add_equipment(self):
        code_error = -1
        tg = 0
        if code_error == -1 and self.eqNameOrEmailLineEdit.text() == "":
            code_error = 1
        elif self.__db.get_equipment_by_title(self.eqNameOrEmailLineEdit.text()):
            code_error = 8
        if code_error == -1 and self.descriptionTextEdit.toPlainText() == "":
            code_error = 3
        if code_error == -1 and self.eqfirstRightsCheckBox.isChecked():
            tg += 1
        if code_error == -1 and self.eqsecondRightsCheckBox.isChecked():
            tg += 10
        if code_error == -1 and self.eqthirdRightsCheckBox.isChecked():
            tg += 100
        if code_error == -1 and self.eqfourthRightsCheckBox.isChecked():
            tg += 1000
        if code_error == -1 and tg == 0:
            code_error = 2
        from_left = self.posFromLeftSpinBox.value()
        if self.posFromLeftSpinBox.value() == 0 or self.posFromLeftSpinBox.value() == -1:
            from_left = -1
        height = self.heightSpinBox.value()
        if self.heightSpinBox.value() == 0 or self.heightSpinBox.value() == -1:
            height = -1
        if code_error == -1 and self.__db.get_equipment_by_coordinates(from_left, height) is not None:
            code_error = 9
        if code_error == -1:
            eq = Equipment(self.eqNameOrEmailLineEdit.text(),
                           self.descriptionTextEdit.toPlainText(),
                           self.ableNowSpinBox.value(), self.reservedSpinBox.value(), tg, height, from_left)
            show_message("Успех", "Оборудование добавлено в базу")
            self.__db.add_equipment(eq)
            self.heightSpinBox.setValue(-1)
            self.posFromLeftSpinBox.setValue(-1)
            self.eqfirstRightsCheckBox.setChecked(False)
            self.eqsecondRightsCheckBox.setChecked(False)
            self.eqthirdRightsCheckBox.setChecked(False)
            self.eqfourthRightsCheckBox.setChecked(False)
            self.eqNameOrEmailLineEdit.setText("")
            self.descriptionTextEdit.setText("")
            self.heightSpinBox.setValue(-1)
            self.posFromLeftSpinBox.setValue(-1)
        else:
            if code_error == 1:
                show_message("Ошибка добавления", "Введите название")
            elif code_error == 2:
                show_message("Ошибка добавления", "Не отмечены требования выдачи")
            elif code_error == 3:
                show_message("Ошибка добавления", "отсутствует описание")
            elif code_error == 8:
                show_message("Ошибка добавления", "Оборудование с таким названием уже есть в базе")
            elif code_error == 9:
                show_message("Ошибка добавления", "Ячейка занята")

    def add_user(self):
        code_error = -1
        tg = 0
        add_users = False
        change_users = False
        add_equipment = False
        change_equipment = False
        get_request = False
        if code_error == -1 and self.usnameOrEmailLineEdit.text() == "":
            code_error = 1
        if code_error == -1 and self.usIdCardLineEdit.text() == "":
            code_error = 4
        if code_error == -1 and (not self.usradioButton_User.isChecked()) and (
                not self.usradioButton_Admin.isChecked()):
            code_error = 6
        if code_error == -1 and self.usradioButton_Admin.isChecked():
            if self.usadminRightsCheckBox.isChecked():
                add_users = True
            if self.usadmin2RightsCheckBox.isChecked():
                change_users = True
            if self.usadmin3RightsCheckBox.isChecked():
                add_equipment = True
            if self.usadmin4RightsCheckBox.isChecked():
                change_equipment = True
            if self.usadmin5RightsCheckBox.isChecked():
                get_request = True
            if (not add_users) and (not change_equipment) and (not change_users) and add_equipment and get_request:
                code_error = 5
        if code_error == -1 and self.usradioButton_User.isChecked():
            add_users = False
            change_users = False
            add_equipment = False
            change_equipment = False
            get_request = False
        if code_error == -1 and self.usfirstRightsCheckBox.isChecked():
            tg += 1
        if code_error == -1 and self.ussecondRightsCheckBox.isChecked():
            tg += 10
        if code_error == -1 and self.usthirdRightsCheckBox.isChecked():
            tg += 100
        if code_error == -1 and self.usfourthRightsCheckBox.isChecked():
            tg += 1000
        if code_error == -1 and tg == 0:
            code_error = 2
        if code_error == -1 and self.__db.get_user_by_id(int(self.usIdCardLineEdit.text(), 16)) is not None:
            code_error = 7
        if code_error == -1 and self.__db.get_user_by_mail(self.usnameOrEmailLineEdit.text()) is not None:
            code_error = 8
        if code_error == -1:
            if self.usradioButton_User.isChecked():
                ac = Access(tg)
                us = CommonUser(int(self.usIdCardLineEdit.text(), 16), str(self.usnameOrEmailLineEdit.text()), ac)
                self.__user_list.append_user(us)
            if self.usradioButton_Admin.isChecked():
                ac = AdminAccess(tg, add_users, change_users, add_equipment, change_equipment, get_request)
                adm = Admin(int(self.usIdCardLineEdit.text(), 16), str(self.usnameOrEmailLineEdit.text()), "", ac)
                self.__user_list.append_user(adm)
            self.heightSpinBox.setValue(-1)
            self.posFromLeftSpinBox.setValue(-1)
            self.usfirstRightsCheckBox.setChecked(False)
            self.ussecondRightsCheckBox.setChecked(False)
            self.usthirdRightsCheckBox.setChecked(False)
            self.usfourthRightsCheckBox.setChecked(False)
            self.usnameOrEmailLineEdit.setText("")
            self.descriptionTextEdit.setText("")
            self.usIdCardLineEdit.setText("")
        else:
            if code_error == 1:
                show_message("Ошибка добавления", "Введите Email")
            elif code_error == 2:
                show_message("Ошибка добавления", "Не отмечены права на получение")
            elif code_error == 3:
                show_message("Ошибка добавления", "отсутствует описание")
            elif code_error == 4:
                show_message("Ошибка добавления", "не введен ID карты сотрудника")
            elif code_error == 5:
                show_message("Ошибка добавления", "не выбраны права администратора")
            elif code_error == 6:
                show_message("Ошибка добавления", "Не выбран тип пользователя")
            elif code_error == 7:
                show_message("Ошибка добавления", "пользователь с такой картой уже добавлен")
            elif code_error == 8:
                show_message("Ошибка добавления", "Пользователь с таким email уже добавлен")

    def refresh_equipment_table(self):
        self.eqsearchByIdSpinBox.setValue(-1)
        self.searchByHeightSpinBox.setValue(-1)
        self.eqTableView.clearSpans()
        self.__eqTableContents.clear()
        all_eq = self.__db.get_all_equipment()
        for i in all_eq:
            x = ""
            y = ""
            if i.x == -1:
                x = "--"
            else:
                x = str(i.x)
            if i.y == -1:
                y = "--"
            else:
                y = str(i.y)
            self.__eqTableContents.append([
                str(i.id),
                str(i.title),
                str(i.count),
                str(i.reserve_count),
                str(i.access),
                x,
                y])
        data_frame = pd.DataFrame(self.__eqTableContents,
                                  columns=["ID", "Название", "Количество", "Зарезервировано",
                                           "Доступ", "От стены", "От пола"],
                                  index=[i for i in range(len(self.__eqTableContents))])
        model = TableModel(data_frame)
        self.eqTableView.setModel(model)

    def refresh_users_table(self):
        self.usTableView.clearSpans()
        ref = AdminAccess
        self.__usTableContents.clear()
        for i in self.__user_list.get_user_list():
            self.__usTableContents.append([
                str(hex(i.id)),
                i.mail,
                i.access.power
            ])
        data_frame = pd.DataFrame(self.__usTableContents, columns=["ID карты", "Почта", "Доступ"],
                                  index=[i for i in range(len(self.__usTableContents))])
        model = TableModel(data_frame)
        self.usTableView.setModel(model)

    def search_users(self):
        tg = 0
        found = []
        found2 = []
        found3 = []
        foundres = []
        if self.ussearchByNameOrEmailLineEdit.text() != "":
            id = self.ussearchByNameOrEmailLineEdit.text()
            for i in self.__usTableContents:
                if i[0] == id:
                    found.append(i)
        if self.ussearchByEmailOrNameLineEdit.text() != "":
            name = self.ussearchByEmailOrNameLineEdit.text()
            for i in self.__usTableContents:
                if i[1] == self.ussearchByEmailOrNameLineEdit.text():
                    found2.append(i)
        if self.ussearchByFirstRightsCheckBox.isChecked():
            tg += 1
        if self.ussearchBySecondRightsCheckBox.isChecked():
            tg += 10
        if self.ussearchByThirdRightsCheckBox.isChecked():
            tg += 100
        if self.ussearchByFourthRightsCheckBox.isChecked():
            tg += 1000
        if tg != 0:
            for i in self.__usTableContents:
                if i[2] == tg:
                    found3.append(i)
        if len(found) != 0:
            foundres = found
            if len(found2) != 0:
                foundres = [x for x in foundres if x in found2]
            if len(found3) != 0:
                foundres = [x for x in foundres if x in found3]
        if len(found2) != 0 and len(found) == 0:
            foundres = found2
            if len(found3) != 0:
                foundres = [x for x in foundres if x in found3]
        if len(found3) != 0 and len(found2) == 0 and len(found) == 0:
            foundres = found3
        if len(foundres) != 0:
            self.usTableView.clearSpans()
            data_frame = pd.DataFrame(foundres, columns=["ID карты", "Почта", "Доступ"],
                                      index=[i for i in range(len(foundres))])
            model = TableModel(data_frame)
            self.usTableView.setModel(model)
        else:
            show_message("Проблема", "Ничего не найдено")

    def searchEq(self):
        tg = 0
        found = []
        found2 = []
        found3 = []
        found4 = []
        found5 = []
        foundres = []
        if self.eqsearchByIdSpinBox.value() != -1:
            id = self.eqsearchByIdSpinBox.value()
            for i in self.__eqTableContents:
                if i[0] == str(self.eqsearchByIdSpinBox.value()):
                    found.append(i)
        if self.eqsearchByEmailOrNameLineEdit.text() != "":
            name = self.eqsearchByEmailOrNameLineEdit.text()
            for i in self.__eqTableContents:
                if i[1] == self.eqsearchByEmailOrNameLineEdit.text():
                    found2.append(i)
        if self.eqsearchByFirstRightsCheckBox.isChecked():
            tg += 1
        if self.eqsearchBySecondRightsCheckBox.isChecked():
            tg += 10
        if self.eqsearchByThirdRightsCheckBox.isChecked():
            tg += 100
        if self.eqsearchByFourthRightsCheckBox.isChecked():
            tg += 1000
        if self.searchByHeightSpinBox.value() != -1:
            for i in self.__eqTableContents:
                if i[6] == str(self.searchByHeightSpinBox.value()):
                    found4.append(i)
        if self.searchByPosFromLeftSpinBox.value() != -1:
            for i in self.__eqTableContents:
                if i[5] == str(self.searchByPosFromLeftSpinBox.value()):
                    found5.append(i)
        if tg != 0:
            for i in self.__eqTableContents:
                if i[4] == str(tg):
                    found3.append(i)
        if len(found) != 0:
            foundres = found
            if len(found2) != 0:
                foundres = [x for x in foundres if x in found2]
            if len(found3) != 0:
                foundres = [x for x in foundres if x in found3]
            if len(found4) != 0:
                foundres = [x for x in foundres if x in found4]
            if len(found5) != 0:
                foundres = [x for x in foundres if x in found5]
        if len(found2) != 0 and len(found) == 0:
            foundres = found2
            if len(found3) != 0:
                foundres = [x for x in foundres if x in found3]
            if len(found4) != 0:
                foundres = [x for x in foundres if x in found4]
            if len(found5) != 0:
                foundres = [x for x in foundres if x in found5]
        if len(found3) != 0 and len(found2) == 0 and len(found) == 0:
            foundres = found3
            if len(found4) != 0:
                foundres = [x for x in foundres if x in found4]
            if len(found5) != 0:
                foundres = [x for x in foundres if x in found5]
        if len(found4) != 0:
            foundres = found4
            if len(found5) != 0:
                foundres = [x for x in foundres if x in found5]
        if len(found5) != 0:
            foundres = found5
            if len(found4) != 0:
                foundres = [x for x in foundres if x in found4]
        if len(foundres) != 0:
            self.eqTableView.clearSpans()
            data_frame = pd.DataFrame(foundres,
                                      columns=["ID", "Название", "Количество", "Зарезервировано",
                                               "Доступ", "От стены", "От пола"],
                                      index=[i for i in range(len(foundres))])
            model = TableModel(data_frame)
            self.eqTableView.setModel(model)
        else:
            show_message("Проблема", "Ничего не найдено")

    def search_request(self):
        tg = 0
        found = []
        found2 = []
        found3 = []
        found4 = []
        found5 = []
        found6 = []
        foundres = []
        if self.reqsearchByEmail.text() != "":
            for i in self.__reqTableContents:
                if i[5] == self.reqsearchByEmail.text():
                    found.append(i)
        if self.reqsearchByUsId.text() != "":
            for i in self.__reqTableContents:
                if i[4] == str(int(self.reqsearchByUsId.text(), 16)):
                    found2.append(i)
        if self.reqsearchByWhat.text() != "":
            for i in self.__reqTableContents:
                if i[1] == self.reqsearchByWhat.text():
                    found3.append(i)
        if self.reqsearchByPurpose.text() != "":
            for i in self.__reqTableContents:
                if i[3] == self.reqsearchByPurpose.text():
                    found4.append(i)
        if self.reqsearchByCount.value() != -1:
            for i in self.__reqTableContents:
                if i[2] == str(self.reqsearchByCount.value()):
                    found5.append(i)
        if self.reqsearchByEqId.value() != -1:
            for i in self.__reqTableContents:
                if i[0] == str(self.reqsearchByEqId.value()):
                    found6.append(i)
        if len(found) != 0:
            foundres = found
            if len(found2) != 0:
                foundres = [x for x in foundres if x in found2]
            if len(found3) != 0:
                foundres = [x for x in foundres if x in found3]
            if len(found4) != 0:
                foundres = [x for x in foundres if x in found4]
            if len(found5) != 0:
                foundres = [x for x in foundres if x in found5]
            if len(found6) != 0:
                foundres = [x for x in foundres if x in found6]
        if len(found2) != 0 and len(found) == 0:
            foundres = found2
            if len(found3) != 0:
                foundres = [x for x in foundres if x in found3]
            if len(found4) != 0:
                foundres = [x for x in foundres if x in found4]
            if len(found5) != 0:
                foundres = [x for x in foundres if x in found5]
            if len(found6) != 0:
                foundres = [x for x in foundres if x in found6]
        if len(found3) != 0 and len(found2) == 0 and len(found) == 0:
            foundres = found3
            if len(found4) != 0:
                foundres = [x for x in foundres if x in found4]
            if len(found5) != 0:
                foundres = [x for x in foundres if x in found5]
            if len(found6) != 0:
                foundres = [x for x in foundres if x in found6]
        if len(found4) != 0:
            foundres = found4
            if len(found5) != 0:
                foundres = [x for x in foundres if x in found5]
            if len(found6) != 0:
                foundres = [x for x in foundres if x in found6]
        if len(found5) != 0:
            foundres = found5
            if len(found4) != 0:
                foundres = [x for x in foundres if x in found4]
            if len(found6) != 0:
                foundres = [x for x in foundres if x in found6]
        if len(foundres) != 0:
            data_frame = pd.DataFrame(foundres,
                                      columns=["ID", "Что", "Сколько", "Цель", "ID запросившего", "EMAIL запросившего"],
                                      index=[i for i in range(len(foundres))]
                                      )
            model = TableModel(data_frame)
            self.tableView2.setModel(model)
        else:
            show_message("Проблема", "Ничего не найдено")

    def refresh_requests_table(self):
        # self.__reqs = self.__db.get_unsolved_requests()
        self.tableView2.clearSpans()
        self.__reqs = self.__db.get_all_requests()
        if (len(self.__reqs)) == 0:
            print("0 requests")
        self.__reqnum = 0
        self.__reqTableContents.clear()
        for i in self.__reqs:
            self.__reqTableContents.append([
                str(i.id),
                str(i.title),
                str(i.count),
                str(i.purpose),
                str(hex(i.sender_tg_id)),
                str(i.sender_mail)
            ])
        data_frame = pd.DataFrame(self.__reqTableContents,
                                  columns=["ID", "Что", "Сколько", "Цель", "ID запросившего", "EMAIL запросившего"],
                                  index=[i for i in range(len(self.__reqTableContents))]
                                  )
        model = TableModel(data_frame)
        self.tableView2.setModel(model)
        self.label_8.setText("Необработанных: " + str(len(self.__reqs)))
        self.get_request()

    def get_request(self):
        if self.__reqnum < len(self.__reqs):
            a = "EMAIL: " + str(self.__reqs[self.__reqnum].sender_mail) + "\n ID запросившего: " + str(
                self.__reqs[self.__reqnum].sender_tg_id) + "\n Что запрашивается: " + str(
                self.__reqs[self.__reqnum].title) + "\n Сколько: " + str(
                self.__reqs[self.__reqnum].count) + "\n Цель: " + str(self.__reqs[self.__reqnum].purpose)
            self.textBrowser.setText(a)
        else:
            self.__reqnum -= 1
            show_message("Сообщение", "Запросов нет")

    def previous_request(self):
        if self.__reqnum > 0:
            self.__reqnum = self.__reqnum - 1
            self.get_request()
        else:
            show_message("Ошибка", "Запрос уже первый в списке")

    def next_request(self):
        if self.__reqnum < len(self.__reqs):
            self.__reqnum = self.__reqnum + 1
            self.get_request()
        else:
            show_message("Ошибка", "Запрос последний в списке")

    def reject_request(self):
        self.decide_request(False)

    def approve_request(self):
        self.decide_request(True)

    def decide_request(self, decision):
        if len(self.__reqs) != 0:
            self.__reqs[self.__reqnum].approved = decision
            print(self.__reqnum)
            self.__reqs[self.__reqnum].approved_id = self.__current_user.id
            self.__db.update_request(self.__reqs[self.__reqnum])
            self.__reqs.remove(self.__reqs[self.__reqnum])
            self.tableView2.model().removeRow(self.__reqnum)
            self.tableView2.update()
            self.label_8.setText("Необработанных: " + str(len(self.__reqs)))
        else:
            show_message("Ошибка", "Запросов нет")

    class TableModel(QtCore.QAbstractTableModel):
        def __init__(self, data):
            super(TableModel, self).__init__()
            self._data = data

        def data(self, index, role):
            if role == Qt.ItemDataRole.DisplayRole:
                value = self._data.iloc[index.row(), index.column()]
                return str(value)

        def rowCount(self, index):
            return self._data.shape[0]

        def columnCount(self, parent: QtCore.QModelIndex) -> int:
            return self._data.shape[1]

        def headerData(self, section: int, orientation, role: int):
            # section is the index of the column/row.
            if role == Qt.ItemDataRole.DisplayRole:
                if orientation == Qt.Orientation.Horizontal:
                    return str(self._data.columns[section])

                if orientation == Qt.Orientation.Vertical:
                    if len(self._data.index) <= section:
                        return ""
                    return str(self._data.index[section])

        def removeRow(self, row: int, parent=None):
            self._data.drop(row, inplace=True)
            self._data.reset_index(drop=True, inplace=True)

        def setData(self, index: QtCore.QModelIndex, value, role: int = ...) -> bool:
            if role == Qt.ItemDataRole.EditRole:
                self._data.iloc[index.row(), index.column()] = value
                return True
            return False

        def flags(self, index: QtCore.QModelIndex) -> Qt.ItemFlag:
            return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable
