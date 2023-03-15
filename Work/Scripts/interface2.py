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
        self.__eqTableContents = []
        self.__usTableContents = []
        self.__reqTableContents = []
        self.__usFoundTableContents = []
        self.__eqFoundTableContents = []
        self.__usFoundGroups=[]
        self.__eqFoundGroups=[]
        self.__grTableContents=[]
        self.__currUsGroupsTableContents=[]
        self.__currEqGroupsTableContents=[]
        self.__addUsTableContents=[]
        self.__addEqTableContents=[]
        self.__admin_access = admin_access  # Права админа, зашедшего в приложение
        self.__reqs = self.__db.get_unsolved_requests()
        self.__reqnum = 0
        self.__eqnum = -1
        self.__usnum = -1
        #self.eqTableView.setGeometry(QtCore.QRect(600, 40, 581, 721))
        #self.usTableView.setGeometry(QtCore.QRect(620, 30, 701, 721))
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
        self.eqaddUserOrInvButton = QtWidgets.QPushButton(parent=self.addSmthBox)
        self.eqaddUserOrInvButton.setGeometry(QtCore.QRect(10, 410, 401, 41))
        self.eqaddUserOrInvButton.setStyleSheet("QPushButton{\n"
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
        self.eqaddUserOrInvButton.setObjectName("eqaddUserOrInvButton")
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
        self.eqDelFromSelectedGr.setGeometry(QtCore.QRect(630, 330, 61, 41))
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
        self.eqAddGroupByNameSpinBox = QtWidgets.QLineEdit(parent=self.addSmthBox)
        self.eqAddGroupByNameSpinBox.setGeometry(QtCore.QRect(180, 280, 191, 22))
        self.eqAddGroupByNameSpinBox.setObjectName("eqAddGroupByNameSpinBox")
        self.searchByEmailOrNameLabel_4 = QtWidgets.QLabel(parent=self.addSmthBox)
        self.searchByEmailOrNameLabel_4.setGeometry(QtCore.QRect(20, 280, 161, 16))
        self.searchByEmailOrNameLabel_4.setObjectName("searchByEmailOrNameLabel_4")
        self.eqRefreshGroupButton = QtWidgets.QPushButton(parent=self.addSmthBox)
        self.eqRefreshGroupButton.setGeometry(QtCore.QRect(10, 360, 401, 41))
        self.eqRefreshGroupButton.setStyleSheet("QPushButton{\n"
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
        self.eqRefreshGroupButton.setObjectName("eqRefreshGroupButton")
        self.eqAddAllGrTableView = QtWidgets.QTableView(parent=self.addSmthBox)
        self.eqAddAllGrTableView.setGeometry(QtCore.QRect(700, 20, 421, 681))
        self.eqAddAllGrTableView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.eqAddAllGrTableView.setObjectName("eqAddAllGrTableView")
        self.eqAddSelectedGrTableView = QtWidgets.QTableView(parent=self.addSmthBox)
        self.eqAddSelectedGrTableView.setGeometry(QtCore.QRect(450, 20, 171, 681))
        self.eqAddSelectedGrTableView.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.eqAddSelectedGrTableView.setObjectName("eqAddSelectedGrTableView")
        self.eqGrToSelected = QtWidgets.QPushButton(parent=self.addSmthBox)
        self.eqGrToSelected.setGeometry(QtCore.QRect(630, 380, 61, 41))
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
        self.eqRefreshGroupButton_2 = QtWidgets.QPushButton(parent=self.addSmthBox)
        self.eqRefreshGroupButton_2.setGeometry(QtCore.QRect(10, 310, 401, 41))
        self.eqRefreshGroupButton_2.setStyleSheet("QPushButton{\n"
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
        self.eqRefreshGroupButton_2.setObjectName("eqRefreshGroupButton_2")
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
        self.usaddUserOrInvButton = QtWidgets.QPushButton(parent=self.addSmthBox_2)
        self.usaddUserOrInvButton.setGeometry(QtCore.QRect(30, 490, 401, 41))
        self.usaddUserOrInvButton.setStyleSheet("QPushButton{\n"
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
        self.usaddUserOrInvButton.setObjectName("usaddUserOrInvButton")
        self.searchByEmailOrNameLabel_3 = QtWidgets.QLabel(parent=self.addSmthBox_2)
        self.searchByEmailOrNameLabel_3.setGeometry(QtCore.QRect(40, 360, 161, 16))
        self.searchByEmailOrNameLabel_3.setObjectName("searchByEmailOrNameLabel_3")
        self.usAddGroupByNameSpinBox = QtWidgets.QLineEdit(parent=self.addSmthBox_2)
        self.usAddGroupByNameSpinBox.setGeometry(QtCore.QRect(200, 360, 191, 22))
        self.usAddGroupByNameSpinBox.setObjectName("usAddGroupByNameSpinBox")
        self.usSearchGroupButton = QtWidgets.QPushButton(parent=self.addSmthBox_2)
        self.usSearchGroupButton.setGeometry(QtCore.QRect(30, 390, 401, 41))
        self.usSearchGroupButton.setStyleSheet("QPushButton{\n"
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
        self.usSearchGroupButton.setObjectName("usSearchGroupButton")
        self.usRefreshGroupButton = QtWidgets.QPushButton(parent=self.addSmthBox_2)
        self.usRefreshGroupButton.setGeometry(QtCore.QRect(30, 440, 401, 41))
        self.usRefreshGroupButton.setStyleSheet("QPushButton{\n"
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
        self.usRefreshGroupButton.setObjectName("usRefreshGroupButton")
        self.usDelFromSelectedGr = QtWidgets.QPushButton(parent=self.addSmthBox_2)
        self.usDelFromSelectedGr.setGeometry(QtCore.QRect(660, 320, 61, 41))
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
        self.usGrToSelected.setGeometry(QtCore.QRect(660, 370, 61, 41))
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
        self.usAddSelectedGrTableView.setGeometry(QtCore.QRect(480, 10, 171, 681))
        self.usAddSelectedGrTableView.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.usAddSelectedGrTableView.setObjectName("usAddSelectedGrTableView")
        self.usAddAllGrTableView = QtWidgets.QTableView(parent=self.addSmthBox_2)
        self.usAddAllGrTableView.setGeometry(QtCore.QRect(730, 10, 431, 681))
        self.usAddAllGrTableView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.usAddAllGrTableView.setObjectName("usAddAllGrTableView")
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
        self.grAddPushButton.setGeometry(QtCore.QRect(20, 90, 401, 41))
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
        self.grTableView.setGeometry(QtCore.QRect(440, 40, 661, 661))
        self.grTableView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.grTableView.setObjectName("grTableView")
        self.grSearchPushButton = QtWidgets.QPushButton(parent=self.tab_16)
        self.grSearchPushButton.setGeometry(QtCore.QRect(20, 140, 401, 41))
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
        self.listLabel_13.setGeometry(QtCore.QRect(440, 10, 161, 20))
        self.listLabel_13.setObjectName("listLabel_13")
        self.tabWidget.addTab(self.tab_16, "")
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
        self.eqsearchByIdSpinBox.setGeometry(QtCore.QRect(30, 30, 271, 22))
        self.eqsearchByIdSpinBox.setObjectName("eqsearchByIdSpinBox")
        self.eqsearchByEmailOrNameLineEdit = QtWidgets.QLineEdit(parent=self.viewInvOrUserBox)
        self.eqsearchByEmailOrNameLineEdit.setGeometry(QtCore.QRect(90, 60, 211, 22))
        self.eqsearchByEmailOrNameLineEdit.setObjectName("eqsearchByEmailOrNameLineEdit")
        self.listLabel = QtWidgets.QLabel(parent=self.viewInvOrUserBox)
        self.listLabel.setGeometry(QtCore.QRect(840, 20, 351, 16))
        self.listLabel.setObjectName("listLabel")
        self.searchByPosGroupBox = QtWidgets.QGroupBox(parent=self.viewInvOrUserBox)
        self.searchByPosGroupBox.setGeometry(QtCore.QRect(10, 190, 441, 61))
        self.searchByPosGroupBox.setStyleSheet("QGroupBox#searchByPosGroupBox{\n"
                                               "    border: 0;\n"
                                               "}")
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
        self.eqsearchPushButton.setGeometry(QtCore.QRect(40, 260, 351, 28))
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
        self.eqViewRefreshPushButton = QtWidgets.QPushButton(parent=self.viewInvOrUserBox)
        self.eqViewRefreshPushButton.setGeometry(QtCore.QRect(40, 300, 351, 28))
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
        self.eqchangerGroupBox = QtWidgets.QGroupBox(parent=self.viewInvOrUserBox)
        self.eqchangerGroupBox.setGeometry(QtCore.QRect(30, 330, 371, 91))
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
        self.eqsearchByNumberSpinBox = QtWidgets.QSpinBox(parent=self.viewInvOrUserBox)
        self.eqsearchByNumberSpinBox.setGeometry(QtCore.QRect(110, 130, 191, 22))
        self.eqsearchByNumberSpinBox.setObjectName("eqsearchByNumberSpinBox")
        self.eqsearchByIdLabel_2 = QtWidgets.QLabel(parent=self.viewInvOrUserBox)
        self.eqsearchByIdLabel_2.setGeometry(QtCore.QRect(10, 130, 81, 16))
        self.eqsearchByIdLabel_2.setObjectName("eqsearchByIdLabel_2")
        self.eqsearchByReservedSpinBox = QtWidgets.QSpinBox(parent=self.viewInvOrUserBox)
        self.eqsearchByReservedSpinBox.setGeometry(QtCore.QRect(160, 160, 141, 22))
        self.eqsearchByReservedSpinBox.setObjectName("eqsearchByReservedSpinBox")
        self.eqsearchByIdLabel_3 = QtWidgets.QLabel(parent=self.viewInvOrUserBox)
        self.eqsearchByIdLabel_3.setGeometry(QtCore.QRect(10, 160, 131, 16))
        self.eqsearchByIdLabel_3.setObjectName("eqsearchByIdLabel_3")
        self.eqGroupsTableView = QtWidgets.QTableView(parent=self.viewInvOrUserBox)
        self.eqGroupsTableView.setGeometry(QtCore.QRect(420, 40, 171, 721))
        self.eqGroupsTableView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.eqGroupsTableView.setObjectName("eqGroupsTableView")
        self.listLabel_3 = QtWidgets.QLabel(parent=self.viewInvOrUserBox)
        self.listLabel_3.setGeometry(QtCore.QRect(420, 20, 161, 20))
        self.listLabel_3.setObjectName("listLabel_3")
        self.eqsearchByIdLabel_18 = QtWidgets.QLabel(parent=self.viewInvOrUserBox)
        self.eqsearchByIdLabel_18.setGeometry(QtCore.QRect(10, 90, 81, 21))
        self.eqsearchByIdLabel_18.setObjectName("eqsearchByIdLabel_18")
        self.eqsearchByGroupIdSpinBox = QtWidgets.QSpinBox(parent=self.viewInvOrUserBox)
        self.eqsearchByGroupIdSpinBox.setGeometry(QtCore.QRect(100, 90, 201, 22))
        self.eqsearchByGroupIdSpinBox.setObjectName("eqsearchByGroupIdSpinBox")
        self.eqCreateStatsPushButton = QtWidgets.QPushButton(parent=self.viewInvOrUserBox)
        self.eqCreateStatsPushButton.setGeometry(QtCore.QRect(20, 470, 231, 28))
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
        self.eqCreateStatsSpinBox.setGeometry(QtCore.QRect(270, 470, 111, 22))
        self.eqCreateStatsSpinBox.setObjectName("eqCreateStatsSpinBox")
        self.label_42 = QtWidgets.QLabel(parent=self.viewInvOrUserBox)
        self.label_42.setGeometry(QtCore.QRect(260, 450, 141, 16))
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
        self.eqSearchAllGrTableView.setGeometry(QtCore.QRect(670, 40, 161, 721))
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
        self.tabWidget.addTab(self.tab_3, "")
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
        self.ussearchByEmailOrNameLineEdit.setGeometry(QtCore.QRect(80, 60, 161, 22))
        self.ussearchByEmailOrNameLineEdit.setObjectName("ussearchByEmailOrNameLineEdit")
        self.usTableView = QtWidgets.QTableView(parent=self.viewInvOrUserBox_2)
        self.usTableView.setGeometry(QtCore.QRect(870, 30, 701, 721))
        self.usTableView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.usTableView.setObjectName("usTableView")
        self.ussearchByNameOrEmailLineEdit = QtWidgets.QLineEdit(parent=self.viewInvOrUserBox_2)
        self.ussearchByNameOrEmailLineEdit.setGeometry(QtCore.QRect(170, 30, 261, 22))
        self.ussearchByNameOrEmailLineEdit.setObjectName("ussearchByNameOrEmailLineEdit")
        self.ussearchPushButton = QtWidgets.QPushButton(parent=self.viewInvOrUserBox_2)
        self.ussearchPushButton.setGeometry(QtCore.QRect(20, 220, 351, 28))
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
        self.usViewRefreshPushButton.setGeometry(QtCore.QRect(20, 260, 351, 28))
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
        self.uschangerGroupBox.setGeometry(QtCore.QRect(10, 120, 371, 91))
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
        self.usGroupsTableView = QtWidgets.QTableView(parent=self.viewInvOrUserBox_2)
        self.usGroupsTableView.setGeometry(QtCore.QRect(440, 30, 171, 721))
        self.usGroupsTableView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.usGroupsTableView.setObjectName("usGroupsTableView")
        self.listLabel_4 = QtWidgets.QLabel(parent=self.viewInvOrUserBox_2)
        self.listLabel_4.setGeometry(QtCore.QRect(440, 10, 161, 20))
        self.listLabel_4.setObjectName("listLabel_4")
        self.ussearchByGroupIdSpinBox = QtWidgets.QSpinBox(parent=self.viewInvOrUserBox_2)
        self.ussearchByGroupIdSpinBox.setGeometry(QtCore.QRect(90, 90, 161, 22))
        self.ussearchByGroupIdSpinBox.setObjectName("ussearchByGroupIdSpinBox")
        self.eqsearchByIdLabel_11 = QtWidgets.QLabel(parent=self.viewInvOrUserBox_2)
        self.eqsearchByIdLabel_11.setGeometry(QtCore.QRect(10, 90, 81, 21))
        self.eqsearchByIdLabel_11.setObjectName("eqsearchByIdLabel_11")
        self.eqCreateStatsSpinBox_2 = QtWidgets.QSpinBox(parent=self.viewInvOrUserBox_2)
        self.eqCreateStatsSpinBox_2.setGeometry(QtCore.QRect(270, 320, 111, 22))
        self.eqCreateStatsSpinBox_2.setObjectName("eqCreateStatsSpinBox_2")
        self.label_43 = QtWidgets.QLabel(parent=self.viewInvOrUserBox_2)
        self.label_43.setGeometry(QtCore.QRect(260, 300, 141, 16))
        self.label_43.setObjectName("label_43")
        self.eqCreateStatsPushButton_2 = QtWidgets.QPushButton(parent=self.viewInvOrUserBox_2)
        self.eqCreateStatsPushButton_2.setGeometry(QtCore.QRect(20, 320, 231, 28))
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
        self.usSearchAllGrTableView.setGeometry(QtCore.QRect(690, 30, 161, 721))
        self.usSearchAllGrTableView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.usSearchAllGrTableView.setObjectName("usSearchAllGrTableView")
        self.listLabel_19 = QtWidgets.QLabel(parent=self.viewInvOrUserBox_2)
        self.listLabel_19.setGeometry(QtCore.QRect(690, 10, 161, 20))
        self.listLabel_19.setObjectName("listLabel_19")
        self.tabWidget.addTab(self.tab_4, "")
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
        self.setCentralWidget(self.centralwidget)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)

        _translate = QtCore.QCoreApplication.translate
        self.nameOrEmailLabel_2.setText(_translate("MainWindow", "Название"))
        self.eqaddUserOrInvButton.setText(_translate("MainWindow", "Добавить"))
        self.label_27.setText(_translate("MainWindow", "Номер от левого края"))
        self.label_12.setText(_translate("MainWindow", "Описание"))
        self.label_11.setText(_translate("MainWindow", "Доступное количество"))
        self.label_26.setText(_translate("MainWindow", "Высота(от пола)"))
        self.label_10.setText(_translate("MainWindow", "Зарезервированное  количество"))
        self.radioButton_setPos.setText(_translate("MainWindow", "Указать расположение в шкафу"))
        self.eqDelFromSelectedGr.setText(_translate("MainWindow", "==>"))
        self.searchByEmailOrNameLabel_4.setText(_translate("MainWindow", "Название группы"))
        self.eqRefreshGroupButton.setText(_translate("MainWindow", "Вернуть полный список групп"))
        self.eqGrToSelected.setText(_translate("MainWindow", "<=="))
        self.eqRefreshGroupButton_2.setText(_translate("MainWindow", "Поиск групп"))
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
        self.usaddUserOrInvButton.setText(_translate("MainWindow", "Добавить"))
        self.searchByEmailOrNameLabel_3.setText(_translate("MainWindow", "Название группы"))
        self.usSearchGroupButton.setText(_translate("MainWindow", "Поиск группы"))
        self.usRefreshGroupButton.setText(_translate("MainWindow", "Вернуть полный список групп"))
        self.usDelFromSelectedGr.setText(_translate("MainWindow", "==>"))
        self.usGrToSelected.setText(_translate("MainWindow", "<=="))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2),
                                  _translate("MainWindow", "Добавление пользователей"))
        self.nameOrEmailLabel_8.setText(_translate("MainWindow", "Название"))
        self.grAddPushButton.setText(_translate("MainWindow", "Добавить"))
        self.grSearchPushButton.setText(_translate("MainWindow", "Найти"))
        self.listLabel_13.setText(_translate("MainWindow", "Все группы"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_16), _translate("MainWindow", "Добавление групп"))
        self.eqsearchByIdLabel.setText(_translate("MainWindow", "ID"))
        self.searchByEmailOrNameLabel.setText(_translate("MainWindow", "Название"))
        self.listLabel.setText(_translate("MainWindow", "Все/найденные элементы оборудования в базе"))
        self.searchByPosGroupBox.setTitle(_translate("MainWindow", "Поиск по расположению в шкафу"))
        self.label_36.setText(_translate("MainWindow", "Высота(от пола)"))
        self.label_37.setText(_translate("MainWindow", "Номер от левого края"))
        self.eqsearchPushButton.setText(_translate("MainWindow", " Поиск"))
        self.eqViewRefreshPushButton.setText(_translate("MainWindow", "Обновить таблицу"))
        self.eqchangernextPushButton.setText(_translate("MainWindow", "Следующий"))
        self.eqchangerprevPushButton.setText(_translate("MainWindow", "Предыдущий"))
        self.eqcommitchangesPushButton.setText(_translate("MainWindow", "Принять изменения"))
        self.eqsearchByIdLabel_2.setText(_translate("MainWindow", "Количество"))
        self.eqsearchByIdLabel_3.setText(_translate("MainWindow", "Зарезервировано"))
        self.listLabel_3.setText(_translate("MainWindow", "Группы оборудования"))
        self.eqsearchByIdLabel_18.setText(_translate("MainWindow", "ID группы"))
        self.eqCreateStatsPushButton.setText(_translate("MainWindow", "Выгрузить статистику в файл"))
        self.label_42.setText(_translate("MainWindow", "количество дней"))
        self.eqSearchDelFromSelectedGr.setText(_translate("MainWindow", "==>"))
        self.eqSearchGrToSelected.setText(_translate("MainWindow", "<=="))
        self.listLabel_20.setText(_translate("MainWindow", "Все группы"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Просмотр инвентаря"))
        self.searchByIdLabel_2.setText(_translate("MainWindow", "ID карты пропуска"))
        self.searchByEmailOrNameLabel_2.setText(_translate("MainWindow", "Email"))
        self.ussearchPushButton.setText(_translate("MainWindow", " Поиск"))
        self.usViewRefreshPushButton.setText(_translate("MainWindow", "Обновить таблицу"))
        self.uschangernextPushButton.setText(_translate("MainWindow", "Следующий"))
        self.uschangerprevPushButton.setText(_translate("MainWindow", "Предыдущий"))
        self.uscommitchangesPushButton.setText(_translate("MainWindow", "Принять изменения"))
        self.listLabel_4.setText(_translate("MainWindow", "Группы пользователя"))
        self.eqsearchByIdLabel_11.setText(_translate("MainWindow", "ID группы"))
        self.label_43.setText(_translate("MainWindow", "количество дней"))
        self.eqCreateStatsPushButton_2.setText(_translate("MainWindow", "Выгрузить статистику в файл"))
        self.listLabel_2.setText(_translate("MainWindow", "Все/найденные элементы оборудования в базе"))
        self.usSearchGrToSelected.setText(_translate("MainWindow", "<=="))
        self.usSearchDelFromSelectedGr.setText(_translate("MainWindow", "==>"))
        self.listLabel_19.setText(_translate("MainWindow", "Все группы"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4),
                                  _translate("MainWindow", "Просмотр пользователей"))
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
        self.eqchangernextPushButton.clicked.connect(self.nextEq)
        self.eqchangerprevPushButton.clicked.connect(self.previousEq)
        self.uschangernextPushButton.clicked.connect(self.nextUs)
        self.uschangerprevPushButton.clicked.connect(self.previousUs)
        # self.uscommitchangesPushButton.clicked.connect(self.testForButton)
        # self.uscommitchangesPushButton.doubleClicked.connect(self.testForDCButton)
        self.uscommitchangesPushButton.clicked.connect(self.changeUs)
        self.eqcommitchangesPushButton.clicked.connect(self.changeEq)
        self.eqGrToSelected.clicked.connect(self.selected_to_eq_groups)
        self.usGrToSelected.clicked.connect(self.selected_to_us_groups)
        self.usDelFromSelectedGr.clicked.connect(self.del_from_us_selected_groups)
        self.eqDelFromSelectedGr.clicked.connect(self.del_from_eq_selected_groups)
        self.grAddPushButton.clicked.connect(self.add_group)
       # self.grSearchPushButton.clicked.connect(self.search_gr)
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
        self.refresh_gr_view_table()
        self.refresh_requests_table()
        self.refresh_equipment_table()
        self.refresh_users_table()
        self.eqDelFromSelectedGr.hide()
        self.usDelFromSelectedGr.hide()
        self.eqSearchDelFromSelectedGr.hide()
        self.usSearchDelFromSelectedGr.hide()
        self.show()
    def add_group(self):
        code_error = -1
        if self.grAddLineEdit.text()=='':
            code_error = 2
        elif self.__db.get_group_by_name(self.grAddLineEdit.text())!=None:
            code_error =4
        if code_error == -1:
            self.__db.add_group(self.grAddLineEdit.text())
            self.refresh_gr_view_table()
        elif code_error == 2:
            show_message("Ошибка добавления", "Введите название группы")
        elif code_error == 4:
            show_message("Ошибка добавления", "Группа с таким названием уже есть в базе")
   # def search_gr(self):
        #indexes = self.grTableView.selectionModel().selectedRows()
        #for i in indexes:
    def refresh_gr_view_table(self):
        self.grTableView.clearSpans()
        self.eqAddAllGrTableView.clearSpans()
        self.usAddAllGrTableView.clearSpans()
        self.eqAddAllGrTableView.clearSpans()
        self.usAddAllGrTableView.clearSpans()
        self.usSearchAllGrTableView.clearSpans()
        self.eqSearchAllGrTableView.clearSpans()
        for i in self.__db.get_all_groups():
            self.__grTableContents.append(
                str(i.group_name))
        data_frame = pd.DataFrame(self.__grTableContents,
                                  columns=["Название группы"],
                                  index=[i for i in range(len(self.__grTableContents))])
        model = TableModel(data_frame)
        self.grTableView.setModel(model)
        self.eqAddAllGrTableView.setModel(model)
        self.usAddAllGrTableView.setModel(model)
        self.eqAddAllGrTableView.setModel(model)
        self.usAddAllGrTableView.setModel(model)
        self.usSearchAllGrTableView.setModel(model)
        self.eqSearchAllGrTableView.setModel(model)
    def selected_to_us_groups(self):
        indexes = self.usAddAllGrTableView.selectionModel().selectedRows()
        if len(indexes)>0:
            for i in indexes:
                if self.__grTableContents[i.row()] not in self.__addUsTableContents:
                    self.__addUsTableContents.append(self.__grTableContents[i.row()])
            self.refresh_selected_us_groups()
            self.usDelFromSelectedGr.show()
    def selected_to_eq_search_groups(self):
        indexes = self.eqSearchAllGrTableView.selectionModel().selectedRows()
        if len(indexes) > 0:
            for i in indexes:
                if self.__grTableContents[i.row()] not in self.__currEqGroupsTableContents:
                    self.__currEqGroupsTableContents.append(self.__grTableContents[i.row()])
            self.refresh_selected_eq_search_groups()
            self.eqSearchDelFromSelectedGr.show()
    def selected_to_us_search_groups(self):
        indexes = self.usSearchAllGrTableView.selectionModel().selectedRows()
        if len(indexes) > 0:
            for i in indexes:
                if self.__grTableContents[i.row()] not in self.__currUsGroupsTableContents:
                    self.__currUsGroupsTableContents.append(self.__grTableContents[i.row()])
                    print(self.__currUsGroupsTableContents)
            self.refresh_selected_us_search_groups()
            self.usSearchDelFromSelectedGr.show()
    def selected_to_eq_groups(self):
        indexes = self.eqAddAllGrTableView.selectionModel().selectedRows()
        if len(indexes) > 0:
            for i in indexes:
                if self.__grTableContents[i.row()] not in self.__addEqTableContents:
                    self.__addEqTableContents.append(self.__grTableContents[i.row()])
            self.refresh_selected_eq_groups()
            self.eqDelFromSelectedGr.show()
    def del_from_eq_search_selected_groups(self):
        indexes = self.eqGroupsTableView.selectionModel().selectedRows()
        if len(indexes) > 0:
            for i in indexes:
                self.__currEqGroupsTableContents.pop(i.row())
            self.refresh_selected_eq_search_groups()
        if len(self.__currEqGroupsTableContents)==0:
            self.eqSearchDelFromSelectedGr.hide()###
    def del_from_us_search_selected_groups(self):
        indexes = self.usGroupsTableView.selectionModel().selectedRows()
        if len(indexes) > 0:
            for i in indexes:
                self.__currUsGroupsTableContents.pop(i.row())
            self.refresh_selected_us_search_groups()
        if len(self.__currUsGroupsTableContents)==0:
            self.usSearchDelFromSelectedGr.hide()
    def del_from_eq_selected_groups(self):
        indexes = self.eqAddSelectedGrTableView.selectionModel().selectedRows()
        if len(indexes) > 0:
            for i in indexes:
                self.__addEqTableContents.pop(i.row())
            self.refresh_selected_eq_groups()
        if len(self.__addEqTableContents)==0:
            self.eqDelFromSelectedGr.hide()
    def del_from_us_selected_groups(self):
        indexes = self.usAddSelectedGrTableView.selectionModel().selectedRows()
        if len(indexes) > 0:
            for i in indexes:
                self.__addUsTableContents.pop(i.row())
            self.refresh_selected_us_groups()
        if len(self.__addUsTableContents)==0:
            self.usDelFromSelectedGr.hide()
    def refresh_selected_us_groups(self):
        self.usAddSelectedGrTableView.clearSpans()
        data_frame = pd.DataFrame(self.__addUsTableContents,
                                  columns=["Название групп"],
                                  index=[i for i in range(len(self.__addUsTableContents))])
        model = TableModel(data_frame)
        self.usAddSelectedGrTableView.setModel(model)
    def refresh_selected_eq_groups(self):
        self.eqAddSelectedGrTableView.clearSpans()
        data_frame = pd.DataFrame(self.__addEqTableContents,
                                  columns=["Название групп"],
                                  index=[i for i in range(len(self.__addEqTableContents))])
        model = TableModel(data_frame)
        self.eqAddSelectedGrTableView.setModel(model)
    def refresh_selected_eq_search_groups(self):
        self.eqGroupsTableView.clearSpans()
        data_frame = pd.DataFrame(self.__currEqGroupsTableContents,
                                  columns=["Название групп"],
                                  index=[i for i in range(len(self.__currEqGroupsTableContents))])
        model = TableModel(data_frame)
        self.eqGroupsTableView.setModel(model)
    def refresh_selected_us_search_groups(self):
        self.usGroupsTableView.clearSpans()
        data_frame = pd.DataFrame(self.__currUsGroupsTableContents,
                                  columns=["Название групп"],
                                  index=[i for i in range(len(self.__currUsGroupsTableContents))])
        model = TableModel(data_frame)
        self.usGroupsTableView.setModel(model)
    def add_equipment(self):
        code_error = -1
        if code_error == -1 and self.eqNameOrEmailLineEdit.text() == "":
            code_error = 1
        elif self.__db.get_equipment_by_title(self.eqNameOrEmailLineEdit.text()):
            code_error = 8
        if code_error == -1 and self.descriptionTextEdit.toPlainText() == "":
            code_error = 3
        from_left = self.posFromLeftSpinBox.value()
        if self.posFromLeftSpinBox.value() == 0 or self.posFromLeftSpinBox.value() == -1:
            from_left = -1
        height = self.heightSpinBox.value()
        if self.heightSpinBox.value() == 0 or self.heightSpinBox.value() == -1:
            height = -1
        if code_error == -1 and self.__db.get_equipment_by_coordinates(from_left, height) is not None:
            code_error = 9
        if code_error == -1:
            groups=[]
            for i in self.__addEqTableContents:
                groups.append(self.__db.get_group_by_name(i).id)
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
        if code_error == -1 and self.__db.get_user_by_id(int(self.usIdCardLineEdit.text(), 16)) is not None:
            code_error = 7
        if code_error == -1 and self.__db.get_user_by_mail(self.usnameOrEmailLineEdit.text()) is not None:
            code_error = 8
        if code_error == -1:
            if self.usradioButton_User.isChecked():
                groups=[]
                for i in self.__addUsTableContents:
                    groups.append(self.__db.get_group_by_name(i).id)
                ac=Access(groups)
                us = CommonUser(int(self.usIdCardLineEdit.text(), 16), str(self.usnameOrEmailLineEdit.text()), ac)
                self.__user_list.append_user(us)
            if self.usradioButton_Admin.isChecked():
                ac = AdminAccess([], add_users, change_users, add_equipment, change_equipment, get_request)
                adm = Admin(int(self.usIdCardLineEdit.text(), 16), str(self.usnameOrEmailLineEdit.text()), ac)
                self.__user_list.append_user(adm)
            self.heightSpinBox.setValue(-1)
            self.posFromLeftSpinBox.setValue(-1)
            self.usnameOrEmailLineEdit.setText("")
            self.descriptionTextEdit.setText("")
            self.usIdCardLineEdit.setText("")
            self.refresh_users_table()
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
    def changeUs(self):
        code_error = -1
        if code_error == -1 and (self.__db.get_user_by_id(
                int(self.ussearchByNameOrEmailLineEdit.text(), 16)) is not None) and \
                self.__db.get_user_by_id(int(self.ussearchByNameOrEmailLineEdit.text(), 16)).mail != self.__usFoundTableContents[self.__usnum][
            1]:
            code_error = 7
        if code_error == -1 and (self.__db.get_user_by_mail(
                self.ussearchByEmailOrNameLineEdit.text()) is not None) and self.__db.get_user_by_mail(
                self.ussearchByEmailOrNameLineEdit.text()).id != int(self.__usFoundTableContents[self.__usnum][0],
                                                                       16):
            code_error = 8
        if code_error == -1:
            user_to_change = self.__user_list.get_user_by_id(int(self.__usFoundTableContents[self.__usnum][0], 16))
            user_to_change.id = int(self.ussearchByNameOrEmailLineEdit.text(), 16)
            user_to_change.mail = self.ussearchByEmailOrNameLineEdit.text()
            user_to_change.access.groups.clear()
            for i in self.__currUsGroupsTableContents:
                    user_to_change.access.groups.append(self.__db.get_group_by_name(i).id)
            self.__user_list.change_user(int(self.__usFoundTableContents[self.__usnum][0], 16),
                                         self.__usFoundTableContents[self.__usnum][1],
                                         user_to_change)
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
        if code_error == -1 and (self.__db.get_equipment_by_title(self.eqsearchByEmailOrNameLineEdit.text()) is not None) and self.__db.get_equipment_by_title(self.eqsearchByEmailOrNameLineEdit.text()).id != int(self.__eqFoundTableContents[self.__eqnum][0]):
            code_error = 7
        if code_error == -1:
            eq_to_change = self.__equipment_list.get_equipment_by_id(int(self.__eqFoundTableContents[self.__eqnum][0]))
            eq_to_change.title = self.eqsearchByEmailOrNameLineEdit.text()
            #eq_to_change.access = tg
            if self.eqsearchByNumberSpinBox.value()>-1:
                eq_to_change.count=self.reqsearchByCount.value()
            else:
                eq_to_change.count=0
            if self.eqsearchByReservedSpinBox.value() > -1:
                eq_to_change.count = self.reqsearchByCount.value()
            else:
                eq_to_change.reserve_count = 0
            eq_to_change.groups.clear()
            for i in self.__currEqGroupsTableContents:
                eq_to_change.groups.append(self.__db.get_group_by_name(i).id)
            self.__equipment_list.change_equipment(eq_to_change)
        else:
            if code_error == 1:
                show_message("Ошибка изменения", "Введите название")
            elif code_error == 3:
                show_message("Ошибка изменения", "Не отмечены права для получения")
            elif code_error == 8:
                show_message("Ошибка изменения", "Уже существует оборудование с таким названием")
    def refresh_equipment_table(self):
        self.eqchangerGroupBox.hide()
        self.__eqFoundTableContents = []
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
    def refresh_users_table(self):
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
        self.ussearchByGroupIdSpinBox.setValue(-1)
        self.ussearchByNameOrEmailLineEdit.setText("")
        self.ussearchByEmailOrNameLineEdit.setText("")
    def search_users(self):
        found = []
        found2 = []
        found3 = []
        found4 = []
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
        if self.ussearchByGroupIdSpinBox.value()!=0:
            for i in self.__user_list.get_user_by_group(int(self.ussearchByGroupIdSpinBox.value())):
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
        else:
            show_message("Проблема", "Ничего не найдено")
    def setUsInfo(self):
        self.usTableView.selectRow(self.__usnum)
        self.ussearchByNameOrEmailLineEdit.setText(self.__usFoundTableContents[self.__usnum][0])
        self.ussearchByEmailOrNameLineEdit.setText(self.__usFoundTableContents[self.__usnum][1])
        self.__currUsGroupsTableContents.clear()
        self.__usFoundGroups=self.__user_list.get_user_by_id(int(self.__usFoundTableContents[self.__usnum][0], 16)).access.groups
        for i in self.__user_list.get_user_by_id(int(self.__usFoundTableContents[self.__usnum][0], 16)).access.groups:
            self.__currUsGroupsTableContents.append(self.__db.get_group_by_id(i).group_name)
        data_frame = pd.DataFrame(self.__currUsGroupsTableContents, columns=["Номер группы"],
                                  index=[i for i in range(len(self.__currUsGroupsTableContents))])
        model = TableModel(data_frame)
        self.usGroupsTableView.setModel(model)
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
                if i[0] == str(self.eqsearchByIdSpinBox.value()):
                    found.append(i)
        if self.eqsearchByEmailOrNameLineEdit.text() != "":
            name = self.eqsearchByEmailOrNameLineEdit.text()
            for i in self.__eqTableContents:
                if i[1] == self.eqsearchByEmailOrNameLineEdit.text():
                    found2.append(i)
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
            #if len(found3) != 0:
               # foundres = [x for x in foundres if x in found3]
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
            #if len(found3) != 0:
               # foundres = [x for x in foundres if x in found3]
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
                                      columns=["ID", "Название", "Количество", "Зарезервировано", "От стены", "От пола"],
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
        else:
            show_message("Проблема", "Ничего не найдено")
    def setEqInfo(self):
        self.eqTableView.selectRow(self.__eqnum)
        self.eqsearchByIdSpinBox.setValue(int(self.__eqFoundTableContents[self.__eqnum][0]))
        self.eqsearchByEmailOrNameLineEdit.setText(self.__eqFoundTableContents[self.__eqnum][1])
        if self.__eqFoundTableContents[self.__eqnum][5] != '--':
            self.searchByHeightSpinBox.setValue(int(self.__eqFoundTableContents[self.__eqnum][6]))
        else:
            self.searchByHeightSpinBox.setValue(-1)
        if self.__eqFoundTableContents[self.__eqnum][4] != '--':
            self.searchByPosFromLeftSpinBox.setValue(int(self.__eqFoundTableContents[self.__eqnum][5]))
        else:
            self.searchByPosFromLeftSpinBox.setValue(-1)
        self.eqsearchByNumberSpinBox.setValue(int(self.__eqFoundTableContents[self.__eqnum][2]))
        self.eqsearchByReservedSpinBox.setValue(int(self.__eqFoundTableContents[self.__eqnum][3]))
        self.__eqFoundGroups = self.__equipment_list.get_equipment_by_id(
            int(self.__eqFoundTableContents[self.__usnum][0])).groups
        self.__currEqGroupsTableContents.clear()
        for i in self.__eqFoundGroups:
            self.__currEqGroupsTableContents.append(self.__db.get_group_by_id(i).group_name)
        data_frame = pd.DataFrame(self.__currEqGroupsTableContents, columns=["Номер группы"],
                                  index=[i for i in range(len(self.__currEqGroupsTableContents))])
        print(self.__currEqGroupsTableContents)
        model = TableModel(data_frame)
        self.eqGroupsTableView.setModel(model)
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
            return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditableFACTION
