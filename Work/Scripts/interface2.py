from PyQt6.QtWidgets import QMainWindow, QLineEdit, QPushButton, QLabel, QFrame, QMessageBox, QHeaderView
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, pyqtSlot
from PyQt6 import QtCore, QtGui, QtWidgets
from equipment_collections import EquipmentCollection
from Work.Scripts.interface import TableModel
from user_collections import *
from equipment import *
from database import *
from accesses import *
from users import *
from accesses import *
import pandas as pd


class QDoublePushButton(QPushButton):
    doubleClicked = pyqtSignal()
    clicked = pyqtSignal()

    def __init__(self, *args, **kwargs):
        QPushButton.__init__(self, *args, **kwargs)
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.clicked.emit)
        super().clicked.connect(self.checkDoubleClick)

    @pyqtSlot()
    def checkDoubleClick(self):
        if self.timer.isActive():
            self.doubleClicked.emit()
            self.timer.stop()
        else:
            self.timer.start(250)


class LogWindow(QMainWindow):
    loggedSignal = QtCore.pyqtSignal()

    def __init__(self, user_list: UserCollection, equipment_list: EquipmentCollection, db: DataBase):
        super(LogWindow, self).__init__()
        self.__main_window = MainWindow
        self.__db = db
        self.__user_list = user_list
        self.__equipment_list = equipment_list
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
        #     if isinstance(user, Admin) and user.password == self.__password_field.text():
        if isinstance(user, Admin):
            self.__db.change_user(user.mail, self.__password_field.text())
            self.hide()
            self.__main_window = MainWindow(self.__user_list, self.__equipment_list, user, self.__db, user.access)
        else:
            self.__label.setText("Введены неверные данные!")
            self.__password_field.setText("")


def show_message(title: str, info: str):
    msg_box = QMessageBox()
    msg_box.setText(info)
    msg_box.setWindowTitle(title)
    msg_box.exec()


class MainWindow(QMainWindow):
    def __init__(self,
                 user_list: UserCollection,
                 equipment_list: EquipmentCollection,
                 current_user,
                 db: DataBase,
                 admin_access: AdminAccess):
        super(MainWindow, self).__init__()
        self.setWindowTitle("App")
        self.setFixedSize(1700, 1000)
        self.setStyleSheet("background-color:#F0F8FF;")
        self.__current_user = current_user
        self.__user_list = user_list
        self.__equipment_list = equipment_list
        self.__db = db
        self.__eqTableContents = [] #Содержимое таблицы просмотра оборудования
        self.__usTableContents = [] #содержимое таблицы просмотра пользователей
        self.__reqTableContents = [] #содержимое таблицы просмотра запросов
        self.__usFoundTableContents = [] #найденные пользователи
        self.__eqFoundTableContents = [] #найденное оборудование
        self.__usFoundGroups = [] #id групп найденного пользователя
        self.__eqFoundGroups = [] #id групп найденного оборудования
        self.__grTableContents = [] #содержимое таблицы групп
        self.__currUsGroupsTableContents = [] #группы найденного пользователя в таблице группы пользователя
        self.__currEqGroupsTableContents = [] #группы найденного оборудования в таблице группы оборудования
        self.__addUsTableContents = [] #содержимое таблицы групп добавляемого пользователя
        self.__addEqTableContents = [] #содержимое таблицы групп добавляемого оборудования
        self.__currGroupsTableContents = []
        self.__allGroups = {} #
        self.__admin_access = admin_access  # Права админа, зашедшего в приложение
        self.__reqs = self.__db.get_unsolved_users_requests()
        self.__reqnum = 0
        self.__eqnum = -1
        self.__usnum = -1
        self.__grnum = -2
        # self.eqTableView.setGeometry(QtCore.QRect(600, 40, 581, 721))
        # self.usTableView.setGeometry(QtCore.QRect(620, 30, 701, 721))
        # self.__sidePanel = QFrame(self)
        # self.__sidePanel.setFixedSize(200, 720)
        # self.__sidePanel.setStyleSheet("background-color:#FFFFFF;")
        # self.__button = QPushButton(self.__sidePanel)
        # self.__button.setFixedSize(180, 30)
        # self.__button.setText("Test")
        # self.__button.setStyleSheet("QPushButton { border-radius: 10; border : 1px solid white; color: #808080;}"
        #                            "QPushButton:hover { background-color: #000000; color: white;} ")

        self.centralwidget = QtWidgets.QWidget(parent=self)
        self.centralwidget.setStyleSheet("QWidget#centralwidget{\n"
                                         "    border: 0;\n"
                                         "}")
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(parent=self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1721, 821))
        self.tabWidget.setStyleSheet("QTabWidget#tabWidget{\n"
                                     "    border: 0;\n"
                                     "}")
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.addSmthBox = QtWidgets.QGroupBox(parent=self.tab)
        self.addSmthBox.setEnabled(True)
        self.addSmthBox.setGeometry(QtCore.QRect(10, 10, 1131, 751))
        self.addSmthBox.setStyleSheet("QGroupBox#addSmthBox{\n"
                                      "    border: 0;\n"
                                      "}")
        self.addSmthBox.setTitle("")
        self.addSmthBox.setObjectName("addSmthBox")
        self.label_4 = QtWidgets.QLabel(parent=self.addSmthBox)
        self.label_4.setGeometry(QtCore.QRect(10, 30, 61, 21))
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.nameOrEmailLabel_2 = QtWidgets.QLabel(parent=self.addSmthBox)
        self.nameOrEmailLabel_2.setGeometry(QtCore.QRect(10, 30, 91, 16))
        self.nameOrEmailLabel_2.setObjectName("nameOrEmailLabel_2")
        self.eqNameOrEmailLineEdit = QtWidgets.QLineEdit(parent=self.addSmthBox)
        self.eqNameOrEmailLineEdit.setGeometry(QtCore.QRect(90, 30, 341, 22))
        self.eqNameOrEmailLineEdit.setObjectName("eqNameOrEmailLineEdit")
        self.ableNowSpinBox = QtWidgets.QSpinBox(parent=self.addSmthBox)
        self.ableNowSpinBox.setGeometry(QtCore.QRect(270, 70, 151, 22))
        self.ableNowSpinBox.setObjectName("ableNowSpinBox")
        self.label_27 = QtWidgets.QLabel(parent=self.addSmthBox)
        self.label_27.setGeometry(QtCore.QRect(220, 220, 121, 16))
        self.label_27.setObjectName("label_27")
        self.label_12 = QtWidgets.QLabel(parent=self.addSmthBox)
        self.label_12.setGeometry(QtCore.QRect(10, 130, 81, 20))
        self.label_12.setObjectName("label_12")
        self.posFromLeftSpinBox = QtWidgets.QSpinBox(parent=self.addSmthBox)
        self.posFromLeftSpinBox.setGeometry(QtCore.QRect(350, 220, 71, 22))
        self.posFromLeftSpinBox.setObjectName("posFromLeftSpinBox")
        self.heightSpinBox = QtWidgets.QSpinBox(parent=self.addSmthBox)
        self.heightSpinBox.setGeometry(QtCore.QRect(140, 220, 61, 22))
        self.heightSpinBox.setObjectName("heightSpinBox")
        self.label_11 = QtWidgets.QLabel(parent=self.addSmthBox)
        self.label_11.setGeometry(QtCore.QRect(60, 70, 171, 16))
        self.label_11.setObjectName("label_11")
        self.descriptionTextEdit = QtWidgets.QTextEdit(parent=self.addSmthBox)
        self.descriptionTextEdit.setGeometry(QtCore.QRect(110, 130, 311, 51))
        self.descriptionTextEdit.setStyleSheet("QTextEdit {\n"
                                               "border: 1px solid black;\n"
                                               "}")
        self.descriptionTextEdit.setObjectName("descriptionTextEdit")
        self.label_26 = QtWidgets.QLabel(parent=self.addSmthBox)
        self.label_26.setGeometry(QtCore.QRect(10, 220, 121, 16))
        self.label_26.setObjectName("label_26")
        self.label_10 = QtWidgets.QLabel(parent=self.addSmthBox)
        self.label_10.setGeometry(QtCore.QRect(10, 100, 231, 16))
        self.label_10.setObjectName("label_10")
        self.reservedSpinBox = QtWidgets.QSpinBox(parent=self.addSmthBox)
        self.reservedSpinBox.setGeometry(QtCore.QRect(270, 100, 151, 22))
        self.reservedSpinBox.setObjectName("reservedSpinBox")
        self.radioButton_setPos = QtWidgets.QRadioButton(parent=self.addSmthBox)
        self.radioButton_setPos.setGeometry(QtCore.QRect(80, 190, 251, 20))
        self.radioButton_setPos.setObjectName("radioButton_setPos")
        self.eqDelFromSelectedGr = QtWidgets.QPushButton(parent=self.addSmthBox)
        self.eqDelFromSelectedGr.setGeometry(QtCore.QRect(630, 160, 61, 41))
        self.eqDelFromSelectedGr.setStyleSheet("QPushButton{\n"
                                               " background-color: #081f2d; \n"
                                               " border-radius: 8px; \n"
                                               " border: 2px solid #081F2D; \n"
                                               " color: white; \n"
                                               " font-size: 15px;  \n"
                                               " cursor: pointer; \n"
                                               " transition: 0.3s; \n"
                                               " }\n"
                                               " \n"
                                               "QPushButton:hover{ \n"
                                               " background-color: white; \n"
                                               " color: #081F2D; \n"
                                               " border-color: #081F2D;\n"
                                               " transition: 0.9s; \n"
                                               "}")
        self.eqDelFromSelectedGr.setObjectName("eqDelFromSelectedGr")
        self.eqAddGroupByName = QtWidgets.QLineEdit(parent=self.addSmthBox)
        self.eqAddGroupByName.setGeometry(QtCore.QRect(190, 300, 191, 22))
        self.eqAddGroupByName.setObjectName("eqAddGroupByName")
        self.searchByEmailOrNameLabel_4 = QtWidgets.QLabel(parent=self.addSmthBox)
        self.searchByEmailOrNameLabel_4.setGeometry(QtCore.QRect(30, 300, 161, 16))
        self.searchByEmailOrNameLabel_4.setObjectName("searchByEmailOrNameLabel_4")
        self.eqAddRefreshGroupButton = QtWidgets.QPushButton(parent=self.addSmthBox)
        self.eqAddRefreshGroupButton.setGeometry(QtCore.QRect(20, 380, 401, 41))
        self.eqAddRefreshGroupButton.setStyleSheet("QPushButton{\n"
                                                   " background-color: #081f2d; \n"
                                                   " border-radius: 8px; \n"
                                                   " border: 2px solid #081F2D; \n"
                                                   " color: white; \n"
                                                   " font-size: 15px;  \n"
                                                   " cursor: pointer; \n"
                                                   " transition: 0.3s; \n"
                                                   " }\n"
                                                   " \n"
                                                   "QPushButton:hover{ \n"
                                                   " background-color: white; \n"
                                                   " color: #081F2D; \n"
                                                   " border-color: #081F2D;\n"
                                                   " transition: 0.9s; \n"
                                                   "}")
        self.eqAddRefreshGroupButton.setObjectName("eqAddRefreshGroupButton")
        self.eqAddAllGrTableView = QtWidgets.QTableView(parent=self.addSmthBox)
        self.eqAddAllGrTableView.setGeometry(QtCore.QRect(700, 20, 421, 401))
        self.eqAddAllGrTableView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.eqAddAllGrTableView.setObjectName("eqAddAllGrTableView")
        self.eqAddSelectedGrTableView = QtWidgets.QTableView(parent=self.addSmthBox)
        self.eqAddSelectedGrTableView.setGeometry(QtCore.QRect(450, 20, 171, 361))
        self.eqAddSelectedGrTableView.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.eqAddSelectedGrTableView.setObjectName("eqAddSelectedGrTableView")
        self.eqGrToSelected = QtWidgets.QPushButton(parent=self.addSmthBox)
        self.eqGrToSelected.setGeometry(QtCore.QRect(630, 210, 61, 41))
        self.eqGrToSelected.setStyleSheet("QPushButton{\n"
                                          " background-color: #081f2d; \n"
                                          " border-radius: 8px; \n"
                                          " border: 2px solid #081F2D; \n"
                                          " color: white; \n"
                                          " font-size: 15px;  \n"
                                          " cursor: pointer; \n"
                                          " transition: 0.3s; \n"
                                          " }\n"
                                          " \n"
                                          "QPushButton:hover{ \n"
                                          " background-color: white; \n"
                                          " color: #081F2D; \n"
                                          " border-color: #081F2D;\n"
                                          " transition: 0.9s; \n"
                                          "}")
        self.eqGrToSelected.setObjectName("eqGrToSelected")
        self.eqAddSearchGroupButton = QtWidgets.QPushButton(parent=self.addSmthBox)
        self.eqAddSearchGroupButton.setGeometry(QtCore.QRect(20, 330, 401, 41))
        self.eqAddSearchGroupButton.setStyleSheet("QPushButton{\n"
                                                  " background-color: #081f2d; \n"
                                                  " border-radius: 8px; \n"
                                                  " border: 2px solid #081F2D; \n"
                                                  " color: white; \n"
                                                  " font-size: 15px;  \n"
                                                  " cursor: pointer; \n"
                                                  " transition: 0.3s; \n"
                                                  " }\n"
                                                  " \n"
                                                  "QPushButton:hover{ \n"
                                                  " background-color: white; \n"
                                                  " color: #081F2D; \n"
                                                  " border-color: #081F2D;\n"
                                                  " transition: 0.9s; \n"
                                                  "}")
        self.eqAddSearchGroupButton.setObjectName("eqAddSearchGroupButton")
        self.eqAddUserOrInvButton = QtWidgets.QPushButton(parent=self.addSmthBox)
        self.eqAddUserOrInvButton.setGeometry(QtCore.QRect(30, 250, 401, 41))
        self.eqAddUserOrInvButton.setStyleSheet("QPushButton{\n"
                                                " background-color: #081f2d; \n"
                                                " border-radius: 8px; \n"
                                                " border: 2px solid #081F2D; \n"
                                                " color: white; \n"
                                                " font-size: 15px;  \n"
                                                " cursor: pointer; \n"
                                                " transition: 0.3s; \n"
                                                " }\n"
                                                " \n"
                                                "QPushButton:hover{ \n"
                                                " background-color: white; \n"
                                                " color: #081F2D; \n"
                                                " border-color: #081F2D;\n"
                                                " transition: 0.9s; \n"
                                                "}")
        self.eqAddUserOrInvButton.setObjectName("eqAddUserOrInvButton")
        self.eqAddDeleteGroupsButton = QtWidgets.QPushButton(parent=self.addSmthBox)
        self.eqAddDeleteGroupsButton.setGeometry(QtCore.QRect(450, 390, 171, 31))
        self.eqAddDeleteGroupsButton.setStyleSheet("QPushButton{\n"
                                                   " background-color: #081f2d; \n"
                                                   " border-radius: 8px; \n"
                                                   " border: 2px solid #081F2D; \n"
                                                   " color: white; \n"
                                                   " font-size: 15px;  \n"
                                                   " cursor: pointer; \n"
                                                   " transition: 0.3s; \n"
                                                   " }\n"
                                                   " \n"
                                                   "QPushButton:hover{ \n"
                                                   " background-color: white; \n"
                                                   " color: #081F2D; \n"
                                                   " border-color: #081F2D;\n"
                                                   " transition: 0.9s; \n"
                                                   "}")
        self.eqAddDeleteGroupsButton.setObjectName("eqAddDeleteGroupsButton")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.addSmthBox_2 = QtWidgets.QGroupBox(parent=self.tab_2)
        self.addSmthBox_2.setGeometry(QtCore.QRect(20, 10, 1211, 711))
        self.addSmthBox_2.setStyleSheet("QGroupBox#addSmthBox_2{\n"
                                        "    border: 0;\n"
                                        "}")
        self.addSmthBox_2.setTitle("")
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
        self.label_9 = QtWidgets.QLabel(parent=self.addSmthBox_2)
        self.label_9.setGeometry(QtCore.QRect(10, 60, 171, 16))
        self.label_9.setObjectName("label_9")
        self.usIdCardLineEdit = QtWidgets.QLineEdit(parent=self.addSmthBox_2)
        self.usIdCardLineEdit.setGeometry(QtCore.QRect(180, 60, 211, 22))
        self.usIdCardLineEdit.setObjectName("usIdCardLineEdit")
        self.addHuman_groupBox_2 = QtWidgets.QGroupBox(parent=self.addSmthBox_2)
        self.addHuman_groupBox_2.setGeometry(QtCore.QRect(-20, 110, 561, 231))
        self.addHuman_groupBox_2.setStyleSheet("QGroupBox#addHuman_groupBox_2{\n"
                                               "    border: 0;\n"
                                               "}")
        self.addHuman_groupBox_2.setTitle("")
        self.addHuman_groupBox_2.setObjectName("addHuman_groupBox_2")
        self.usradioButton_User = QtWidgets.QRadioButton(parent=self.addHuman_groupBox_2)
        self.usradioButton_User.setGeometry(QtCore.QRect(220, 20, 141, 20))
        self.usradioButton_User.setObjectName("usradioButton_User")
        self.usradioButton_Admin = QtWidgets.QRadioButton(parent=self.addHuman_groupBox_2)
        self.usradioButton_Admin.setGeometry(QtCore.QRect(220, 0, 141, 20))
        self.usradioButton_Admin.setObjectName("usradioButton_Admin")
        self.adminRightsGroupBox_2 = QtWidgets.QGroupBox(parent=self.addHuman_groupBox_2)
        self.adminRightsGroupBox_2.setGeometry(QtCore.QRect(0, 40, 501, 181))
        self.adminRightsGroupBox_2.setStyleSheet("QGroupBox#adminRightsGroupBox_2{\n"
                                                 "    border: 0;\n"
                                                 "}")
        self.adminRightsGroupBox_2.setTitle("")
        self.adminRightsGroupBox_2.setObjectName("adminRightsGroupBox_2")
        self.verticalLayoutWidget_6 = QtWidgets.QWidget(parent=self.adminRightsGroupBox_2)
        self.verticalLayoutWidget_6.setGeometry(QtCore.QRect(140, 10, 354, 151))
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
        self.rightsLabel_4.setGeometry(QtCore.QRect(20, 10, 101, 16))
        self.rightsLabel_4.setObjectName("rightsLabel_4")
        self.searchByEmailOrNameLabel_3 = QtWidgets.QLabel(parent=self.addSmthBox_2)
        self.searchByEmailOrNameLabel_3.setGeometry(QtCore.QRect(40, 390, 161, 16))
        self.searchByEmailOrNameLabel_3.setObjectName("searchByEmailOrNameLabel_3")
        self.usAddGroupByName = QtWidgets.QLineEdit(parent=self.addSmthBox_2)
        self.usAddGroupByName.setGeometry(QtCore.QRect(200, 390, 191, 22))
        self.usAddGroupByName.setObjectName("usAddGroupByName")
        self.usAddSearchGroupButton = QtWidgets.QPushButton(parent=self.addSmthBox_2)
        self.usAddSearchGroupButton.setGeometry(QtCore.QRect(30, 420, 401, 41))
        self.usAddSearchGroupButton.setStyleSheet("QPushButton{\n"
                                                  " background-color: #081f2d; \n"
                                                  " border-radius: 8px; \n"
                                                  " border: 2px solid #081F2D; \n"
                                                  " color: white; \n"
                                                  " font-size: 15px;  \n"
                                                  " cursor: pointer; \n"
                                                  " transition: 0.3s; \n"
                                                  " }\n"
                                                  " \n"
                                                  "QPushButton:hover{ \n"
                                                  " background-color: white; \n"
                                                  " color: #081F2D; \n"
                                                  " border-color: #081F2D;\n"
                                                  " transition: 0.9s; \n"
                                                  "}")
        self.usAddSearchGroupButton.setObjectName("usAddSearchGroupButton")
        self.usAddRefreshGroupButton = QtWidgets.QPushButton(parent=self.addSmthBox_2)
        self.usAddRefreshGroupButton.setGeometry(QtCore.QRect(30, 470, 401, 41))
        self.usAddRefreshGroupButton.setStyleSheet("QPushButton{\n"
                                                   " background-color: #081f2d; \n"
                                                   " border-radius: 8px; \n"
                                                   " border: 2px solid #081F2D; \n"
                                                   " color: white; \n"
                                                   " font-size: 15px;  \n"
                                                   " cursor: pointer; \n"
                                                   " transition: 0.3s; \n"
                                                   " }\n"
                                                   " \n"
                                                   "QPushButton:hover{ \n"
                                                   " background-color: white; \n"
                                                   " color: #081F2D; \n"
                                                   " border-color: #081F2D;\n"
                                                   " transition: 0.9s; \n"
                                                   "}")
        self.usAddRefreshGroupButton.setObjectName("usAddRefreshGroupButton")
        self.usDelFromSelectedGr = QtWidgets.QPushButton(parent=self.addSmthBox_2)
        self.usDelFromSelectedGr.setGeometry(QtCore.QRect(660, 240, 61, 41))
        self.usDelFromSelectedGr.setStyleSheet("QPushButton{\n"
                                               " background-color: #081f2d; \n"
                                               " border-radius: 8px; \n"
                                               " border: 2px solid #081F2D; \n"
                                               " color: white; \n"
                                               " font-size: 15px;  \n"
                                               " cursor: pointer; \n"
                                               " transition: 0.3s; \n"
                                               " }\n"
                                               " \n"
                                               "QPushButton:hover{ \n"
                                               " background-color: white; \n"
                                               " color: #081F2D; \n"
                                               " border-color: #081F2D;\n"
                                               " transition: 0.9s; \n"
                                               "}")
        self.usDelFromSelectedGr.setObjectName("usDelFromSelectedGr")
        self.usGrToSelected = QtWidgets.QPushButton(parent=self.addSmthBox_2)
        self.usGrToSelected.setGeometry(QtCore.QRect(660, 290, 61, 41))
        self.usGrToSelected.setStyleSheet("QPushButton{\n"
                                          " background-color: #081f2d; \n"
                                          " border-radius: 8px; \n"
                                          " border: 2px solid #081F2D; \n"
                                          " color: white; \n"
                                          " font-size: 15px;  \n"
                                          " cursor: pointer; \n"
                                          " transition: 0.3s; \n"
                                          " }\n"
                                          " \n"
                                          "QPushButton:hover{ \n"
                                          " background-color: white; \n"
                                          " color: #081F2D; \n"
                                          " border-color: #081F2D;\n"
                                          " transition: 0.9s; \n"
                                          "}")
        self.usGrToSelected.setObjectName("usGrToSelected")
        self.usAddSelectedGrTableView = QtWidgets.QTableView(parent=self.addSmthBox_2)
        self.usAddSelectedGrTableView.setGeometry(QtCore.QRect(480, 30, 171, 441))
        self.usAddSelectedGrTableView.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.usAddSelectedGrTableView.setObjectName("usAddSelectedGrTableView")
        self.usAddAllGrTableView = QtWidgets.QTableView(parent=self.addSmthBox_2)
        self.usAddAllGrTableView.setGeometry(QtCore.QRect(730, 30, 431, 481))
        self.usAddAllGrTableView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.usAddAllGrTableView.setObjectName("usAddAllGrTableView")
        self.usAddUserOrInvButton = QtWidgets.QPushButton(parent=self.addSmthBox_2)
        self.usAddUserOrInvButton.setGeometry(QtCore.QRect(40, 330, 401, 41))
        self.usAddUserOrInvButton.setStyleSheet("QPushButton{\n"
                                                " background-color: #081f2d; \n"
                                                " border-radius: 8px; \n"
                                                " border: 2px solid #081F2D; \n"
                                                " color: white; \n"
                                                " font-size: 15px;  \n"
                                                " cursor: pointer; \n"
                                                " transition: 0.3s; \n"
                                                " }\n"
                                                " \n"
                                                "QPushButton:hover{ \n"
                                                " background-color: white; \n"
                                                " color: #081F2D; \n"
                                                " border-color: #081F2D;\n"
                                                " transition: 0.9s; \n"
                                                "}")
        self.usAddUserOrInvButton.setObjectName("usAddUserOrInvButton")
        self.usAddDeleteGroupsButton = QtWidgets.QPushButton(parent=self.addSmthBox_2)
        self.usAddDeleteGroupsButton.setGeometry(QtCore.QRect(480, 480, 171, 31))
        self.usAddDeleteGroupsButton.setStyleSheet("QPushButton{\n"
                                                   " background-color: #081f2d; \n"
                                                   " border-radius: 8px; \n"
                                                   " border: 2px solid #081F2D; \n"
                                                   " color: white; \n"
                                                   " font-size: 15px;  \n"
                                                   " cursor: pointer; \n"
                                                   " transition: 0.3s; \n"
                                                   " }\n"
                                                   " \n"
                                                   "QPushButton:hover{ \n"
                                                   " background-color: white; \n"
                                                   " color: #081F2D; \n"
                                                   " border-color: #081F2D;\n"
                                                   " transition: 0.9s; \n"
                                                   "}")
        self.usAddDeleteGroupsButton.setObjectName("usAddDeleteGroupsButton")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_16 = QtWidgets.QWidget()
        self.tab_16.setObjectName("tab_16")
        self.nameOrEmailLabel_8 = QtWidgets.QLabel(parent=self.tab_16)
        self.nameOrEmailLabel_8.setGeometry(QtCore.QRect(30, 30, 71, 16))
        self.nameOrEmailLabel_8.setObjectName("nameOrEmailLabel_8")
        self.grAddLineEdit = QtWidgets.QLineEdit(parent=self.tab_16)
        self.grAddLineEdit.setGeometry(QtCore.QRect(110, 30, 311, 22))
        self.grAddLineEdit.setObjectName("grAddLineEdit")
        self.grAddPushButton = QtWidgets.QPushButton(parent=self.tab_16)
        self.grAddPushButton.setGeometry(QtCore.QRect(20, 120, 401, 41))
        self.grAddPushButton.setStyleSheet("QPushButton{\n"
                                           " background-color: #081f2d; \n"
                                           " border-radius: 8px; \n"
                                           " border: 2px solid #081F2D; \n"
                                           " color: white; \n"
                                           " font-size: 15px;  \n"
                                           " cursor: pointer; \n"
                                           " transition: 0.3s; \n"
                                           " }\n"
                                           " \n"
                                           "QPushButton:hover{ \n"
                                           " background-color: white; \n"
                                           " color: #081F2D; \n"
                                           " border-color: #081F2D;\n"
                                           " transition: 0.9s; \n"
                                           "}")
        self.grAddPushButton.setObjectName("grAddPushButton")
        self.grTableView = QtWidgets.QTableView(parent=self.tab_16)
        self.grTableView.setGeometry(QtCore.QRect(490, 40, 611, 561))
        self.grTableView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.grTableView.setObjectName("grTableView")
        self.grSearchPushButton = QtWidgets.QPushButton(parent=self.tab_16)
        self.grSearchPushButton.setGeometry(QtCore.QRect(20, 170, 401, 41))
        self.grSearchPushButton.setStyleSheet("QPushButton{\n"
                                              " background-color: #081f2d; \n"
                                              " border-radius: 8px; \n"
                                              " border: 2px solid #081F2D; \n"
                                              " color: white; \n"
                                              " font-size: 15px;  \n"
                                              " cursor: pointer; \n"
                                              " transition: 0.3s; \n"
                                              " }\n"
                                              " \n"
                                              "QPushButton:hover{ \n"
                                              " background-color: white; \n"
                                              " color: #081F2D; \n"
                                              " border-color: #081F2D;\n"
                                              " transition: 0.9s; \n"
                                              "}")
        self.grSearchPushButton.setObjectName("grSearchPushButton")
        self.listLabel_13 = QtWidgets.QLabel(parent=self.tab_16)
        self.listLabel_13.setGeometry(QtCore.QRect(490, 10, 161, 20))
        self.listLabel_13.setObjectName("listLabel_13")
        self.grRefreshPushButton = QtWidgets.QPushButton(parent=self.tab_16)
        self.grRefreshPushButton.setGeometry(QtCore.QRect(20, 220, 401, 41))
        self.grRefreshPushButton.setStyleSheet("QPushButton{\n"
                                               " background-color: #081f2d; \n"
                                               " border-radius: 8px; \n"
                                               " border: 2px solid #081F2D; \n"
                                               " color: white; \n"
                                               " font-size: 15px;  \n"
                                               " cursor: pointer; \n"
                                               " transition: 0.3s; \n"
                                               " }\n"
                                               " \n"
                                               "QPushButton:hover{ \n"
                                               " background-color: white; \n"
                                               " color: #081F2D; \n"
                                               " border-color: #081F2D;\n"
                                               " transition: 0.9s; \n"
                                               "}")
        self.grRefreshPushButton.setObjectName("grRefreshPushButton")
        self.grDeletePushButton = QtWidgets.QPushButton(parent=self.tab_16)
        self.grDeletePushButton.setGeometry(QtCore.QRect(20, 70, 401, 41))
        self.grDeletePushButton.setStyleSheet("QPushButton{\n"
                                              " background-color: #081f2d; \n"
                                              " border-radius: 8px; \n"
                                              " border: 2px solid #081F2D; \n"
                                              " color: white; \n"
                                              " font-size: 15px;  \n"
                                              " cursor: pointer; \n"
                                              " transition: 0.3s; \n"
                                              " }\n"
                                              " \n"
                                              "QPushButton:hover{ \n"
                                              " background-color: white; \n"
                                              " color: #081F2D; \n"
                                              " border-color: #081F2D;\n"
                                              " transition: 0.9s; \n"
                                              "}")
        self.grDeletePushButton.setObjectName("grDeletePushButton")
        self.grPrevPushButton = QtWidgets.QPushButton(parent=self.tab_16)
        self.grPrevPushButton.setGeometry(QtCore.QRect(450, 70, 31, 51))
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.grPrevPushButton.setFont(font)
        self.grPrevPushButton.setStyleSheet("QPushButton{\n"
                                            " background-color: #081f2d; \n"
                                            " border-radius: 8px; \n"
                                            " border: 2px solid #081F2D; \n"
                                            " color: white; \n"
                                            " font-size: 15px;  \n"
                                            " cursor: pointer; \n"
                                            " transition: 0.3s; \n"
                                            " }\n"
                                            " \n"
                                            "QPushButton:hover{ \n"
                                            " background-color: white; \n"
                                            " color: #081F2D; \n"
                                            " border-color: #081F2D;\n"
                                            " transition: 0.9s; \n"
                                            "}")
        self.grPrevPushButton.setObjectName("grPrevPushButton")
        self.grNextPushButton = QtWidgets.QPushButton(parent=self.tab_16)
        self.grNextPushButton.setGeometry(QtCore.QRect(450, 140, 31, 51))
        self.grNextPushButton.setStyleSheet("QPushButton{\n"
                                            " background-color: #081f2d; \n"
                                            " border-radius: 8px; \n"
                                            " border: 2px solid #081F2D; \n"
                                            " color: white; \n"
                                            " font-size: 15px;  \n"
                                            " cursor: pointer; \n"
                                            " transition: 0.3s; \n"
                                            " }\n"
                                            " \n"
                                            "QPushButton:hover{ \n"
                                            " background-color: white; \n"
                                            " color: #081F2D; \n"
                                            " border-color: #081F2D;\n"
                                            " transition: 0.9s; \n"
                                            "}")
        self.grNextPushButton.setObjectName("grNextPushButton")
        self.tabWidget.addTab(self.tab_16, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.viewInvOrUserBox_2 = QtWidgets.QGroupBox(parent=self.tab_4)
        self.viewInvOrUserBox_2.setGeometry(QtCore.QRect(10, 10, 1641, 761))
        self.viewInvOrUserBox_2.setStyleSheet("QGroupBox#viewInvOrUserBox_2{\n"
                                              "    border: 0;\n"
                                              "}")
        self.viewInvOrUserBox_2.setTitle("")
        self.viewInvOrUserBox_2.setObjectName("viewInvOrUserBox_2")
        self.searchByIdLabel_2 = QtWidgets.QLabel(parent=self.viewInvOrUserBox_2)
        self.searchByIdLabel_2.setGeometry(QtCore.QRect(10, 30, 141, 16))
        self.searchByIdLabel_2.setObjectName("searchByIdLabel_2")
        self.searchByEmailOrNameLabel_2 = QtWidgets.QLabel(parent=self.viewInvOrUserBox_2)
        self.searchByEmailOrNameLabel_2.setGeometry(QtCore.QRect(10, 60, 71, 16))
        self.searchByEmailOrNameLabel_2.setObjectName("searchByEmailOrNameLabel_2")
        self.ussearchByEmailOrNameLineEdit = QtWidgets.QLineEdit(parent=self.viewInvOrUserBox_2)
        self.ussearchByEmailOrNameLineEdit.setGeometry(QtCore.QRect(80, 60, 351, 22))
        self.ussearchByEmailOrNameLineEdit.setObjectName("ussearchByEmailOrNameLineEdit")
        self.usTableView = QtWidgets.QTableView(parent=self.viewInvOrUserBox_2)
        self.usTableView.setGeometry(QtCore.QRect(870, 30, 701, 721))
        self.usTableView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.usTableView.setObjectName("usTableView")
        self.ussearchByNameOrEmailLineEdit = QtWidgets.QLineEdit(parent=self.viewInvOrUserBox_2)
        self.ussearchByNameOrEmailLineEdit.setGeometry(QtCore.QRect(170, 30, 261, 22))
        self.ussearchByNameOrEmailLineEdit.setObjectName("ussearchByNameOrEmailLineEdit")
        self.ussearchPushButton = QtWidgets.QPushButton(parent=self.viewInvOrUserBox_2)
        self.ussearchPushButton.setGeometry(QtCore.QRect(20, 390, 351, 28))
        self.ussearchPushButton.setStyleSheet("QPushButton{\n"
                                              " background-color: #081f2d; \n"
                                              " border-radius: 8px; \n"
                                              " border: 2px solid #081F2D; \n"
                                              " color: white; \n"
                                              " font-size: 15px;  \n"
                                              " cursor: pointer; \n"
                                              " transition: 0.3s; \n"
                                              " }\n"
                                              " \n"
                                              "QPushButton:hover{ \n"
                                              " background-color: white; \n"
                                              " color: #081F2D; \n"
                                              " border-color: #081F2D;\n"
                                              " transition: 0.9s; \n"
                                              "}")
        self.ussearchPushButton.setObjectName("ussearchPushButton")
        self.usViewRefreshPushButton = QtWidgets.QPushButton(parent=self.viewInvOrUserBox_2)
        self.usViewRefreshPushButton.setGeometry(QtCore.QRect(20, 430, 351, 28))
        self.usViewRefreshPushButton.setStyleSheet("QPushButton{\n"
                                                   " background-color: #081f2d; \n"
                                                   " border-radius: 8px; \n"
                                                   " border: 2px solid #081F2D; \n"
                                                   " color: white; \n"
                                                   " font-size: 15px;  \n"
                                                   " cursor: pointer; \n"
                                                   " transition: 0.3s; \n"
                                                   " }\n"
                                                   " \n"
                                                   "QPushButton:hover{ \n"
                                                   " background-color: white; \n"
                                                   " color: #081F2D; \n"
                                                   " border-color: #081F2D;\n"
                                                   " transition: 0.9s; \n"
                                                   "}")
        self.usViewRefreshPushButton.setObjectName("usViewRefreshPushButton")
        self.uschangerGroupBox = QtWidgets.QGroupBox(parent=self.viewInvOrUserBox_2)
        self.uschangerGroupBox.setGeometry(QtCore.QRect(10, 130, 371, 131))
        self.uschangerGroupBox.setTitle("")
        self.uschangerGroupBox.setObjectName("uschangerGroupBox")
        self.uschangernextPushButton = QtWidgets.QPushButton(parent=self.uschangerGroupBox)
        self.uschangernextPushButton.setGeometry(QtCore.QRect(10, 10, 121, 31))
        self.uschangernextPushButton.setStyleSheet("QPushButton{\n"
                                                   " background-color: #081f2d; \n"
                                                   " border-radius: 8px; \n"
                                                   " border: 2px solid #081F2D; \n"
                                                   " color: white; \n"
                                                   " font-size: 15px;  \n"
                                                   " cursor: pointer; \n"
                                                   " transition: 0.3s; \n"
                                                   " }\n"
                                                   " \n"
                                                   "QPushButton:hover{ \n"
                                                   " background-color: white; \n"
                                                   " color: #081F2D; \n"
                                                   " border-color: #081F2D;\n"
                                                   " transition: 0.9s; \n"
                                                   "}")
        self.uschangernextPushButton.setObjectName("uschangernextPushButton")
        self.uschangerprevPushButton = QtWidgets.QPushButton(parent=self.uschangerGroupBox)
        self.uschangerprevPushButton.setGeometry(QtCore.QRect(10, 50, 121, 31))
        self.uschangerprevPushButton.setStyleSheet("QPushButton{\n"
                                                   " background-color: #081f2d; \n"
                                                   " border-radius: 8px; \n"
                                                   " border: 2px solid #081F2D; \n"
                                                   " color: white; \n"
                                                   " font-size: 15px;  \n"
                                                   " cursor: pointer; \n"
                                                   " transition: 0.3s; \n"
                                                   " }\n"
                                                   " \n"
                                                   "QPushButton:hover{ \n"
                                                   " background-color: white; \n"
                                                   " color: #081F2D; \n"
                                                   " border-color: #081F2D;\n"
                                                   " transition: 0.9s; \n"
                                                   "}")
        self.uschangerprevPushButton.setObjectName("uschangerprevPushButton")
        self.uscommitchangesPushButton = QtWidgets.QPushButton(parent=self.uschangerGroupBox)
        self.uscommitchangesPushButton.setGeometry(QtCore.QRect(150, 10, 211, 71))
        self.uscommitchangesPushButton.setStyleSheet("QPushButton{\n"
                                                     " background-color: #081f2d; \n"
                                                     " border-radius: 8px; \n"
                                                     " border: 2px solid #081F2D; \n"
                                                     " color: white; \n"
                                                     " font-size: 15px;  \n"
                                                     " cursor: pointer; \n"
                                                     " transition: 0.3s; \n"
                                                     " }\n"
                                                     " \n"
                                                     "QPushButton:hover{ \n"
                                                     " background-color: white; \n"
                                                     " color: #081F2D; \n"
                                                     " border-color: #081F2D;\n"
                                                     " transition: 0.9s; \n"
                                                     "}")
        self.uscommitchangesPushButton.setObjectName("uscommitchangesPushButton")
        self.usChangeDelPushButton = QtWidgets.QPushButton(parent=self.uschangerGroupBox)
        self.usChangeDelPushButton.setGeometry(QtCore.QRect(10, 90, 351, 31))
        self.usChangeDelPushButton.setStyleSheet("QPushButton{\n"
                                                 " background-color: #081f2d; \n"
                                                 " border-radius: 8px; \n"
                                                 " border: 2px solid #081F2D; \n"
                                                 " color: white; \n"
                                                 " font-size: 15px;  \n"
                                                 " cursor: pointer; \n"
                                                 " transition: 0.3s; \n"
                                                 " }\n"
                                                 " \n"
                                                 "QPushButton:hover{ \n"
                                                 " background-color: white; \n"
                                                 " color: #081F2D; \n"
                                                 " border-color: #081F2D;\n"
                                                 " transition: 0.9s; \n"
                                                 "}")
        self.usChangeDelPushButton.setObjectName("usChangeDelPushButton")
        self.usGroupsTableView = QtWidgets.QTableView(parent=self.viewInvOrUserBox_2)
        self.usGroupsTableView.setGeometry(QtCore.QRect(440, 30, 171, 481))
        self.usGroupsTableView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.usGroupsTableView.setObjectName("usGroupsTableView")
        self.listLabel_4 = QtWidgets.QLabel(parent=self.viewInvOrUserBox_2)
        self.listLabel_4.setGeometry(QtCore.QRect(440, 10, 161, 20))
        self.listLabel_4.setObjectName("listLabel_4")
        self.eqCreateStatsSpinBox_2 = QtWidgets.QSpinBox(parent=self.viewInvOrUserBox_2)
        self.eqCreateStatsSpinBox_2.setGeometry(QtCore.QRect(270, 330, 111, 22))
        self.eqCreateStatsSpinBox_2.setObjectName("eqCreateStatsSpinBox_2")
        self.label_43 = QtWidgets.QLabel(parent=self.viewInvOrUserBox_2)
        self.label_43.setGeometry(QtCore.QRect(260, 310, 141, 16))
        self.label_43.setObjectName("label_43")
        self.eqCreateStatsPushButton_2 = QtWidgets.QPushButton(parent=self.viewInvOrUserBox_2)
        self.eqCreateStatsPushButton_2.setGeometry(QtCore.QRect(20, 330, 231, 28))
        self.eqCreateStatsPushButton_2.setStyleSheet("QPushButton{\n"
                                                     " background-color: #081f2d; \n"
                                                     " border-radius: 8px; \n"
                                                     " border: 2px solid #081F2D; \n"
                                                     " color: white; \n"
                                                     " font-size: 15px;  \n"
                                                     " cursor: pointer; \n"
                                                     " transition: 0.3s; \n"
                                                     " }\n"
                                                     " \n"
                                                     "QPushButton:hover{ \n"
                                                     " background-color: white; \n"
                                                     " color: #081F2D; \n"
                                                     " border-color: #081F2D;\n"
                                                     " transition: 0.9s; \n"
                                                     "}")
        self.eqCreateStatsPushButton_2.setObjectName("eqCreateStatsPushButton_2")
        self.listLabel_2 = QtWidgets.QLabel(parent=self.viewInvOrUserBox_2)
        self.listLabel_2.setGeometry(QtCore.QRect(870, 10, 351, 16))
        self.listLabel_2.setObjectName("listLabel_2")
        self.usSearchGrToSelected = QtWidgets.QPushButton(parent=self.viewInvOrUserBox_2)
        self.usSearchGrToSelected.setGeometry(QtCore.QRect(620, 390, 61, 41))
        self.usSearchGrToSelected.setStyleSheet("QPushButton{\n"
                                                " background-color: #081f2d; \n"
                                                " border-radius: 8px; \n"
                                                " border: 2px solid #081F2D; \n"
                                                " color: white; \n"
                                                " font-size: 15px;  \n"
                                                " cursor: pointer; \n"
                                                " transition: 0.3s; \n"
                                                " }\n"
                                                " \n"
                                                "QPushButton:hover{ \n"
                                                " background-color: white; \n"
                                                " color: #081F2D; \n"
                                                " border-color: #081F2D;\n"
                                                " transition: 0.9s; \n"
                                                "}")
        self.usSearchGrToSelected.setObjectName("usSearchGrToSelected")
        self.usSearchDelFromSelectedGr = QtWidgets.QPushButton(parent=self.viewInvOrUserBox_2)
        self.usSearchDelFromSelectedGr.setGeometry(QtCore.QRect(620, 340, 61, 41))
        self.usSearchDelFromSelectedGr.setStyleSheet("QPushButton{\n"
                                                     " background-color: #081f2d; \n"
                                                     " border-radius: 8px; \n"
                                                     " border: 2px solid #081F2D; \n"
                                                     " color: white; \n"
                                                     " font-size: 15px;  \n"
                                                     " cursor: pointer; \n"
                                                     " transition: 0.3s; \n"
                                                     " }\n"
                                                     " \n"
                                                     "QPushButton:hover{ \n"
                                                     " background-color: white; \n"
                                                     " color: #081F2D; \n"
                                                     " border-color: #081F2D;\n"
                                                     " transition: 0.9s; \n"
                                                     "}")
        self.usSearchDelFromSelectedGr.setObjectName("usSearchDelFromSelectedGr")
        self.usSearchAllGrTableView = QtWidgets.QTableView(parent=self.viewInvOrUserBox_2)
        self.usSearchAllGrTableView.setGeometry(QtCore.QRect(690, 30, 161, 521))
        self.usSearchAllGrTableView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.usSearchAllGrTableView.setObjectName("usSearchAllGrTableView")
        self.listLabel_19 = QtWidgets.QLabel(parent=self.viewInvOrUserBox_2)
        self.listLabel_19.setGeometry(QtCore.QRect(690, 10, 161, 20))
        self.listLabel_19.setObjectName("listLabel_19")
        self.usChangeSearchGroupsGroupBox = QtWidgets.QGroupBox(parent=self.viewInvOrUserBox_2)
        self.usChangeSearchGroupsGroupBox.setGeometry(QtCore.QRect(660, 570, 201, 161))
        self.usChangeSearchGroupsGroupBox.setTitle("")
        self.usChangeSearchGroupsGroupBox.setObjectName("usChangeSearchGroupsGroupBox")
        self.usChangeRefreshGroupButton = QtWidgets.QPushButton(parent=self.usChangeSearchGroupsGroupBox)
        self.usChangeRefreshGroupButton.setGeometry(QtCore.QRect(10, 110, 181, 41))
        self.usChangeRefreshGroupButton.setStyleSheet("QPushButton{\n"
                                                      " background-color: #081f2d; \n"
                                                      " border-radius: 8px; \n"
                                                      " border: 2px solid #081F2D; \n"
                                                      " color: white; \n"
                                                      " font-size: 15px;  \n"
                                                      " cursor: pointer; \n"
                                                      " transition: 0.3s; \n"
                                                      " }\n"
                                                      " \n"
                                                      "QPushButton:hover{ \n"
                                                      " background-color: white; \n"
                                                      " color: #081F2D; \n"
                                                      " border-color: #081F2D;\n"
                                                      " transition: 0.9s; \n"
                                                      "}")
        self.usChangeRefreshGroupButton.setObjectName("usChangeRefreshGroupButton")
        self.usChangeSearchGroupButton = QtWidgets.QPushButton(parent=self.usChangeSearchGroupsGroupBox)
        self.usChangeSearchGroupButton.setGeometry(QtCore.QRect(10, 60, 121, 41))
        self.usChangeSearchGroupButton.setStyleSheet("QPushButton{\n"
                                                     " background-color: #081f2d; \n"
                                                     " border-radius: 8px; \n"
                                                     " border: 2px solid #081F2D; \n"
                                                     " color: white; \n"
                                                     " font-size: 15px;  \n"
                                                     " cursor: pointer; \n"
                                                     " transition: 0.3s; \n"
                                                     " }\n"
                                                     " \n"
                                                     "QPushButton:hover{ \n"
                                                     " background-color: white; \n"
                                                     " color: #081F2D; \n"
                                                     " border-color: #081F2D;\n"
                                                     " transition: 0.9s; \n"
                                                     "}")
        self.usChangeSearchGroupButton.setObjectName("usChangeSearchGroupButton")
        self.usChangeGroupByName = QtWidgets.QLineEdit(parent=self.usChangeSearchGroupsGroupBox)
        self.usChangeGroupByName.setGeometry(QtCore.QRect(0, 30, 191, 22))
        self.usChangeGroupByName.setObjectName("usChangeGroupByName")
        self.searchByEmailOrNameLabel_10 = QtWidgets.QLabel(parent=self.usChangeSearchGroupsGroupBox)
        self.searchByEmailOrNameLabel_10.setGeometry(QtCore.QRect(30, 10, 161, 16))
        self.searchByEmailOrNameLabel_10.setObjectName("searchByEmailOrNameLabel_10")
        self.eqsearchByIdLabel_19 = QtWidgets.QLabel(parent=self.viewInvOrUserBox_2)
        self.eqsearchByIdLabel_19.setGeometry(QtCore.QRect(10, 90, 131, 21))
        self.eqsearchByIdLabel_19.setObjectName("eqsearchByIdLabel_19")
        self.ussearchByGroupLineEdit = QtWidgets.QLineEdit(parent=self.viewInvOrUserBox_2)
        self.ussearchByGroupLineEdit.setGeometry(QtCore.QRect(150, 90, 281, 22))
        self.ussearchByGroupLineEdit.setObjectName("ussearchByGroupLineEdit")
        self.usChangeDeleteGroupsButton = QtWidgets.QPushButton(parent=self.viewInvOrUserBox_2)
        self.usChangeDeleteGroupsButton.setGeometry(QtCore.QRect(440, 520, 171, 31))
        self.usChangeDeleteGroupsButton.setStyleSheet("QPushButton{\n"
                                                      " background-color: #081f2d; \n"
                                                      " border-radius: 8px; \n"
                                                      " border: 2px solid #081F2D; \n"
                                                      " color: white; \n"
                                                      " font-size: 15px;  \n"
                                                      " cursor: pointer; \n"
                                                      " transition: 0.3s; \n"
                                                      " }\n"
                                                      " \n"
                                                      "QPushButton:hover{ \n"
                                                      " background-color: white; \n"
                                                      " color: #081F2D; \n"
                                                      " border-color: #081F2D;\n"
                                                      " transition: 0.9s; \n"
                                                      "}")
        self.usChangeDeleteGroupsButton.setObjectName("usChangeDeleteGroupsButton")
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.viewInvOrUserBox = QtWidgets.QGroupBox(parent=self.tab_3)
        self.viewInvOrUserBox.setGeometry(QtCore.QRect(0, 0, 1771, 781))
        self.viewInvOrUserBox.setStyleSheet("QGroupBox#viewInvOrUserBox{\n"
                                            "    border: 0;\n"
                                            "}")
        self.viewInvOrUserBox.setTitle("")
        self.viewInvOrUserBox.setObjectName("viewInvOrUserBox")
        self.eqsearchByIdLabel = QtWidgets.QLabel(parent=self.viewInvOrUserBox)
        self.eqsearchByIdLabel.setGeometry(QtCore.QRect(10, 30, 21, 16))
        self.eqsearchByIdLabel.setObjectName("eqsearchByIdLabel")
        self.searchByEmailOrNameLabel = QtWidgets.QLabel(parent=self.viewInvOrUserBox)
        self.searchByEmailOrNameLabel.setGeometry(QtCore.QRect(10, 60, 81, 16))
        self.searchByEmailOrNameLabel.setObjectName("searchByEmailOrNameLabel")
        self.eqsearchByIdSpinBox = QtWidgets.QSpinBox(parent=self.viewInvOrUserBox)
        self.eqsearchByIdSpinBox.setGeometry(QtCore.QRect(30, 30, 291, 22))
        self.eqsearchByIdSpinBox.setObjectName("eqsearchByIdSpinBox")
        self.eqsearchByEmailOrNameLineEdit = QtWidgets.QLineEdit(parent=self.viewInvOrUserBox)
        self.eqsearchByEmailOrNameLineEdit.setGeometry(QtCore.QRect(90, 60, 231, 22))
        self.eqsearchByEmailOrNameLineEdit.setObjectName("eqsearchByEmailOrNameLineEdit")
        self.listLabel = QtWidgets.QLabel(parent=self.viewInvOrUserBox)
        self.listLabel.setGeometry(QtCore.QRect(840, 20, 351, 16))
        self.listLabel.setObjectName("listLabel")
        self.searchByPosGroupBox = QtWidgets.QGroupBox(parent=self.viewInvOrUserBox)
        self.searchByPosGroupBox.setGeometry(QtCore.QRect(0, 190, 451, 61))
        self.searchByPosGroupBox.setStyleSheet("QGroupBox#searchByPosGroupBox{\n"
                                               "    border: 0;\n"
                                               "}")
        self.searchByPosGroupBox.setObjectName("searchByPosGroupBox")
        self.label_36 = QtWidgets.QLabel(parent=self.searchByPosGroupBox)
        self.label_36.setGeometry(QtCore.QRect(10, 30, 101, 16))
        self.label_36.setObjectName("label_36")
        self.label_37 = QtWidgets.QLabel(parent=self.searchByPosGroupBox)
        self.label_37.setGeometry(QtCore.QRect(190, 30, 161, 16))
        self.label_37.setObjectName("label_37")
        self.searchByHeightSpinBox = QtWidgets.QSpinBox(parent=self.searchByPosGroupBox)
        self.searchByHeightSpinBox.setGeometry(QtCore.QRect(120, 30, 61, 22))
        self.searchByHeightSpinBox.setObjectName("searchByHeightSpinBox")
        self.searchByPosFromLeftSpinBox = QtWidgets.QSpinBox(parent=self.searchByPosGroupBox)
        self.searchByPosFromLeftSpinBox.setGeometry(QtCore.QRect(350, 30, 61, 22))
        self.searchByPosFromLeftSpinBox.setObjectName("searchByPosFromLeftSpinBox")
        self.eqsearchPushButton = QtWidgets.QPushButton(parent=self.viewInvOrUserBox)
        self.eqsearchPushButton.setGeometry(QtCore.QRect(30, 380, 351, 28))
        self.eqsearchPushButton.setStyleSheet("QPushButton{\n"
                                              " background-color: #081f2d; \n"
                                              " border-radius: 8px; \n"
                                              " border: 2px solid #081F2D; \n"
                                              " color: white; \n"
                                              " font-size: 15px;  \n"
                                              " cursor: pointer; \n"
                                              " transition: 0.3s; \n"
                                              " }\n"
                                              " \n"
                                              "QPushButton:hover{ \n"
                                              " background-color: white; \n"
                                              " color: #081F2D; \n"
                                              " border-color: #081F2D;\n"
                                              " transition: 0.9s; \n"
                                              "}")
        self.eqsearchPushButton.setObjectName("eqsearchPushButton")
        self.eqTableView = QtWidgets.QTableView(parent=self.viewInvOrUserBox)
        self.eqTableView.setGeometry(QtCore.QRect(840, 40, 781, 721))
        self.eqTableView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.eqTableView.setObjectName("eqTableView")
        self.eqchangerGroupBox = QtWidgets.QGroupBox(parent=self.viewInvOrUserBox)
        self.eqchangerGroupBox.setGeometry(QtCore.QRect(20, 450, 371, 131))
        self.eqchangerGroupBox.setTitle("")
        self.eqchangerGroupBox.setObjectName("eqchangerGroupBox")
        self.eqchangernextPushButton = QtWidgets.QPushButton(parent=self.eqchangerGroupBox)
        self.eqchangernextPushButton.setGeometry(QtCore.QRect(10, 10, 121, 31))
        self.eqchangernextPushButton.setStyleSheet("QPushButton{\n"
                                                   " background-color: #081f2d; \n"
                                                   " border-radius: 8px; \n"
                                                   " border: 2px solid #081F2D; \n"
                                                   " color: white; \n"
                                                   " font-size: 15px;  \n"
                                                   " cursor: pointer; \n"
                                                   " transition: 0.3s; \n"
                                                   " }\n"
                                                   " \n"
                                                   "QPushButton:hover{ \n"
                                                   " background-color: white; \n"
                                                   " color: #081F2D; \n"
                                                   " border-color: #081F2D;\n"
                                                   " transition: 0.9s; \n"
                                                   "}")
        self.eqchangernextPushButton.setObjectName("eqchangernextPushButton")
        self.eqchangerprevPushButton = QtWidgets.QPushButton(parent=self.eqchangerGroupBox)
        self.eqchangerprevPushButton.setGeometry(QtCore.QRect(10, 50, 121, 31))
        self.eqchangerprevPushButton.setStyleSheet("QPushButton{\n"
                                                   " background-color: #081f2d; \n"
                                                   " border-radius: 8px; \n"
                                                   " border: 2px solid #081F2D; \n"
                                                   " color: white; \n"
                                                   " font-size: 15px;  \n"
                                                   " cursor: pointer; \n"
                                                   " transition: 0.3s; \n"
                                                   " }\n"
                                                   " \n"
                                                   "QPushButton:hover{ \n"
                                                   " background-color: white; \n"
                                                   " color: #081F2D; \n"
                                                   " border-color: #081F2D;\n"
                                                   " transition: 0.9s; \n"
                                                   "}")
        self.eqchangerprevPushButton.setObjectName("eqchangerprevPushButton")
        self.eqcommitchangesPushButton = QtWidgets.QPushButton(parent=self.eqchangerGroupBox)
        self.eqcommitchangesPushButton.setGeometry(QtCore.QRect(150, 10, 211, 71))
        self.eqcommitchangesPushButton.setStyleSheet("QPushButton{\n"
                                                     " background-color: #081f2d; \n"
                                                     " border-radius: 8px; \n"
                                                     " border: 2px solid #081F2D; \n"
                                                     " color: white; \n"
                                                     " font-size: 15px;  \n"
                                                     " cursor: pointer; \n"
                                                     " transition: 0.3s; \n"
                                                     " }\n"
                                                     " \n"
                                                     "QPushButton:hover{ \n"
                                                     " background-color: white; \n"
                                                     " color: #081F2D; \n"
                                                     " border-color: #081F2D;\n"
                                                     " transition: 0.9s; \n"
                                                     "}")
        self.eqcommitchangesPushButton.setObjectName("eqcommitchangesPushButton")
        self.eqChangeDelPushButton = QtWidgets.QPushButton(parent=self.eqchangerGroupBox)
        self.eqChangeDelPushButton.setGeometry(QtCore.QRect(10, 90, 351, 31))
        self.eqChangeDelPushButton.setStyleSheet("QPushButton{\n"
                                                 " background-color: #081f2d; \n"
                                                 " border-radius: 8px; \n"
                                                 " border: 2px solid #081F2D; \n"
                                                 " color: white; \n"
                                                 " font-size: 15px;  \n"
                                                 " cursor: pointer; \n"
                                                 " transition: 0.3s; \n"
                                                 " }\n"
                                                 " \n"
                                                 "QPushButton:hover{ \n"
                                                 " background-color: white; \n"
                                                 " color: #081F2D; \n"
                                                 " border-color: #081F2D;\n"
                                                 " transition: 0.9s; \n"
                                                 "}")
        self.eqChangeDelPushButton.setObjectName("eqChangeDelPushButton")
        self.eqsearchByNumberSpinBox = QtWidgets.QSpinBox(parent=self.viewInvOrUserBox)
        self.eqsearchByNumberSpinBox.setGeometry(QtCore.QRect(110, 130, 211, 22))
        self.eqsearchByNumberSpinBox.setObjectName("eqsearchByNumberSpinBox")
        self.eqsearchByIdLabel_2 = QtWidgets.QLabel(parent=self.viewInvOrUserBox)
        self.eqsearchByIdLabel_2.setGeometry(QtCore.QRect(10, 130, 81, 16))
        self.eqsearchByIdLabel_2.setObjectName("eqsearchByIdLabel_2")
        self.eqsearchByReservedSpinBox = QtWidgets.QSpinBox(parent=self.viewInvOrUserBox)
        self.eqsearchByReservedSpinBox.setGeometry(QtCore.QRect(160, 160, 161, 22))
        self.eqsearchByReservedSpinBox.setObjectName("eqsearchByReservedSpinBox")
        self.eqsearchByIdLabel_3 = QtWidgets.QLabel(parent=self.viewInvOrUserBox)
        self.eqsearchByIdLabel_3.setGeometry(QtCore.QRect(10, 160, 131, 16))
        self.eqsearchByIdLabel_3.setObjectName("eqsearchByIdLabel_3")
        self.eqGroupsTableView = QtWidgets.QTableView(parent=self.viewInvOrUserBox)
        self.eqGroupsTableView.setGeometry(QtCore.QRect(420, 40, 171, 501))
        self.eqGroupsTableView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.eqGroupsTableView.setObjectName("eqGroupsTableView")
        self.listLabel_3 = QtWidgets.QLabel(parent=self.viewInvOrUserBox)
        self.listLabel_3.setGeometry(QtCore.QRect(420, 20, 161, 20))
        self.listLabel_3.setObjectName("listLabel_3")
        self.eqsearchByIdLabel_18 = QtWidgets.QLabel(parent=self.viewInvOrUserBox)
        self.eqsearchByIdLabel_18.setGeometry(QtCore.QRect(10, 90, 131, 21))
        self.eqsearchByIdLabel_18.setObjectName("eqsearchByIdLabel_18")
        self.eqCreateStatsPushButton = QtWidgets.QPushButton(parent=self.viewInvOrUserBox)
        self.eqCreateStatsPushButton.setGeometry(QtCore.QRect(20, 680, 231, 28))
        self.eqCreateStatsPushButton.setStyleSheet("QPushButton{\n"
                                                   " background-color: #081f2d; \n"
                                                   " border-radius: 8px; \n"
                                                   " border: 2px solid #081F2D; \n"
                                                   " color: white; \n"
                                                   " font-size: 15px;  \n"
                                                   " cursor: pointer; \n"
                                                   " transition: 0.3s; \n"
                                                   " }\n"
                                                   " \n"
                                                   "QPushButton:hover{ \n"
                                                   " background-color: white; \n"
                                                   " color: #081F2D; \n"
                                                   " border-color: #081F2D;\n"
                                                   " transition: 0.9s; \n"
                                                   "}")
        self.eqCreateStatsPushButton.setObjectName("eqCreateStatsPushButton")
        self.eqCreateStatsSpinBox = QtWidgets.QSpinBox(parent=self.viewInvOrUserBox)
        self.eqCreateStatsSpinBox.setGeometry(QtCore.QRect(270, 680, 111, 22))
        self.eqCreateStatsSpinBox.setObjectName("eqCreateStatsSpinBox")
        self.label_42 = QtWidgets.QLabel(parent=self.viewInvOrUserBox)
        self.label_42.setGeometry(QtCore.QRect(260, 660, 141, 16))
        self.label_42.setObjectName("label_42")
        self.eqSearchDelFromSelectedGr = QtWidgets.QPushButton(parent=self.viewInvOrUserBox)
        self.eqSearchDelFromSelectedGr.setGeometry(QtCore.QRect(600, 350, 61, 41))
        self.eqSearchDelFromSelectedGr.setStyleSheet("QPushButton{\n"
                                                     " background-color: #081f2d; \n"
                                                     " border-radius: 8px; \n"
                                                     " border: 2px solid #081F2D; \n"
                                                     " color: white; \n"
                                                     " font-size: 15px;  \n"
                                                     " cursor: pointer; \n"
                                                     " transition: 0.3s; \n"
                                                     " }\n"
                                                     " \n"
                                                     "QPushButton:hover{ \n"
                                                     " background-color: white; \n"
                                                     " color: #081F2D; \n"
                                                     " border-color: #081F2D;\n"
                                                     " transition: 0.9s; \n"
                                                     "}")
        self.eqSearchDelFromSelectedGr.setObjectName("eqSearchDelFromSelectedGr")
        self.eqSearchAllGrTableView = QtWidgets.QTableView(parent=self.viewInvOrUserBox)
        self.eqSearchAllGrTableView.setGeometry(QtCore.QRect(670, 40, 161, 541))
        self.eqSearchAllGrTableView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.eqSearchAllGrTableView.setObjectName("eqSearchAllGrTableView")
        self.eqSearchGrToSelected = QtWidgets.QPushButton(parent=self.viewInvOrUserBox)
        self.eqSearchGrToSelected.setGeometry(QtCore.QRect(600, 400, 61, 41))
        self.eqSearchGrToSelected.setStyleSheet("QPushButton{\n"
                                                " background-color: #081f2d; \n"
                                                " border-radius: 8px; \n"
                                                " border: 2px solid #081F2D; \n"
                                                " color: white; \n"
                                                " font-size: 15px;  \n"
                                                " cursor: pointer; \n"
                                                " transition: 0.3s; \n"
                                                " }\n"
                                                " \n"
                                                "QPushButton:hover{ \n"
                                                " background-color: white; \n"
                                                " color: #081F2D; \n"
                                                " border-color: #081F2D;\n"
                                                " transition: 0.9s; \n"
                                                "}")
        self.eqSearchGrToSelected.setObjectName("eqSearchGrToSelected")
        self.listLabel_20 = QtWidgets.QLabel(parent=self.viewInvOrUserBox)
        self.listLabel_20.setGeometry(QtCore.QRect(670, 20, 161, 20))
        self.listLabel_20.setObjectName("listLabel_20")
        self.eqsearchByEmailOrNameLineEdit_2 = QtWidgets.QLineEdit(parent=self.viewInvOrUserBox)
        self.eqsearchByEmailOrNameLineEdit_2.setGeometry(QtCore.QRect(100, 250, 251, 111))
        self.eqsearchByEmailOrNameLineEdit_2.setObjectName("eqsearchByEmailOrNameLineEdit_2")
        self.searchByEmailOrNameLabel_8 = QtWidgets.QLabel(parent=self.viewInvOrUserBox)
        self.searchByEmailOrNameLabel_8.setGeometry(QtCore.QRect(10, 250, 81, 16))
        self.searchByEmailOrNameLabel_8.setObjectName("searchByEmailOrNameLabel_8")
        self.eqChangeSearchGroupsGroupBox = QtWidgets.QGroupBox(parent=self.viewInvOrUserBox)
        self.eqChangeSearchGroupsGroupBox.setGeometry(QtCore.QRect(640, 590, 201, 161))
        self.eqChangeSearchGroupsGroupBox.setTitle("")
        self.eqChangeSearchGroupsGroupBox.setObjectName("eqChangeSearchGroupsGroupBox")
        self.eqChangeRefreshGroupButton = QtWidgets.QPushButton(parent=self.eqChangeSearchGroupsGroupBox)
        self.eqChangeRefreshGroupButton.setGeometry(QtCore.QRect(10, 110, 181, 41))
        self.eqChangeRefreshGroupButton.setStyleSheet("QPushButton{\n"
                                                      " background-color: #081f2d; \n"
                                                      " border-radius: 8px; \n"
                                                      " border: 2px solid #081F2D; \n"
                                                      " color: white; \n"
                                                      " font-size: 15px;  \n"
                                                      " cursor: pointer; \n"
                                                      " transition: 0.3s; \n"
                                                      " }\n"
                                                      " \n"
                                                      "QPushButton:hover{ \n"
                                                      " background-color: white; \n"
                                                      " color: #081F2D; \n"
                                                      " border-color: #081F2D;\n"
                                                      " transition: 0.9s; \n"
                                                      "}")
        self.eqChangeRefreshGroupButton.setObjectName("eqChangeRefreshGroupButton")
        self.eqChangeSearchGroupButton = QtWidgets.QPushButton(parent=self.eqChangeSearchGroupsGroupBox)
        self.eqChangeSearchGroupButton.setGeometry(QtCore.QRect(10, 60, 121, 41))
        self.eqChangeSearchGroupButton.setStyleSheet("QPushButton{\n"
                                                     " background-color: #081f2d; \n"
                                                     " border-radius: 8px; \n"
                                                     " border: 2px solid #081F2D; \n"
                                                     " color: white; \n"
                                                     " font-size: 15px;  \n"
                                                     " cursor: pointer; \n"
                                                     " transition: 0.3s; \n"
                                                     " }\n"
                                                     " \n"
                                                     "QPushButton:hover{ \n"
                                                     " background-color: white; \n"
                                                     " color: #081F2D; \n"
                                                     " border-color: #081F2D;\n"
                                                     " transition: 0.9s; \n"
                                                     "}")
        self.eqChangeSearchGroupButton.setObjectName("eqChangeSearchGroupButton")
        self.eqChangeGroupByName = QtWidgets.QLineEdit(parent=self.eqChangeSearchGroupsGroupBox)
        self.eqChangeGroupByName.setGeometry(QtCore.QRect(0, 30, 191, 22))
        self.eqChangeGroupByName.setObjectName("eqChangeGroupByName")
        self.searchByEmailOrNameLabel_11 = QtWidgets.QLabel(parent=self.eqChangeSearchGroupsGroupBox)
        self.searchByEmailOrNameLabel_11.setGeometry(QtCore.QRect(30, 10, 161, 16))
        self.searchByEmailOrNameLabel_11.setObjectName("searchByEmailOrNameLabel_11")
        self.eqsearchByGroupLineEdit = QtWidgets.QLineEdit(parent=self.viewInvOrUserBox)
        self.eqsearchByGroupLineEdit.setGeometry(QtCore.QRect(140, 90, 181, 22))
        self.eqsearchByGroupLineEdit.setObjectName("eqsearchByGroupLineEdit")
        self.eqViewRefreshPushButton = QtWidgets.QPushButton(parent=self.viewInvOrUserBox)
        self.eqViewRefreshPushButton.setGeometry(QtCore.QRect(30, 410, 351, 28))
        self.eqViewRefreshPushButton.setStyleSheet("QPushButton{\n"
                                                   " background-color: #081f2d; \n"
                                                   " border-radius: 8px; \n"
                                                   " border: 2px solid #081F2D; \n"
                                                   " color: white; \n"
                                                   " font-size: 15px;  \n"
                                                   " cursor: pointer; \n"
                                                   " transition: 0.3s; \n"
                                                   " }\n"
                                                   " \n"
                                                   "QPushButton:hover{ \n"
                                                   " background-color: white; \n"
                                                   " color: #081F2D; \n"
                                                   " border-color: #081F2D;\n"
                                                   " transition: 0.9s; \n"
                                                   "}")
        self.eqViewRefreshPushButton.setObjectName("eqViewRefreshPushButton")
        self.eqChangeDeleteGroupsButton = QtWidgets.QPushButton(parent=self.viewInvOrUserBox)
        self.eqChangeDeleteGroupsButton.setGeometry(QtCore.QRect(420, 550, 171, 31))
        self.eqChangeDeleteGroupsButton.setStyleSheet("QPushButton{\n"
                                                      " background-color: #081f2d; \n"
                                                      " border-radius: 8px; \n"
                                                      " border: 2px solid #081F2D; \n"
                                                      " color: white; \n"
                                                      " font-size: 15px;  \n"
                                                      " cursor: pointer; \n"
                                                      " transition: 0.3s; \n"
                                                      " }\n"
                                                      " \n"
                                                      "QPushButton:hover{ \n"
                                                      " background-color: white; \n"
                                                      " color: #081F2D; \n"
                                                      " border-color: #081F2D;\n"
                                                      " transition: 0.9s; \n"
                                                      "}")
        self.eqChangeDeleteGroupsButton.setObjectName("eqChangeDeleteGroupsButton")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.RequestsGroupBox = QtWidgets.QGroupBox(parent=self.tab_5)
        self.RequestsGroupBox.setGeometry(QtCore.QRect(0, 0, 1401, 621))
        self.RequestsGroupBox.setStyleSheet("QGroupBox#RequestsGroupBox{\n"
                                            "    border: 0;\n"
                                            "}")
        self.RequestsGroupBox.setTitle("")
        self.RequestsGroupBox.setObjectName("RequestsGroupBox")
        self.textBrowser = QtWidgets.QTextBrowser(parent=self.RequestsGroupBox)
        self.textBrowser.setGeometry(QtCore.QRect(20, 50, 511, 141))
        self.textBrowser.setObjectName("textBrowser")
        self.AcceptReqPushButton = QtWidgets.QPushButton(parent=self.RequestsGroupBox)
        self.AcceptReqPushButton.setGeometry(QtCore.QRect(20, 190, 181, 28))
        self.AcceptReqPushButton.setStyleSheet("QPushButton{\n"
                                               " background-color: #081f2d; \n"
                                               " border-radius: 8px; \n"
                                               " border: 2px solid #081F2D; \n"
                                               " color: white; \n"
                                               " font-size: 15px;  \n"
                                               " cursor: pointer; \n"
                                               " transition: 0.3s; \n"
                                               " }\n"
                                               " \n"
                                               "QPushButton:hover{ \n"
                                               " background-color: white; \n"
                                               " color: #081F2D; \n"
                                               " border-color: #081F2D;\n"
                                               " transition: 0.9s; \n"
                                               "}")
        self.AcceptReqPushButton.setObjectName("AcceptReqPushButton")
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.RequestsGroupBox)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 220, 181, 28))
        self.pushButton_2.setStyleSheet("QPushButton{\n"
                                        " background-color: #081f2d; \n"
                                        " border-radius: 8px; \n"
                                        " border: 2px solid #081F2D; \n"
                                        " color: white; \n"
                                        " font-size: 15px;  \n"
                                        " cursor: pointer; \n"
                                        " transition: 0.3s; \n"
                                        " }\n"
                                        " \n"
                                        "QPushButton:hover{ \n"
                                        " background-color: white; \n"
                                        " color: #081F2D; \n"
                                        " border-color: #081F2D;\n"
                                        " transition: 0.9s; \n"
                                        "}")
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_2 = QtWidgets.QLabel(parent=self.RequestsGroupBox)
        self.label_2.setGeometry(QtCore.QRect(20, 30, 201, 16))
        self.label_2.setObjectName("label_2")
        self.label_7 = QtWidgets.QLabel(parent=self.RequestsGroupBox)
        self.label_7.setGeometry(QtCore.QRect(710, 30, 331, 16))
        self.label_7.setObjectName("label_7")
        self.pushButton = QtWidgets.QPushButton(parent=self.RequestsGroupBox)
        self.pushButton.setGeometry(QtCore.QRect(550, 50, 101, 28))
        self.pushButton.setStyleSheet("QPushButton{\n"
                                      " background-color: #081f2d; \n"
                                      " border-radius: 8px; \n"
                                      " border: 2px solid #081F2D; \n"
                                      " color: white; \n"
                                      " font-size: 15px;  \n"
                                      " cursor: pointer; \n"
                                      " transition: 0.3s; \n"
                                      " }\n"
                                      " \n"
                                      "QPushButton:hover{ \n"
                                      " background-color: white; \n"
                                      " color: #081F2D; \n"
                                      " border-color: #081F2D;\n"
                                      " transition: 0.9s; \n"
                                      "}")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_3 = QtWidgets.QPushButton(parent=self.RequestsGroupBox)
        self.pushButton_3.setGeometry(QtCore.QRect(550, 80, 101, 28))
        self.pushButton_3.setStyleSheet("QPushButton{\n"
                                        " background-color: #081f2d; \n"
                                        " border-radius: 8px; \n"
                                        " border: 2px solid #081F2D; \n"
                                        " color: white; \n"
                                        " font-size: 15px;  \n"
                                        " cursor: pointer; \n"
                                        " transition: 0.3s; \n"
                                        " }\n"
                                        " \n"
                                        "QPushButton:hover{ \n"
                                        " background-color: white; \n"
                                        " color: #081F2D; \n"
                                        " border-color: #081F2D;\n"
                                        " transition: 0.9s; \n"
                                        "}")
        self.pushButton_3.setObjectName("pushButton_3")
        self.label_8 = QtWidgets.QLabel(parent=self.RequestsGroupBox)
        self.label_8.setGeometry(QtCore.QRect(540, 110, 131, 16))
        self.label_8.setObjectName("label_8")
        self.tableView2 = QtWidgets.QTableView(parent=self.RequestsGroupBox)
        self.tableView2.setGeometry(QtCore.QRect(710, 50, 711, 551))
        self.tableView2.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.tableView2.setObjectName("tableView2")
        self.reqViewRefreshPushButton = QtWidgets.QPushButton(parent=self.RequestsGroupBox)
        self.reqViewRefreshPushButton.setGeometry(QtCore.QRect(150, 580, 351, 28))
        self.reqViewRefreshPushButton.setStyleSheet("QPushButton{\n"
                                                    " background-color: #081f2d; \n"
                                                    " border-radius: 8px; \n"
                                                    " border: 2px solid #081F2D; \n"
                                                    " color: white; \n"
                                                    " font-size: 15px;  \n"
                                                    " cursor: pointer; \n"
                                                    " transition: 0.3s; \n"
                                                    " }\n"
                                                    " \n"
                                                    "QPushButton:hover{ \n"
                                                    " background-color: white; \n"
                                                    " color: #081F2D; \n"
                                                    " border-color: #081F2D;\n"
                                                    " transition: 0.9s; \n"
                                                    "}")
        self.reqViewRefreshPushButton.setObjectName("reqViewRefreshPushButton")
        self.reqsearchPushButton = QtWidgets.QPushButton(parent=self.RequestsGroupBox)
        self.reqsearchPushButton.setGeometry(QtCore.QRect(150, 540, 351, 28))
        self.reqsearchPushButton.setStyleSheet("QPushButton{\n"
                                               " background-color: #081f2d; \n"
                                               " border-radius: 8px; \n"
                                               " border: 2px solid #081F2D; \n"
                                               " color: white; \n"
                                               " font-size: 15px;  \n"
                                               " cursor: pointer; \n"
                                               " transition: 0.3s; \n"
                                               " }\n"
                                               " \n"
                                               "QPushButton:hover{ \n"
                                               " background-color: white; \n"
                                               " color: #081F2D; \n"
                                               " border-color: #081F2D;\n"
                                               " transition: 0.9s; \n"
                                               "}")
        self.reqsearchPushButton.setObjectName("reqsearchPushButton")
        self.reqsearchByWhat = QtWidgets.QLineEdit(parent=self.RequestsGroupBox)
        self.reqsearchByWhat.setGeometry(QtCore.QRect(90, 380, 381, 22))
        self.reqsearchByWhat.setObjectName("reqsearchByWhat")
        self.reqsearchByEmail = QtWidgets.QLineEdit(parent=self.RequestsGroupBox)
        self.reqsearchByEmail.setGeometry(QtCore.QRect(170, 320, 301, 22))
        self.reqsearchByEmail.setObjectName("reqsearchByEmail")
        self.searchByIdLabel_4 = QtWidgets.QLabel(parent=self.RequestsGroupBox)
        self.searchByIdLabel_4.setGeometry(QtCore.QRect(40, 380, 41, 16))
        self.searchByIdLabel_4.setObjectName("searchByIdLabel_4")
        self.searchByEmailOrNameLabel_5 = QtWidgets.QLabel(parent=self.RequestsGroupBox)
        self.searchByEmailOrNameLabel_5.setGeometry(QtCore.QRect(20, 320, 141, 16))
        self.searchByEmailOrNameLabel_5.setObjectName("searchByEmailOrNameLabel_5")
        self.reqsearchByUsId = QtWidgets.QLineEdit(parent=self.RequestsGroupBox)
        self.reqsearchByUsId.setGeometry(QtCore.QRect(150, 350, 321, 22))
        self.reqsearchByUsId.setObjectName("reqsearchByUsId")
        self.reqsearchByPurpose = QtWidgets.QLineEdit(parent=self.RequestsGroupBox)
        self.reqsearchByPurpose.setGeometry(QtCore.QRect(90, 410, 381, 22))
        self.reqsearchByPurpose.setObjectName("reqsearchByPurpose")
        self.searchByIdLabel_5 = QtWidgets.QLabel(parent=self.RequestsGroupBox)
        self.searchByIdLabel_5.setGeometry(QtCore.QRect(20, 350, 131, 16))
        self.searchByIdLabel_5.setObjectName("searchByIdLabel_5")
        self.searchByEmailOrNameLabel_6 = QtWidgets.QLabel(parent=self.RequestsGroupBox)
        self.searchByEmailOrNameLabel_6.setGeometry(QtCore.QRect(40, 410, 41, 16))
        self.searchByEmailOrNameLabel_6.setObjectName("searchByEmailOrNameLabel_6")
        self.searchByIdLabel_6 = QtWidgets.QLabel(parent=self.RequestsGroupBox)
        self.searchByIdLabel_6.setGeometry(QtCore.QRect(40, 440, 91, 16))
        self.searchByIdLabel_6.setObjectName("searchByIdLabel_6")
        self.searchByEmailOrNameLabel_7 = QtWidgets.QLabel(parent=self.RequestsGroupBox)
        self.searchByEmailOrNameLabel_7.setGeometry(QtCore.QRect(40, 470, 131, 16))
        self.searchByEmailOrNameLabel_7.setObjectName("searchByEmailOrNameLabel_7")
        self.reqsearchByEqId = QtWidgets.QSpinBox(parent=self.RequestsGroupBox)
        self.reqsearchByEqId.setGeometry(QtCore.QRect(180, 470, 81, 22))
        self.reqsearchByEqId.setObjectName("reqsearchByEqId")
        self.reqsearchByCount = QtWidgets.QSpinBox(parent=self.RequestsGroupBox)
        self.reqsearchByCount.setGeometry(QtCore.QRect(180, 440, 81, 22))
        self.reqsearchByCount.setObjectName("reqsearchByCount")
        self.tabWidget.addTab(self.tab_5, "")
        self.setCentralWidget(self.centralwidget)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)

        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.nameOrEmailLabel_2.setText(_translate("MainWindow", "Название"))
        self.label_27.setText(_translate("MainWindow", "Номер от левого края"))
        self.label_12.setText(_translate("MainWindow", "Описание"))
        self.label_11.setText(_translate("MainWindow", "Доступное количество"))
        self.label_26.setText(_translate("MainWindow", "Высота(от пола)"))
        self.label_10.setText(_translate("MainWindow", "Зарезервированное  количество"))
        self.radioButton_setPos.setText(_translate("MainWindow", "Указать расположение в шкафу"))
        self.eqDelFromSelectedGr.setText(_translate("MainWindow", "==>"))
        self.searchByEmailOrNameLabel_4.setText(_translate("MainWindow", "Название группы"))
        self.eqAddRefreshGroupButton.setText(_translate("MainWindow", "Вернуть полный список групп"))
        self.eqGrToSelected.setText(_translate("MainWindow", "<=="))
        self.eqAddSearchGroupButton.setText(_translate("MainWindow", "Поиск групп"))
        self.eqAddUserOrInvButton.setText(_translate("MainWindow", "Добавить инвентарь"))
        self.eqAddDeleteGroupsButton.setText(_translate("MainWindow", "Удалить все группы"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Добавление инвентаря"))
        self.nameOrEmailLabel_3.setText(_translate("MainWindow", "Email"))
        self.label_9.setText(_translate("MainWindow", "ID карты сотрудника"))
        self.usradioButton_User.setText(_translate("MainWindow", "Пользователь"))
        self.usradioButton_Admin.setText(_translate("MainWindow", "Администратор"))
        self.usadminRightsCheckBox.setText(_translate("MainWindow", "Добавление пользователей"))
        self.usadmin2RightsCheckBox.setText(_translate("MainWindow", "Удаление или редактирование пользователей"))
        self.usadmin3RightsCheckBox.setText(_translate("MainWindow", "Добавление инвентаря"))
        self.usadmin4RightsCheckBox.setText(_translate("MainWindow", "Удаление или редактирование инвентаря"))
        self.usadmin5RightsCheckBox.setText(_translate("MainWindow", "Вынесение решений по запросам"))
        self.rightsLabel_4.setText(_translate("MainWindow", "Имеет права:"))
        self.searchByEmailOrNameLabel_3.setText(_translate("MainWindow", "Название группы"))
        self.usAddSearchGroupButton.setText(_translate("MainWindow", "Поиск группы"))
        self.usAddRefreshGroupButton.setText(_translate("MainWindow", "Вернуть полный список групп"))
        self.usDelFromSelectedGr.setText(_translate("MainWindow", "==>"))
        self.usGrToSelected.setText(_translate("MainWindow", "<=="))
        self.usAddUserOrInvButton.setText(_translate("MainWindow", "Добавить пользователя"))
        self.usAddDeleteGroupsButton.setText(_translate("MainWindow", "Удалить все группы"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2),
                                  _translate("MainWindow", "Добавление пользователей"))
        self.nameOrEmailLabel_8.setText(_translate("MainWindow", "Название"))
        self.grAddPushButton.setText(_translate("MainWindow", "Добавить"))
        self.grSearchPushButton.setText(_translate("MainWindow", "Найти"))
        self.listLabel_13.setText(_translate("MainWindow", "Все группы"))
        self.grRefreshPushButton.setText(_translate("MainWindow", "Вернуть полный список"))
        self.grDeletePushButton.setText(_translate("MainWindow", "Удалить группу"))
        self.grPrevPushButton.setText(_translate("MainWindow", "▲\n"
                                                               "||"))
        self.grNextPushButton.setText(_translate("MainWindow", "||\n"
                                                               "▼"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_16), _translate("MainWindow", "Добавление групп"))
        self.searchByIdLabel_2.setText(_translate("MainWindow", "ID карты пропуска"))
        self.searchByEmailOrNameLabel_2.setText(_translate("MainWindow", "Email"))
        self.ussearchPushButton.setText(_translate("MainWindow", " Поиск"))
        self.usViewRefreshPushButton.setText(_translate("MainWindow", "Обновить таблицу"))
        self.uschangernextPushButton.setText(_translate("MainWindow", "Следующий"))
        self.uschangerprevPushButton.setText(_translate("MainWindow", "Предыдущий"))
        self.uscommitchangesPushButton.setText(_translate("MainWindow", "Принять изменения"))
        self.usChangeDelPushButton.setText(_translate("MainWindow", "Удалить единицу оборудования"))
        self.listLabel_4.setText(_translate("MainWindow", "Группы пользователя"))
        self.label_43.setText(_translate("MainWindow", "количество дней"))
        self.eqCreateStatsPushButton_2.setText(_translate("MainWindow", "Выгрузить статистику в файл"))
        self.listLabel_2.setText(_translate("MainWindow", "Все/найденные элементы оборудования в базе"))
        self.usSearchGrToSelected.setText(_translate("MainWindow", "<=="))
        self.usSearchDelFromSelectedGr.setText(_translate("MainWindow", "==>"))
        self.listLabel_19.setText(_translate("MainWindow", "Все группы"))
        self.usChangeRefreshGroupButton.setText(_translate("MainWindow", "Вернуть полный список"))
        self.usChangeSearchGroupButton.setText(_translate("MainWindow", "Поиск групп"))
        self.searchByEmailOrNameLabel_10.setText(_translate("MainWindow", "Название группы"))
        self.eqsearchByIdLabel_19.setText(_translate("MainWindow", "Название  группы"))
        self.usChangeDeleteGroupsButton.setText(_translate("MainWindow", "Удалить все группы"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4),
                                  _translate("MainWindow", "Просмотр пользователей"))
        self.eqsearchByIdLabel.setText(_translate("MainWindow", "ID"))
        self.searchByEmailOrNameLabel.setText(_translate("MainWindow", "Название"))
        self.listLabel.setText(_translate("MainWindow", "Все/найденные элементы оборудования в базе"))
        self.searchByPosGroupBox.setTitle(_translate("MainWindow", "Поиск по расположению в шкафу"))
        self.label_36.setText(_translate("MainWindow", "Высота(от пола)"))
        self.label_37.setText(_translate("MainWindow", "Номер от левого края"))
        self.eqsearchPushButton.setText(_translate("MainWindow", " Поиск"))
        self.eqchangernextPushButton.setText(_translate("MainWindow", "Следующий"))
        self.eqchangerprevPushButton.setText(_translate("MainWindow", "Предыдущий"))
        self.eqcommitchangesPushButton.setText(_translate("MainWindow", "Принять изменения"))
        self.eqChangeDelPushButton.setText(_translate("MainWindow", "Удалить единицу оборудования"))
        self.eqsearchByIdLabel_2.setText(_translate("MainWindow", "Количество"))
        self.eqsearchByIdLabel_3.setText(_translate("MainWindow", "Зарезервировано"))
        self.listLabel_3.setText(_translate("MainWindow", "Группы оборудования"))
        self.eqsearchByIdLabel_18.setText(_translate("MainWindow", "Название  группы"))
        self.eqCreateStatsPushButton.setText(_translate("MainWindow", "Выгрузить статистику в файл"))
        self.label_42.setText(_translate("MainWindow", "количество дней"))
        self.eqSearchDelFromSelectedGr.setText(_translate("MainWindow", "==>"))
        self.eqSearchGrToSelected.setText(_translate("MainWindow", "<=="))
        self.listLabel_20.setText(_translate("MainWindow", "Все группы"))
        self.searchByEmailOrNameLabel_8.setText(_translate("MainWindow", "Описание"))
        self.eqChangeRefreshGroupButton.setText(_translate("MainWindow", "Вернуть полный список"))
        self.eqChangeSearchGroupButton.setText(_translate("MainWindow", "Поиск групп"))
        self.searchByEmailOrNameLabel_11.setText(_translate("MainWindow", "Название группы"))
        self.eqViewRefreshPushButton.setText(_translate("MainWindow", "Обновить таблицу"))
        self.eqChangeDeleteGroupsButton.setText(_translate("MainWindow", "Удалить все группы"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Просмотр инвентаря"))
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
        self.eqAddUserOrInvButton.clicked.connect(self.add_equipment)
        self.usAddUserOrInvButton.clicked.connect(self.add_user)
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
        self.eqchangernextPushButton.clicked.connect(self.nextEq)
        self.eqchangerprevPushButton.clicked.connect(self.previousEq)
        self.uschangernextPushButton.clicked.connect(self.nextUs)
        self.uschangerprevPushButton.clicked.connect(self.previousUs)
        self.uscommitchangesPushButton.clicked.connect(self.changeUs)
        self.eqcommitchangesPushButton.clicked.connect(self.changeEq)
        self.eqGrToSelected.clicked.connect(self.selected_to_eq_groups)
        self.usGrToSelected.clicked.connect(self.selected_to_us_groups)
        self.usDelFromSelectedGr.clicked.connect(self.del_from_us_selected_groups)
        self.eqDelFromSelectedGr.clicked.connect(self.del_from_eq_selected_groups)
        self.grAddPushButton.clicked.connect(self.add_group)
        self.eqSearchGrToSelected.clicked.connect(self.selected_to_eq_search_groups)
        self.usSearchGrToSelected.clicked.connect(self.selected_to_us_search_groups)
        self.eqSearchDelFromSelectedGr.clicked.connect(self.del_from_eq_search_selected_groups)
        self.usSearchDelFromSelectedGr.clicked.connect(self.del_from_us_search_selected_groups)
        self.heightSpinBox.setMinimum(-1)
        self.posFromLeftSpinBox.setMinimum(-1)
        self.heightSpinBox.setValue(-1)
        self.posFromLeftSpinBox.setValue(-1)
        self.eqsearchByIdSpinBox.setMinimum(-1)
        self.searchByPosFromLeftSpinBox.setMinimum(-1)
        self.searchByHeightSpinBox.setValue(-1)
        self.searchByHeightSpinBox.setMinimum(-1)
        self.searchByPosFromLeftSpinBox.setMinimum(-1)
        self.eqsearchByNumberSpinBox.setMinimum(-1)
        self.eqsearchByReservedSpinBox.setMinimum(-1)
        self.eqsearchByNumberSpinBox.setValue(-1)
        self.eqsearchByReservedSpinBox.setValue(-1)
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
        self.refresh_gr_view_table()
        self.refresh_requests_table()
        self.refresh_equipment_table()
        self.refresh_users_table()
        self.eqDelFromSelectedGr.hide()
        self.usDelFromSelectedGr.hide()
        self.eqSearchDelFromSelectedGr.hide()
        self.usSearchDelFromSelectedGr.hide()
        self.usChangeSearchGroupsGroupBox.hide()
        self.eqChangeSearchGroupsGroupBox.hide()
        self.eqChangeSearchGroupButton.clicked.connect(self.search_groups_in_eq_search_groups)
        self.eqChangeRefreshGroupButton.clicked.connect(self.refresh_groups_in_eq_search_groups)
        self.usChangeSearchGroupButton.clicked.connect(self.search_groups_in_us_search_groups)
        self.usChangeRefreshGroupButton.clicked.connect(self.refresh_groups_in_us_search_groups)
        self.usAddSearchGroupButton.clicked.connect(self.search_groups_in_us_add_groups)
        self.usAddRefreshGroupButton.clicked.connect(self.refresh_groups_in_us_add_groups)
        self.eqAddSearchGroupButton.clicked.connect(self.search_groups_in_eq_add_groups)
        self.eqAddRefreshGroupButton.clicked.connect(self.refresh_groups_in_eq_add_groups)
        self.grRefreshPushButton.clicked.connect(self.refresh_only_groups_table)
        self.grSearchPushButton.clicked.connect(self.search_groups_in_groups)
        self.grPrevPushButton.clicked.connect(self.prevGr)
        self.grNextPushButton.clicked.connect(self.nextGr)
        self.grDeletePushButton.hide()
        self.grNextPushButton.hide()
        self.grPrevPushButton.hide()
        self.usChangeDeleteGroupsButton.hide()
        self.eqChangeDeleteGroupsButton.hide()
        self.usChangeDelPushButton.clicked.connect(self.del_user)
        self.grDeletePushButton.clicked.connect(self.del_group)
        self.eqChangeDelPushButton.clicked.connect(self.del_equipment)
        self.eqAddDeleteGroupsButton.clicked.connect(self.del_all_from_eq_selected_groups)
        self.usAddDeleteGroupsButton.clicked.connect(self.del_all_from_eq_selected_groups)
        self.eqAddDeleteGroupsButton.clicked.connect(self.del_all_from_eq_search_selected_groups)
        self.usAddDeleteGroupsButton.clicked.connect(self.del_all_from_us_search_selected_groups)
        self.refresh_selected_eq_groups()
        self.refresh_selected_us_groups()
        self.refresh_selected_us_search_groups()
        self.refresh_selected_eq_search_groups()
        self.show()
    def search_groups_in_groups(self):
        if self.grAddLineEdit.text()!='':
            self.__currGroupsTableContents = []
            for i in self.__allGroups.keys():
                if i.find(self.grAddLineEdit.text())>=0:
                    self.__currGroupsTableContents.append(i)
            if len(self.__currGroupsTableContents)>0:
                self.grTableView.clearSpans()
                data_frame = pd.DataFrame(self.__currGroupsTableContents,
                                          columns=["Название группы"],
                                          index=[i for i in range(len(self.__currGroupsTableContents))])
                model = TableModel(data_frame)
                self.grTableView.setModel(model)
                self.grAddLineEdit.setText("")
                self.__grnum=0
                self.grDeletePushButton.show()
                self.grAddPushButton.setText("Принять изменения")
                self.set_gr_info()
            else:
                show_message('Проблема','Ничего не найдено')
                self.__grnum=-2
    def set_gr_info(self):
        if self.__grnum!=-1:
            self.grTableView.selectRow(self.__grnum)
            if self.__grnum >= 0 and self.__grnum <= len(self.__currGroupsTableContents) -1:
                self.grAddLineEdit.setText(self.__currGroupsTableContents[self.__grnum])
            if self.__grnum == 0:
                self.grPrevPushButton.hide()
            else:
                self.grPrevPushButton.show()
            if self.__grnum == len(self.__currGroupsTableContents) -1:
                self.grNextPushButton.hide()
            else:
                self.grNextPushButton.show()
    def prevGr(self):
        if self.__grnum>0:
            self.__grnum = self.__grnum - 1
            self.set_gr_info()
    def nextGr(self):
            if self.__grnum<= len(self.__currGroupsTableContents)-1:
                self.__grnum = self.__grnum + 1
                self.set_gr_info()
    #def changeGroup(self):
    def del_user(self):
        self.__user_list.del_user(int(self.__usFoundTableContents[self.__usnum][0],16))
        self.__usFoundTableContents.pop(self.__usnum)
        if len(self.__usFoundTableContents)>0:
            self.usTableView.clearSpans()
            data_frame = pd.DataFrame(self.__usFoundTableContents, columns=["ID карты", "Почта"],
                                      index=[i for i in range(len(self.__usFoundTableContents))])
            model = TableModel(data_frame)
            self.setUsInfo()
            self.usTableView.setModel(model)
        else:
            self.refresh_users_table()
            show_message("успех","Пользователь удален")
    def del_equipment(self):
        self.__equipment_list.del_equipment(int(self.__eqFoundTableContents[self.__eqnum][0]))
        self.__eqFoundTableContents.pop(self.__eqnum)
        if len(self.__eqFoundTableContents)>0:
            self.usTableView.clearSpans()
            data_frame = pd.DataFrame(self.__eqFoundTableContents, columns=["ID карты", "Почта"],
                                      index=[i for i in range(len(self.__eqFoundTableContents))])
            model = TableModel(data_frame)
            self.setEqInfo()
            self.eqTableView.setModel(model)
        else:
            self.refresh_equipment_table()
            show_message("успех","Оборудование удалено")
    def del_group(self):
        self.__db.del_group(self.__allGroups[self.__currGroupsTableContents[self.__grnum]])
        to_delete=self.__currGroupsTableContents[self.__grnum]
        self.__currGroupsTableContents.pop(self.__grnum)
        if len(self.__currGroupsTableContents)>0:
            self.grTableView.clearSpans()
            data_frame = pd.DataFrame(self.__currGroupsTableContents, columns=["Название группы"],
                                      index=[i for i in range(len(self.__currGroupsTableContents))])
            model = TableModel(data_frame)
            self.set_gr_info()
            self.grTableView.selectRow(self.__grnum)
            self.grTableView.setModel(model)
        else:
            show_message("успех","Группа удалена")
        self.eqGroupsTableView.clearSpans()
        self.usGroupsTableView.clearSpans()
        self.eqAddSelectedGrTableView.clearSpans()
        self.usAddSelectedGrTableView.clearSpans()
        if to_delete in self.__currEqGroupsTableContents:
            self.__currEqGroupsTableContents.remove(to_delete)
            self.__eqFoundGroups.remove(self.__allGroups[to_delete])
        data_frame = pd.DataFrame(self.__currEqGroupsTableContents,
                                  columns=["Название группы"],
                                  index=[i for i in range(len(self.__currEqGroupsTableContents))])
        model = TableModel(data_frame)
        self.eqGroupsTableView.setModel(model)
        if to_delete in self.__currUsGroupsTableContents:
            self.__currUsGroupsTableContents.remove(to_delete)
            self.__usFoundGroups.remove(self.__allGroups[to_delete])
        data_frame = pd.DataFrame(self.__currUsGroupsTableContents,
                                  columns=["Название группы"],
                                  index=[i for i in range(len(self.__currUsGroupsTableContents))])
        model = TableModel(data_frame)
        self.usGroupsTableView.setModel(model)
        if to_delete in self.__addEqTableContents:
            self.__addEqTableContents.remove(to_delete)
        data_frame = pd.DataFrame(self.__addEqTableContents,
                                  columns=["Название группы"],
                                  index=[i for i in range(len(self.__addEqTableContents))])
        model = TableModel(data_frame)
        self.eqAddSelectedGrTableView.setModel(model)
        if to_delete in self.__addUsTableContents:
            self.__addUsTableContents.remove(to_delete)
        data_frame = pd.DataFrame(self.__addUsTableContents,
                                  columns=["Название группы"],
                                  index=[i for i in range(len(self.__addUsTableContents))])
        model = TableModel(data_frame)
        self.usAddSelectedGrTableView.setModel(model)
        del self.__allGroups[to_delete]
        self.refresh_gr_view_table()
    def change_group(self):
        if self.grAddLineEdit.text()!='':
            if self.grAddLineEdit.text() in self.__allGroups.keys() and self.grAddLineEdit.text()!=self.__currGroupsTableContents[self.__grnum]:
                show_message("Ошибка","группа с таким названием уже существует")
            elif self.grAddLineEdit.text()==self.__currGroupsTableContents[self.__grnum]:
                show_message("Ошибка","группа уже имееь такое название")
            elif self.grAddLineEdit.text() not in self.__allGroups.keys():
                self.__db.rename_group(self.__allGroups[self.__currGroupsTableContents[self.__grnum]],self.grAddLineEdit.text())
                old_name=self.__currGroupsTableContents[self.__grnum]
                new_name=self.grAddLineEdit.text()
                if old_name in self.__currGroupsTableContents:
                    self.__currGroupsTableContents[self.__currGroupsTableContents.index(old_name)]=new_name
                self.grTableView.clearSpans()
                data_frame = pd.DataFrame(self.__currGroupsTableContents, columns=["Название группы"],
                                          index=[i for i in range(len(self.__currGroupsTableContents))])
                model = TableModel(data_frame)
                self.grTableView.setModel(model)

                if old_name in self.__currEqGroupsTableContents:
                    self.__currEqGroupsTableContents[self.__currEqGroupsTableContents.index(old_name)]=new_name
                self.eqGroupsTableView.clearSpans()
                data_frame = pd.DataFrame(self.__currEqGroupsTableContents, columns=["Название группы"],
                                          index=[i for i in range(len(self.__currEqGroupsTableContents))])
                model = TableModel(data_frame)
                self.eqGroupsTableView.setModel(model)

                if old_name in self.__currUsGroupsTableContents:
                    self.__currUsGroupsTableContents[self.__currUsGroupsTableContents.index(old_name)]=new_name
                self.usGroupsTableView.clearSpans()
                data_frame = pd.DataFrame(self.__currUsGroupsTableContents, columns=["Название группы"],
                                          index=[i for i in range(len(self.__currUsGroupsTableContents))])
                model = TableModel(data_frame)
                self.usGroupsTableView.setModel(model)

                if old_name in self.__addUsTableContents:
                    self.__addUsTableContents[self.__addUsTableContents.index(old_name)]=new_name
                self.usAddSelectedGrTableView.clearSpans()
                data_frame = pd.DataFrame(self.__addUsTableContents, columns=["Название группы"],
                                          index=[i for i in range(len(self.__addUsTableContents))])
                model = TableModel(data_frame)
                self.usAddSelectedGrTableView.setModel(model)

                if old_name in self.__addUsTableContents:
                    self.__addUsTableContents[self.__addUsTableContents.index(old_name)]=new_name
                self.usAddSelectedGrTableView.clearSpans()
                data_frame = pd.DataFrame(self.__addUsTableContents, columns=["Название группы"],
                                          index=[i for i in range(len(self.__addUsTableContents))])
                model = TableModel(data_frame)
                self.usAddSelectedGrTableView.setModel(model)

                self.__allGroups[self.grAddLineEdit.text()]=self.__allGroups[old_name]
                show_message("успех","Группа переименована")
                del self.__allGroups[old_name]
                self.refresh_gr_view_table()

    def search_groups_in_eq_search_groups(self):
        if self.eqChangeGroupByName.text() != '':
            self.eqSearchAllGrTableView.clearSpans()
            new_table=[]
            for i in self.__allGroups.keys():
                if i.find(self.eqChangeGroupByName.text()) >= 0 or i==self.eqChangeGroupByName.text():
                    new_table.append(i)
            data_frame = pd.DataFrame(new_table,
                                      columns=["Название группы"],
                                      index=[i for i in range(len(new_table))])
            model = TableModel(data_frame)
            self.eqSearchAllGrTableView.setModel(model)
    def refresh_groups_in_eq_search_groups(self):
        self.eqSearchAllGrTableView.clearSpans()
        data_frame = pd.DataFrame(sorted(self.__allGroups),columns=["Название группы"],index=[i for i in range(len(sorted(self.__allGroups)))])
        model = TableModel(data_frame)
        self.eqSearchAllGrTableView.setModel(model)
    def search_groups_in_us_search_groups(self):
        if self.usChangeGroupByName.text() != '':
            self.usSearchAllGrTableView.clearSpans()
            new_table=[]
            for i in self.__allGroups.keys():
                if i.find(self.usChangeGroupByName.text()) >= 0 or i==self.usChangeGroupByName.text():
                    new_table.append(i)
            data_frame = pd.DataFrame(new_table,
                                      columns=["Название группы"],
                                      index=[i for i in range(len(new_table))])
            model = TableModel(data_frame)
            self.usSearchAllGrTableView.setModel(model)
    def refresh_groups_in_us_search_groups(self):
        self.usSearchAllGrTableView.clearSpans()
        data_frame = pd.DataFrame(sorted(self.__allGroups),columns=["Название группы"],index=[i for i in range(len(sorted(self.__allGroups)))])
        model = TableModel(data_frame)
        self.usSearchAllGrTableView.setModel(model)
    def search_groups_in_eq_add_groups(self):
        if self.eqAddGroupByName.text() != '':
            self.eqAddAllGrTableView.clearSpans()
            new_table=[]
            for i in self.__allGroups.keys():
                if i.find(self.eqAddGroupByName.text()) >= 0 or i==self.eqAddGroupByName.text():
                    new_table.append(i)
            data_frame = pd.DataFrame(new_table,
                                      columns=["Название группы"],
                                      index=[i for i in range(len(new_table))])
            model = TableModel(data_frame)
            self.eqAddAllGrTableView.setModel(model)
    def refresh_groups_in_eq_add_groups(self):
        self.eqAddAllGrTableView.clearSpans()
        data_frame = pd.DataFrame(sorted(self.__allGroups),columns=["Название группы"],index=[i for i in range(len(sorted(self.__allGroups)))])
        model = TableModel(data_frame)
        self.eqAddAllGrTableView.setModel(model)
    def search_groups_in_us_add_groups(self):
        if self.usAddGroupByName.text() != '':
            self.usAddAllGrTableView.clearSpans()
            new_table=[]
            for i in self.__allGroups.keys():
                if i.find(self.usAddGroupByName.text()) >= 0 or i==self.usAddGroupByName.text():
                    new_table.append(i)
            data_frame = pd.DataFrame(new_table,
                                      columns=["Название группы"],
                                      index=[i for i in range(len(new_table))])
            model = TableModel(data_frame)
            self.usAddAllGrTableView.setModel(model)
    def refresh_groups_in_us_add_groups(self):
        self.usAddAllGrTableView.clearSpans()
        data_frame = pd.DataFrame(sorted(self.__allGroups),columns=["Название группы"],index=[i for i in range(len(sorted(self.__allGroups)))])
        model = TableModel(data_frame)
        self.usAddAllGrTableView.setModel(model)

    def selected_to_us_groups(self):
        indexes = self.usAddAllGrTableView.selectionModel().selectedRows()
        if len(indexes) > 0:
            for i in indexes:
                if i.data(0) not in self.__addUsTableContents:
                    self.__addUsTableContents.append(i.data(0))
            self.refresh_selected_us_groups()
            self.usDelFromSelectedGr.show()

    def selected_to_eq_search_groups(self):
        indexes = self.eqSearchAllGrTableView.selectionModel().selectedRows()
        if len(indexes) > 0:
            for i in indexes:
                if i.data(0) not in self.__currEqGroupsTableContents:
                    self.__currEqGroupsTableContents.append(i.data(0))
            self.refresh_selected_eq_search_groups()
            self.eqSearchDelFromSelectedGr.show()

    def selected_to_us_search_groups(self):
        indexes = self.usSearchAllGrTableView.selectionModel().selectedRows()
        if len(indexes) > 0:
            for i in indexes:
                if i.data(0) not in self.__currUsGroupsTableContents:
                    self.__currUsGroupsTableContents.append(i.data(0))
            self.refresh_selected_us_search_groups()
            self.usSearchDelFromSelectedGr.show()

    def selected_to_eq_groups(self):
        indexes = self.eqAddAllGrTableView.selectionModel().selectedRows()
        if len(indexes) > 0:
            for i in indexes:
                if i.data(0) not in self.__addEqTableContents:
                    self.__addEqTableContents.append(i.data(0))
            self.refresh_selected_eq_groups()
            self.eqDelFromSelectedGr.show()

    def del_from_eq_search_selected_groups(self):
        indexes = self.eqGroupsTableView.selectionModel().selectedRows()
        if len(indexes) > 0:
            for i in reversed(indexes):
                self.__currEqGroupsTableContents.remove(i.data(0))
        self.refresh_selected_eq_search_groups()
    def del_all_from_eq_search_selected_groups(self):
        self.__currEqGroupsTableContents=[]
        self.refresh_selected_eq_search_groups()
    def del_from_us_search_selected_groups(self):
        indexes = self.usGroupsTableView.selectionModel().selectedRows()
        if len(indexes) > 0:
            for i in reversed(indexes):
                self.__currUsGroupsTableContents.remove(i.data(0))
        self.refresh_selected_us_search_groups()
        if len(self.__currUsGroupsTableContents) == 0:
            self.usSearchDelFromSelectedGr.hide()
    def del_all_from_us_search_selected_groups(self):
        self.__currUsGroupsTableContents=[]
        self.refresh_selected_us_search_groups()
    def del_from_eq_selected_groups(self):
        indexes = self.eqAddSelectedGrTableView.selectionModel().selectedRows()
        if len(indexes) > 0:
            for i in reversed(indexes):
                self.__addEqTableContents.remove(i.data(0))
        self.refresh_selected_eq_groups()
    def del_all_from_eq_selected_groups(self):
        self.__addEqTableContents=[]
        self.refresh_selected_eq_groups()

    def del_from_us_selected_groups(self):
        indexes = self.usAddSelectedGrTableView.selectionModel().selectedRows()
        if len(indexes) > 0:
            for i in reversed(indexes):
                self.__addUsTableContents.remove(i.data(0))
        self.refresh_selected_us_groups()
        if len(self.__addUsTableContents) == 0:
            self.usDelFromSelectedGr.hide()
    def del_all_from_us_selected_groups(self):
        self.__addUsTableContents=[]
        self.refresh_selected_us_groups()
    def refresh_equipment_table(self):
        self.eqchangerGroupBox.hide()
        self.__eqFoundTableContents = []
        self.eqsearchByIdSpinBox.setValue(-1)
        self.searchByHeightSpinBox.setValue(-1)
        self.eqTableView.clearSpans()
        self.__eqTableContents.clear()
        all_eq = self.__equipment_list.get_equipment_list()
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
                x,
                y])
        data_frame = pd.DataFrame(self.__eqTableContents,
                                  columns=["ID", "Название", "Количество", "Зарезервировано", "От стены", "От пола"],
                                  index=[i for i in range(len(self.__eqTableContents))])
        model = TableModel(data_frame)
        self.eqTableView.setModel(model)
        self.eqsearchByIdSpinBox.setValue(-1)
        self.eqsearchByEmailOrNameLineEdit.setText('')
        self.searchByHeightSpinBox.setValue(-1)
        self.searchByPosFromLeftSpinBox.setValue(-1)
        self.eqsearchByReservedSpinBox.setValue(-1)
        self.eqsearchByNumberSpinBox.setValue(-1)
        self.eqSearchAllGrTableView.hide()
        self.eqGroupsTableView.hide()
        self.eqSearchGrToSelected.hide()
        self.eqSearchDelFromSelectedGr.hide()
        self.listLabel_3.hide()
        self.listLabel_20.hide()
        self.eqTableView.setGeometry(QtCore.QRect(420, 40, 1201, 721))
        self.eqChangeSearchGroupsGroupBox.hide()
        self.eqsearchByEmailOrNameLineEdit_2.setText("")
        self.eqsearchByGroupLineEdit.setText("")
        self.eqChangeDelPushButton.hide()
        self.eqChangeDeleteGroupsButton.hide()

    def refresh_users_table(self):
        self.usChangeSearchGroupsGroupBox.hide()
        self.listLabel_19.hide()
        self.listLabel_4.setText("Все пользователи")
        self.uschangerGroupBox.hide()
        self.__usFoundTableContents = []
        self.usTableView.clearSpans()
        ref = AdminAccess
        self.__usTableContents.clear()
        for i in self.__user_list.get_user_list():
            self.__usTableContents.append([
                str(hex(i.pass_number)),
                i.mail,
            ])
        data_frame = pd.DataFrame(self.__usTableContents, columns=["ID карты", "Почта"],
                                  index=[i for i in range(len(self.__usTableContents))])
        model = TableModel(data_frame)
        self.usTableView.setModel(model)
        self.usGroupsTableView.hide()
        self.listLabel_4.hide()
        self.usSearchAllGrTableView.hide()
        self.usSearchGrToSelected.hide()
        self.usSearchDelFromSelectedGr.hide()
        self.listLabel_2.hide()
        self.usTableView.setGeometry(QtCore.QRect(470, 30, 1101, 721))
        self.ussearchByNameOrEmailLineEdit.setText("")
        self.ussearchByEmailOrNameLineEdit.setText("")
        self.ussearchByGroupLineEdit.setText("")
        self.usChangeDelPushButton.hide()
        self.usChangeDeleteGroupsButton.hide()

    def refresh_gr_view_table(self):
        self.grTableView.clearSpans()
        self.eqAddAllGrTableView.clearSpans()
        self.usAddAllGrTableView.clearSpans()
        self.eqAddAllGrTableView.clearSpans()
        self.usAddAllGrTableView.clearSpans()
        self.usSearchAllGrTableView.clearSpans()
        self.eqSearchAllGrTableView.clearSpans()
        for i in self.__db.get_all_groups():
            self.__allGroups[i.group_name] = i.id
        data_frame = pd.DataFrame(self.__allGroups.keys(),
                                  columns=["Название группы"],
                                  index=[i for i in range(len(self.__allGroups.keys()))])
        model = TableModel(data_frame)
        self.grTableView.setModel(model)
        self.eqAddAllGrTableView.setModel(model)
        self.usAddAllGrTableView.setModel(model)
        self.eqAddAllGrTableView.setModel(model)
        self.usAddAllGrTableView.setModel(model)
        self.usSearchAllGrTableView.setModel(model)
        self.eqSearchAllGrTableView.setModel(model)
    def refresh_only_groups_table(self):
        self.grTableView.clearSpans()
        data_frame = pd.DataFrame(self.__allGroups.keys(),
                                  columns=["Название группы"],
                                  index=[i for i in range(len(self.__allGroups.keys()))])
        model = TableModel(data_frame)
        self.grTableView.setModel(model)
        self.grDeletePushButton.hide()
        self.grNextPushButton.hide()
        self.grPrevPushButton.hide()
        self.grAddPushButton.setText("Добавить")
        self.__grnum=-2
    def refresh_selected_us_groups(self):
        self.usAddSelectedGrTableView.clearSpans()
        data_frame = pd.DataFrame(self.__addUsTableContents,
                                  columns=["Название групп"],
                                  index=[i for i in range(len(self.__addUsTableContents))])
        model = TableModel(data_frame)
        self.usAddSelectedGrTableView.setModel(model)
        if len(self.__addUsTableContents) == 0:
            self.usDelFromSelectedGr.hide()
            self.usAddDeleteGroupsButton.hide()
        else:
            self.usDelFromSelectedGr.show()
            self.usAddDeleteGroupsButton.show()

    def refresh_selected_eq_groups(self):
        self.eqAddSelectedGrTableView.clearSpans()
        data_frame = pd.DataFrame(self.__addEqTableContents,
                                  columns=["Название групп"],
                                  index=[i for i in range(len(self.__addEqTableContents))])
        model = TableModel(data_frame)
        self.eqAddSelectedGrTableView.setModel(model)
        if len(self.__addEqTableContents) == 0:
            self.eqDelFromSelectedGr.hide()
            self.eqAddDeleteGroupsButton.hide()
        else:
            self.eqDelFromSelectedGr.show()
            self.eqAddDeleteGroupsButton.show()
    def refresh_selected_eq_search_groups(self):
        self.eqGroupsTableView.clearSpans()
        data_frame = pd.DataFrame(self.__currEqGroupsTableContents,
                                  columns=["Название групп"],
                                  index=[i for i in range(len(self.__currEqGroupsTableContents))])
        model = TableModel(data_frame)
        self.eqGroupsTableView.setModel(model)
        if len(self.__currEqGroupsTableContents) == 0:
            self.eqSearchDelFromSelectedGr.hide()
            self.eqChangeDeleteGroupsButton.hide()
        else:
            self.eqSearchDelFromSelectedGr.show()
            self.eqChangeDeleteGroupsButton.show()
    def refresh_selected_us_search_groups(self):
        self.usGroupsTableView.clearSpans()
        data_frame = pd.DataFrame(self.__currUsGroupsTableContents,
                                  columns=["Название групп"],
                                  index=[i for i in range(len(self.__currUsGroupsTableContents))])
        model = TableModel(data_frame)
        self.usGroupsTableView.setModel(model)
        if len(self.__currUsGroupsTableContents) == 0:
            self.usSearchDelFromSelectedGr.hide()
            self.usSearchDelFromSelectedGr.hide()
        else:
            self.usSearchDelFromSelectedGr.show()
            self.usSearchDelFromSelectedGr.show()
    def refresh_requests_table(self):
        # self.__reqs = self.__db.get_unsolved_requests()
        self.tableView2.clearSpans()
        self.__reqs = self.__db.get_unsolved_users_requests()
        if (len(self.__reqs)) == 0:
            print("0 requests")
        self.__reqnum = 0
        self.__reqTableContents.clear()
        for i in self.__reqs:
            self.__reqTableContents.append([
                str(i.id),
                str(self.__equipment_list.get_equipment_by_id(i.equipment_id).title),
                str(i.count),
                str(i.purpose),
                str(hex(i.sender_tg_id)),
                str(self.__user_list.get_user_by_id(i.sender_id).mail)
            ])
        data_frame = pd.DataFrame(self.__reqTableContents,
                                  columns=["ID", "Что", "Сколько", "Цель", "ID запросившего", "EMAIL запросившего"],
                                  index=[i for i in range(len(self.__reqTableContents))]
                                  )
        model = TableModel(data_frame)
        self.tableView2.setModel(model)
        self.label_8.setText("Необработанных: " + str(len(self.__reqs)))
        self.get_request()
    def add_equipment(self):
        code_error = -1
        if code_error == -1 and self.eqNameOrEmailLineEdit.text() == "":
            code_error = 1
        elif self.__equipment_list.get_equipment_by_title(self.eqNameOrEmailLineEdit.text()):
            code_error = 8
        if code_error == -1 and self.descriptionTextEdit.toPlainText() == "":
            code_error = 3
        from_left = self.posFromLeftSpinBox.value()
        if self.posFromLeftSpinBox.value() == 0 or self.posFromLeftSpinBox.value() == -1:
            from_left = -1
        height = self.heightSpinBox.value()
        if self.heightSpinBox.value() == 0 or self.heightSpinBox.value() == -1:
            height = -1
        if code_error == -1 and self.__equipment_list.get_equipment_by_coordinates(from_left,
                                                                                   height) is not None and from_left != -1 and height != -1:
            code_error = 9
        if code_error == -1 and self.__equipment_list.get_equipment_by_coordinates(from_left,
                                                                                   height) is not None and from_left != -1 and height != -1:
            code_error = 9
        if code_error == -1:
            groups = []
            for i in self.__addEqTableContents:
                groups.append(self.__allGroups[i])
            eq = Equipment(self.eqNameOrEmailLineEdit.text(),
                           self.descriptionTextEdit.toPlainText(),
                           self.ableNowSpinBox.value(), self.reservedSpinBox.value(), groups, height, from_left)
            show_message("Успех", "Оборудование добавлено в базу")
            self.__equipment_list.add_equipment(eq)
            self.heightSpinBox.setValue(-1)
            self.posFromLeftSpinBox.setValue(-1)
            self.eqNameOrEmailLineEdit.setText("")
            self.descriptionTextEdit.setText("")
            self.heightSpinBox.setValue(-1)
            self.posFromLeftSpinBox.setValue(-1)
            self.refresh_equipment_table()
            self.eqAddSelectedGrTableView.clearSpans()
            self.__addEqTableContents.clear()
        else:
            if code_error == 1:
                show_message("Ошибка добавления", "Введите название")
            elif code_error == 3:
                show_message("Ошибка добавления", "отсутствует описание")
            elif code_error == 8:
                show_message("Ошибка добавления", "Оборудование с таким названием уже есть в базе")
            elif code_error == 9:
                show_message("Ошибка добавления", "Ячейка занята")
    def add_user(self):
        code_error = -1
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
        if code_error == -1 and self.__user_list.get_user_by_pass(int(self.usIdCardLineEdit.text(), 16)) is not None:
            code_error = 7
        if code_error == -1 and self.__user_list.get_user_by_mail(self.usnameOrEmailLineEdit.text()) is not None:
            code_error = 8
        if code_error == -1:
            if self.usradioButton_User.isChecked():
                groups = []
                for i in self.__addUsTableContents:
                    groups.append(self.__allGroups[i])
                ac = Access(groups)
                us = CommonUser(int(self.usIdCardLineEdit.text(), 16), str(self.usnameOrEmailLineEdit.text()), ac)
                self.__user_list.append_user(us)
            if self.usradioButton_Admin.isChecked():
                groups = []
                for i in self.__addUsTableContents:
                    groups.append(self.__allGroups[i])
                ac = AdminAccess(groups, add_users, change_users, add_equipment, change_equipment, get_request)
                adm = Admin(int(self.usIdCardLineEdit.text(), 16), str(self.usnameOrEmailLineEdit.text()), ac)
                self.__user_list.append_user(adm)
            self.heightSpinBox.setValue(-1)
            self.posFromLeftSpinBox.setValue(-1)
            self.usnameOrEmailLineEdit.setText("")
            self.descriptionTextEdit.setText("")
            self.usIdCardLineEdit.setText("")
            self.refresh_users_table()
            self.usAddSelectedGrTableView.clearSpans()
            self.__addUsTableContents.clear()
            show_message("Успех", "Пользователь добавлен")
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
    def add_group(self):
        if self.__grnum==-2:
            code_error = -1
            if self.grAddLineEdit.text() == '':
                code_error = 2
            elif self.__db.get_group_by_name(self.grAddLineEdit.text()) != None:
                code_error = 4
            if code_error == -1:
                self.__db.add_group(self.grAddLineEdit.text())
                self.grAddLineEdit.setText("")
                self.refresh_gr_view_table()
            elif code_error == 2:
                show_message("Ошибка добавления", "Введите название группы")
            elif code_error == 4:
                show_message("Ошибка добавления", "Группа с таким названием уже есть в базе")
        else:
            self.change_group()
    def changeUs(self):
        code_error = -1

        if (self.__user_list.get_user_by_pass(
                int(self.ussearchByNameOrEmailLineEdit.text(), 16)) is not None) and \
                self.__user_list.get_user_by_pass(int(self.ussearchByNameOrEmailLineEdit.text(), 16)).mail != \
                self.__usFoundTableContents[self.__usnum][
                    1]:
            code_error = 7
        elif (self.__user_list.get_user_by_mail(
                self.ussearchByEmailOrNameLineEdit.text()) is not None) and \
                (self.__user_list.get_user_by_mail(self.ussearchByEmailOrNameLineEdit.text()).pass_number !=
                 int(self.__usFoundTableContents[self.__usnum][0], 16)):
            code_error = 8
        if code_error == -1:
            user_to_change = self.__user_list.get_user_by_pass(int(self.__usFoundTableContents[self.__usnum][0], 16))
            user_to_change.pass_number = int(self.ussearchByNameOrEmailLineEdit.text(), 16)
            user_to_change.mail = self.ussearchByEmailOrNameLineEdit.text()
            user_to_change.access.groups.clear()
            for i in self.__currUsGroupsTableContents:
                user_to_change.access.groups.append(self.__allGroups[i])
            self.__user_list.change_user(int(self.__usFoundTableContents[self.__usnum][0], 16),
                                         self.__usFoundTableContents[self.__usnum][1],
                                         user_to_change)
            self.refresh_users_table()
        else:
            if code_error == 1:
                show_message("Ошибка изменения", "Введите ID карты сотрудника")
            elif code_error == 2:
                show_message("Ошибка изменения", "Введите Email сотрудника")
            elif code_error == 7:
                show_message("Ошибка изменения", "этот ID уже занят")
            elif code_error == 8:
                show_message("Ошибка изменения", "Другой пользователь с таким email уже добавлен")
    def changeEq(self):
        code_error = -1
        if (self.__equipment_list.get_equipment_by_title(
                self.eqsearchByEmailOrNameLineEdit.text()) is not None) and self.__equipment_list.get_equipment_by_title(
                self.eqsearchByEmailOrNameLineEdit.text()).id != int(self.__eqFoundTableContents[self.__eqnum][0]):
            code_error = 7
        if code_error == -1:
            eq_to_change = self.__equipment_list.get_equipment_by_id(int(self.__eqFoundTableContents[self.__eqnum][0]))
            if int(self.__eqFoundTableContents[self.__eqnum][0])!=self.eqsearchByIdSpinBox.value():
                show_message("Ошибка","ID оборудования нельзя изменить")
            eq_to_change.title = self.eqsearchByEmailOrNameLineEdit.text()
            # eq_to_change.access = tg
            if self.eqsearchByNumberSpinBox.value() > -1:
                eq_to_change.count = self.eqsearchByNumberSpinBox.value()
            else:
                eq_to_change.count = 0
            if self.eqsearchByReservedSpinBox.value() > -1:
                eq_to_change.reserve_count = self.eqsearchByReservedSpinBox.value()
            else:
                eq_to_change.reserve_count = 0
            eq_to_change.description=self.eqsearchByEmailOrNameLineEdit_2.text()
            eq_to_change.groups.clear()
            for i in self.__currEqGroupsTableContents:
                eq_to_change.groups.append(self.__allGroups[i])
            self.__equipment_list.change_equipment(eq_to_change)
        else:
            if code_error == 1:
                show_message("Ошибка изменения", "Введите название")
            elif code_error == 3:
                show_message("Ошибка изменения", "Не отмечены права для получения")
            elif code_error == 8:
                show_message("Ошибка изменения", "Уже существует оборудование с таким названием")
    def setUsInfo(self):
        if self.__usnum==0:
            self.uschangerprevPushButton.hide()
            self.uschangernextPushButton.show()

        elif self.__usnum==len(self.__usFoundTableContents) - 1:
            self.uschangernextPushButton.hide()
            self.uschangerprevPushButton.show()
        elif len(self.__usFoundTableContents)==0:
            self.uschangerprevPushButton.hide()
            self.uschangernextPushButton.hide()
        else:
            self.uschangerprevPushButton.show()
            self.uschangernextPushButton.show()
        self.usTableView.selectRow(self.__usnum)
        self.ussearchByNameOrEmailLineEdit.setText(self.__usFoundTableContents[self.__usnum][0])
        self.ussearchByEmailOrNameLineEdit.setText(self.__usFoundTableContents[self.__usnum][1])
        self.__currUsGroupsTableContents.clear()
        self.__usFoundGroups = self.__user_list.get_user_by_pass(
            int(self.__usFoundTableContents[self.__usnum][0], 16)).access.groups
        for i in self.__user_list.get_user_by_pass(int(self.__usFoundTableContents[self.__usnum][0], 16)).access.groups:
            self.__currUsGroupsTableContents.append(self.__db.get_group_by_id(i).group_name)
        data_frame = pd.DataFrame(self.__currUsGroupsTableContents, columns=["Номер группы"],
                                  index=[i for i in range(len(self.__currUsGroupsTableContents))])
        model = TableModel(data_frame)
        self.usGroupsTableView.setModel(model)
        self.usGroupsTableView.selectRow(self.__usnum)
        if len(self.__usFoundGroups) > 0:
            self.usSearchDelFromSelectedGr.show()
    def setEqInfo(self):
        if self.__eqnum==0:
            self.eqchangerprevPushButton.hide()
            self.eqchangernextPushButton.show()

        elif self.__eqnum==len(self.__eqFoundTableContents) - 1:
            self.eqchangernextPushButton.hide()
            self.eqchangerprevPushButton.show()
        elif len(self.__eqFoundTableContents)==0:
            self.eqchangerprevPushButton.hide()
            self.eqchangernextPushButton.hide()
        else:
            self.eqchangerprevPushButton.show()
            self.eqchangernextPushButton.show()
        self.eqTableView.selectRow(self.__eqnum)
        self.eqsearchByIdSpinBox.setValue(int(self.__eqFoundTableContents[self.__eqnum][0]))
        self.eqsearchByEmailOrNameLineEdit_2.setText(self.__equipment_list.get_equipment_by_id(int(self.__eqFoundTableContents[self.__eqnum][0])).description)
        self.eqsearchByEmailOrNameLineEdit.setText(self.__eqFoundTableContents[self.__eqnum][1])
        if self.__eqFoundTableContents[self.__eqnum][5] != '--':
            self.searchByHeightSpinBox.setValue(int(self.__eqFoundTableContents[self.__eqnum][5]))
        else:
            self.searchByHeightSpinBox.setValue(-1)
        if self.__eqFoundTableContents[self.__eqnum][4] != '--':
            self.searchByPosFromLeftSpinBox.setValue(int(self.__eqFoundTableContents[self.__eqnum][4]))
        else:
            self.searchByPosFromLeftSpinBox.setValue(-1)
        self.eqsearchByNumberSpinBox.setValue(int(self.__eqFoundTableContents[self.__eqnum][2]))
        self.eqsearchByReservedSpinBox.setValue(int(self.__eqFoundTableContents[self.__eqnum][3]))
        self.__eqFoundGroups = self.__equipment_list.get_equipment_by_id(
            int(self.__eqFoundTableContents[self.__eqnum][0])).groups
        self.__currEqGroupsTableContents.clear()
        for i in self.__eqFoundGroups:

            self.__currEqGroupsTableContents.append(self.__db.get_group_by_id(i).group_name)
        data_frame = pd.DataFrame(self.__currEqGroupsTableContents, columns=["Номер группы"],
                                  index=[i for i in range(len(self.__currEqGroupsTableContents))])
        model = TableModel(data_frame)
        self.eqGroupsTableView.setModel(model)
        if len(self.__eqFoundGroups) > 0:
            self.eqSearchDelFromSelectedGr.show()
    def search_users(self):
        found = []
        found2 = []
        found3 = []
        found4 = []
        foundres = []
        if self.ussearchByNameOrEmailLineEdit.text() != "":
            try:
                user_id = int(self.ussearchByNameOrEmailLineEdit.text())
                for i in self.__usTableContents:
                    if int(i[0], 16) == user_id:
                        found.append(i)
            except ValueError:
                show_message("Ошибка", "ID должен быть числом")
        if self.ussearchByEmailOrNameLineEdit.text() != "":
            for i in self.__usTableContents:
                if i[1] == self.ussearchByEmailOrNameLineEdit.text() or i[1].find(self.ussearchByEmailOrNameLineEdit.text())>=0:
                    found2.append(i)
        if self.ussearchByGroupLineEdit.text() != "" and self.ussearchByGroupLineEdit.text() in self.__allGroups.keys():
            for i in self.__user_list.get_user_by_group(self.__allGroups.get(self.ussearchByGroupLineEdit.text())):
                found4.append([
                    str(hex(i.pass_number)),
                    i.mail,
                ])
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
            if len(found3) != 0:
                foundres = [x for x in foundres if x in found4]
        if len(found4) != 0 and len(found3) == 0 and len(found2) == 0 and len(found) == 0:
            foundres = found4
        if len(foundres) != 0:
            self.usTableView.clearSpans()
            self.__usFoundTableContents = foundres
            self.__usnum = 0
            data_frame = pd.DataFrame(foundres, columns=["ID карты", "Почта"],
                                      index=[i for i in range(len(foundres))])
            model = TableModel(data_frame)
            self.usTableView.setModel(model)
            self.setUsInfo()
            if self.__admin_access.can_change_users:
                self.uschangerGroupBox.show()
                self.usGroupsTableView.show()
                self.listLabel_4.show()
                self.listLabel_2.show()
                self.usTableView.setGeometry(QtCore.QRect(870, 30, 701, 721))
                self.usSearchAllGrTableView.show()
                self.usSearchGrToSelected.show()
                self.usChangeSearchGroupsGroupBox.show()
                self.listLabel_19.show()
                self.listLabel_4.setText("Группы пользователя")
                self.usChangeDelPushButton.show()
                self.eqChangeDeleteGroupsButton.show()
        else:
            show_message("Проблема", "Ничего не найдено")
    def searchEq(self):
        found = []
        found2 = []
        found3 = []
        found4 = []
        found5 = []
        found6 = []
        found7 = []
        foundres = []
        if self.eqsearchByIdSpinBox.value() != -1:
            id = self.eqsearchByIdSpinBox.value()
            for i in self.__eqTableContents:
                if i[0] == str(id):
                    found.append(i)
                    break
        if self.eqsearchByEmailOrNameLineEdit.text() != "":
            name = self.eqsearchByEmailOrNameLineEdit.text()
            for i in self.__eqTableContents:
                if i[1] == name or i[1].find(name)>=0:
                    found2.append(i)
                    break
        if self.eqsearchByGroupLineEdit.text() != "" and self.eqsearchByGroupLineEdit.text() in self.__allGroups.keys():
            for i in self.__equipment_list.get_equipment_by_group(
                    self.__allGroups[self.eqsearchByGroupLineEdit.text()]):
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
                found3.append([
                    str(i.id),
                    str(i.title),
                    str(i.count),
                    str(i.reserve_count),
                    x,
                    y])
        if self.searchByHeightSpinBox.value() != -1:
            for i in self.__eqTableContents:
                if i[6] == str(self.searchByHeightSpinBox.value()):
                    found4.append(i)
        if self.searchByPosFromLeftSpinBox.value() != -1:
            for i in self.__eqTableContents:
                if i[5] == str(self.searchByPosFromLeftSpinBox.value()):
                    found5.append(i)
        if self.eqsearchByReservedSpinBox.value() != -1:
            for i in self.__eqTableContents:
                if i[3] == str(self.eqsearchByReservedSpinBox.value()):
                    found6.append(i)
        if self.eqsearchByNumberSpinBox.value() != -1:
            for i in self.__eqTableContents:
                if i[2] == str(self.eqsearchByNumberSpinBox.value()):
                    found7.append(i)
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
            if len(found7) != 0:
                foundres = [x for x in foundres if x in found7]
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
            if len(found7) != 0:
                foundres = [x for x in foundres if x in found7]
        if len(found3) != 0 and len(found) == 0 and len(found2) == 0:
            foundres = found3
            if len(found4) != 0:
                foundres = [x for x in foundres if x in found4]
            if len(found5) != 0:
                foundres = [x for x in foundres if x in found5]
            if len(found6) != 0:
                foundres = [x for x in foundres if x in found6]
            if len(found7) != 0:
                foundres = [x for x in foundres if x in found7]
        if len(found4) != 0:
            foundres = found4
            if len(found5) != 0:
                foundres = [x for x in foundres if x in found5]
            if len(found6) != 0:
                foundres = [x for x in foundres if x in found6]
            if len(found7) != 0:
                foundres = [x for x in foundres if x in found7]
        if len(found5) != 0:
            foundres = found5
            if len(found4) != 0:
                foundres = [x for x in foundres if x in found4]
            if len(found6) != 0:
                foundres = [x for x in foundres if x in found6]
            if len(found7) != 0:
                foundres = [x for x in foundres if x in found7]
        if len(found6) != 0 and len(found) == 0 and len(found2) == 0 and len(found3) == 0 and len(found4) == 0 and len(
                found5) == 0:
            foundres = found6
            if len(found7) != 0:
                foundres = [x for x in foundres if x in found7]
        if len(found7) != 0 and len(found) == 0 and len(found2) == 0 and len(found3) == 0 and len(found4) == 0 and len(
                found5) == 0 and len(found6) == 0:
            foundres = found7
        if len(foundres) != 0:
            self.__eqFoundTableContents = foundres
            self.eqTableView.clearSpans()
            data_frame = pd.DataFrame(foundres,
                                      columns=["ID", "Название", "Количество", "Зарезервировано", "От стены",
                                               "От пола"],
                                      index=[i for i in range(len(foundres))])
            model = TableModel(data_frame)
            self.eqTableView.setModel(model)
            self.__eqnum = 0
            self.setEqInfo()
            if self.__admin_access.can_change_inventory:
                self.eqchangerGroupBox.show()
                self.eqTableView.setGeometry(QtCore.QRect(840, 40, 781, 721))
                self.eqSearchAllGrTableView.show()
                self.eqGroupsTableView.show()
                self.eqSearchGrToSelected.show()
                self.listLabel_3.show()
                self.listLabel_20.show()
                self.eqChangeSearchGroupsGroupBox.show()
                self.eqChangeDelPushButton.show()
                self.eqChangeDeleteGroupsButton.show()
        else:
            show_message("Проблема", "Ничего не найдено")
    def search_request(self):
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
    def previousEq(self):
        if self.__eqnum > 0:
            self.__eqnum = self.__eqnum - 1
            self.setEqInfo()
        else:
            show_message("Ошибка", "Это первый элемент в списке")
    def nextEq(self):
        if self.__eqnum < len(self.__eqFoundTableContents) - 1:
            self.__eqnum = self.__eqnum + 1
            self.setEqInfo()
        else:
            show_message("Ошибка", "Элемент последний в списке")
    def previousUs(self):
        if self.__usnum > 0:
            self.__usnum = self.__usnum - 1
            self.setUsInfo()
        else:
            show_message("Ошибка", "Это первый элемент в списке")
    def nextUs(self):
        if self.__usnum < len(self.__usFoundTableContents) - 1:
            self.__usnum = self.__usnum + 1
            self.setUsInfo()
        else:
            show_message("Ошибка", "Элемент последний в списке")
    def get_request(self):
        if self.__reqnum < len(self.__reqs):
            a = "EMAIL: " + str(self.__user_list.get_user_by_id(
                self.__reqs[self.__reqnum].sender_id).mail) + "\n ID запросившего: " + str(
                self.__reqs[self.__reqnum].sender_tg_id) + "\n Что запрашивается: " + str(
                self.__equipment_list.get_equipment_by_id(
                    self.__reqs[self.__reqnum].equipment_id).title) + "\n Сколько: " + str(
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
            self.__reqs[self.__reqnum].solved = True
            self.__reqs[self.__reqnum].approved = decision
            self.__reqs[self.__reqnum].approved_id = self.__current_user.base_id
            self.__db.update_user_request(self.__reqs[self.__reqnum])
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
            return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditableFACTION
