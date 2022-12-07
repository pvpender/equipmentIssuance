"""from PyQt6.QtWidgets import QMainWindow, QLineEdit, QPushButton, QLabel, QFrame, QMessageBox
from PyQt6 import QtCore, QtGui, QtWidgets
from user_collections import *
from equipment import *
from users import *
from accesses import *


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
        self.__addingEq = False  # либо добавляет оборудование, либо пользователя
        self.__viewingEq = False  # аналогично с просмотром
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
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, 1181, 921))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.addSmthBox = QtWidgets.QGroupBox(self.groupBox)
        self.addSmthBox.setGeometry(QtCore.QRect(370, 40, 401, 431))
        self.addSmthBox.setObjectName("addSmthBox")
        self.label = QtWidgets.QLabel(self.addSmthBox)
        self.label.setGeometry(QtCore.QRect(10, 30, 61, 21))
        self.label.setText("")
        self.label.setObjectName("label")
        self.nameOrEmailLabel = QtWidgets.QLabel(self.addSmthBox)
        self.nameOrEmailLabel.setGeometry(QtCore.QRect(10, 30, 61, 16))
        self.nameOrEmailLabel.setObjectName("nameOrEmailLabel")
        self.nameOrEmailLineEdit = QtWidgets.QLineEdit(self.addSmthBox)
        self.nameOrEmailLineEdit.setGeometry(QtCore.QRect(80, 30, 311, 22))
        self.nameOrEmailLineEdit.setObjectName("nameOrEmailLineEdit")
        self.rightsLabel = QtWidgets.QLabel(self.addSmthBox)
        self.rightsLabel.setGeometry(QtCore.QRect(60, 100, 121, 16))
        self.rightsLabel.setObjectName("rightsLabel")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.addSmthBox)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(230, 90, 170, 126))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.firstRightsCheckBox = QtWidgets.QCheckBox(self.verticalLayoutWidget_3)
        self.firstRightsCheckBox.setObjectName("firstRightsCheckBox")
        self.verticalLayout.addWidget(self.firstRightsCheckBox)
        self.secondRightsCheckBox = QtWidgets.QCheckBox(self.verticalLayoutWidget_3)
        self.secondRightsCheckBox.setObjectName("secondRightsCheckBox")
        self.verticalLayout.addWidget(self.secondRightsCheckBox)
        self.thirdRightsCheckBox_3 = QtWidgets.QCheckBox(self.verticalLayoutWidget_3)
        self.thirdRightsCheckBox_3.setObjectName("thirdRightsCheckBox_3")
        self.verticalLayout.addWidget(self.thirdRightsCheckBox_3)
        self.fourthRightsCheckBox = QtWidgets.QCheckBox(self.verticalLayoutWidget_3)
        self.fourthRightsCheckBox.setObjectName("fourthRightsCheckBox")
        self.verticalLayout.addWidget(self.fourthRightsCheckBox)
        self.addUserOrInvButton = QtWidgets.QPushButton(self.addSmthBox)
        self.addUserOrInvButton.setGeometry(QtCore.QRect(0, 390, 401, 41))
        self.addUserOrInvButton.setObjectName("addUserOrInvButton")
        self.label_3 = QtWidgets.QLabel(self.addSmthBox)
        self.label_3.setGeometry(QtCore.QRect(10, 60, 171, 16))
        self.label_3.setObjectName("label_3")
        self.IdCardLineEdit = QtWidgets.QLineEdit(self.addSmthBox)
        self.IdCardLineEdit.setGeometry(QtCore.QRect(180, 60, 211, 22))
        self.IdCardLineEdit.setObjectName("IdCardLineEdit")
        self.addHuman_groupBox = QtWidgets.QGroupBox(self.addSmthBox)
        self.addHuman_groupBox.setGeometry(QtCore.QRect(-10, 220, 411, 171))
        self.addHuman_groupBox.setTitle("")
        self.addHuman_groupBox.setObjectName("addHuman_groupBox")
        self.radioButton_User = QtWidgets.QRadioButton(self.addHuman_groupBox)
        self.radioButton_User.setGeometry(QtCore.QRect(270, 20, 111, 20))
        self.radioButton_User.setObjectName("radioButton_User")
        self.radioButton_Admin = QtWidgets.QRadioButton(self.addHuman_groupBox)
        self.radioButton_Admin.setGeometry(QtCore.QRect(270, 0, 121, 20))
        self.radioButton_Admin.setObjectName("radioButton_Admin")
        self.adminRightsGroupBox = QtWidgets.QGroupBox(self.addHuman_groupBox)
        self.adminRightsGroupBox.setGeometry(QtCore.QRect(-10, 40, 411, 131))
        self.adminRightsGroupBox.setTitle("")
        self.adminRightsGroupBox.setObjectName("adminRightsGroupBox")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.adminRightsGroupBox)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(110, 0, 317, 130))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.adminRightsCheckBox = QtWidgets.QCheckBox(self.verticalLayoutWidget_4)
        self.adminRightsCheckBox.setObjectName("adminRightsCheckBox")
        self.verticalLayout_2.addWidget(self.adminRightsCheckBox)
        self.admin2RightsCheckBox = QtWidgets.QCheckBox(self.verticalLayoutWidget_4)
        self.admin2RightsCheckBox.setObjectName("admin2RightsCheckBox")
        self.verticalLayout_2.addWidget(self.admin2RightsCheckBox)
        self.admin3RightsCheckBox = QtWidgets.QCheckBox(self.verticalLayoutWidget_4)
        self.admin3RightsCheckBox.setObjectName("admin3RightsCheckBox")
        self.verticalLayout_2.addWidget(self.admin3RightsCheckBox)
        self.admin4RightsCheckBox = QtWidgets.QCheckBox(self.verticalLayoutWidget_4)
        self.admin4RightsCheckBox.setObjectName("admin4RightsCheckBox")
        self.verticalLayout_2.addWidget(self.admin4RightsCheckBox)
        self.admin5RightsCheckBox = QtWidgets.QCheckBox(self.verticalLayoutWidget_4)
        self.admin5RightsCheckBox.setObjectName("admin5RightsCheckBox")
        self.verticalLayout_2.addWidget(self.admin5RightsCheckBox)
        self.rightsLabel_2 = QtWidgets.QLabel(self.adminRightsGroupBox)
        self.rightsLabel_2.setGeometry(QtCore.QRect(20, 0, 81, 16))
        self.rightsLabel_2.setObjectName("rightsLabel_2")
        self.inventoryWidgetsGroupBox = QtWidgets.QGroupBox(self.addSmthBox)
        self.inventoryWidgetsGroupBox.setGeometry(QtCore.QRect(0, 210, 401, 181))
        self.inventoryWidgetsGroupBox.setTitle("")
        self.inventoryWidgetsGroupBox.setObjectName("inventoryWidgetsGroupBox")
        self.label_5 = QtWidgets.QLabel(self.inventoryWidgetsGroupBox)
        self.label_5.setGeometry(QtCore.QRect(10, 40, 201, 16))
        self.label_5.setObjectName("label_5")
        self.descriptionTextEdit = QtWidgets.QTextEdit(self.inventoryWidgetsGroupBox)
        self.descriptionTextEdit.setGeometry(QtCore.QRect(70, 70, 321, 51))
        self.descriptionTextEdit.setObjectName("descriptionTextEdit")
        self.ableNowSpinBox = QtWidgets.QSpinBox(self.inventoryWidgetsGroupBox)
        self.ableNowSpinBox.setGeometry(QtCore.QRect(240, 10, 151, 22))
        self.ableNowSpinBox.setObjectName("ableNowSpinBox")
        self.label_4 = QtWidgets.QLabel(self.inventoryWidgetsGroupBox)
        self.label_4.setGeometry(QtCore.QRect(50, 10, 141, 16))
        self.label_4.setObjectName("label_4")
        self.reservedSpinBox = QtWidgets.QSpinBox(self.inventoryWidgetsGroupBox)
        self.reservedSpinBox.setGeometry(QtCore.QRect(240, 40, 151, 22))
        self.reservedSpinBox.setObjectName("reservedSpinBox")
        self.label_6 = QtWidgets.QLabel(self.inventoryWidgetsGroupBox)
        self.label_6.setGeometry(QtCore.QRect(10, 70, 61, 16))
        self.label_6.setObjectName("label_6")
        self.label_26 = QtWidgets.QLabel(self.inventoryWidgetsGroupBox)
        self.label_26.setGeometry(QtCore.QRect(0, 150, 101, 16))
        self.label_26.setObjectName("label_26")
        self.label_27 = QtWidgets.QLabel(self.inventoryWidgetsGroupBox)
        self.label_27.setGeometry(QtCore.QRect(180, 150, 141, 16))
        self.label_27.setObjectName("label_27")
        self.heightSpinBox = QtWidgets.QSpinBox(self.inventoryWidgetsGroupBox)
        self.heightSpinBox.setGeometry(QtCore.QRect(110, 150, 61, 22))
        self.heightSpinBox.setObjectName("heightSpinBox")
        self.posFromLeftSpinBox = QtWidgets.QSpinBox(self.inventoryWidgetsGroupBox)
        self.posFromLeftSpinBox.setGeometry(QtCore.QRect(320, 150, 71, 22))
        self.posFromLeftSpinBox.setObjectName("posFromLeftSpinBox")
        self.user_buttons_groupBox = QtWidgets.QGroupBox(self.groupBox)
        self.user_buttons_groupBox.setGeometry(QtCore.QRect(0, 40, 371, 211))
        self.user_buttons_groupBox.setTitle("")
        self.user_buttons_groupBox.setObjectName("user_buttons_groupBox")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.user_buttons_groupBox)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 361, 205))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.usersLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.usersLayout.setContentsMargins(0, 0, 0, 0)
        self.usersLayout.setObjectName("usersLayout")
        self.addUserButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.addUserButton.setObjectName("addUserButton")
        self.usersLayout.addWidget(self.addUserButton)
        self.changeUserInfButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.changeUserInfButton.setObjectName("changeUserInfButton")
        self.usersLayout.addWidget(self.changeUserInfButton)
        self.addInventoryButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.addInventoryButton.setObjectName("addInventoryButton")
        self.usersLayout.addWidget(self.addInventoryButton)
        self.changeInventoryButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.changeInventoryButton.setObjectName("changeInventoryButton")
        self.usersLayout.addWidget(self.changeInventoryButton)
        self.requestsButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.requestsButton.setObjectName("requestsButton")
        self.usersLayout.addWidget(self.requestsButton)
        self.viewInvOrUserBox = QtWidgets.QGroupBox(self.groupBox)
        self.viewInvOrUserBox.setGeometry(QtCore.QRect(370, 30, 661, 341))
        self.viewInvOrUserBox.setObjectName("viewInvOrUserBox")
        self.listView = QtWidgets.QListView(self.viewInvOrUserBox)
        self.listView.setGeometry(QtCore.QRect(400, 30, 251, 311))
        self.listView.setObjectName("listView")
        self.searchByIdLabel = QtWidgets.QLabel(self.viewInvOrUserBox)
        self.searchByIdLabel.setGeometry(QtCore.QRect(10, 30, 21, 16))
        self.searchByIdLabel.setObjectName("searchByIdLabel")
        self.searchByEmailOrNameLabel = QtWidgets.QLabel(self.viewInvOrUserBox)
        self.searchByEmailOrNameLabel.setGeometry(QtCore.QRect(10, 60, 71, 16))
        self.searchByEmailOrNameLabel.setObjectName("searchByEmailOrNameLabel")
        self.searchByIdSpinBox = QtWidgets.QSpinBox(self.viewInvOrUserBox)
        self.searchByIdSpinBox.setGeometry(QtCore.QRect(30, 30, 161, 22))
        self.searchByIdSpinBox.setObjectName("searchByIdSpinBox")
        self.searchByEmailOrNameLineEdit = QtWidgets.QLineEdit(self.viewInvOrUserBox)
        self.searchByEmailOrNameLineEdit.setGeometry(QtCore.QRect(80, 60, 161, 22))
        self.searchByEmailOrNameLineEdit.setObjectName("searchByEmailOrNameLineEdit")
        self.listLabel = QtWidgets.QLabel(self.viewInvOrUserBox)
        self.listLabel.setGeometry(QtCore.QRect(400, 10, 111, 16))
        self.listLabel.setObjectName("listLabel")
        self.verticalLayoutWidget_13 = QtWidgets.QWidget(self.viewInvOrUserBox)
        self.verticalLayoutWidget_13.setGeometry(QtCore.QRect(120, 90, 171, 103))
        self.verticalLayoutWidget_13.setObjectName("verticalLayoutWidget_13")
        self.searchByRightsVerticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_13)
        self.searchByRightsVerticalLayout.setContentsMargins(0, 0, 0, 0)
        self.searchByRightsVerticalLayout.setObjectName("searchByRightsVerticalLayout")
        self.searchByFirstRightsCheckBox = QtWidgets.QCheckBox(self.verticalLayoutWidget_13)
        self.searchByFirstRightsCheckBox.setObjectName("searchByFirstRightsCheckBox")
        self.searchByRightsVerticalLayout.addWidget(self.searchByFirstRightsCheckBox)
        self.searchBySecondRightsCheckBox = QtWidgets.QCheckBox(self.verticalLayoutWidget_13)
        self.searchBySecondRightsCheckBox.setObjectName("searchBySecondRightsCheckBox")
        self.searchByRightsVerticalLayout.addWidget(self.searchBySecondRightsCheckBox)
        self.searchByThirdRightsCheckBox = QtWidgets.QCheckBox(self.verticalLayoutWidget_13)
        self.searchByThirdRightsCheckBox.setObjectName("searchByThirdRightsCheckBox")
        self.searchByRightsVerticalLayout.addWidget(self.searchByThirdRightsCheckBox)
        self.searchByFourthRightsCheckBox = QtWidgets.QCheckBox(self.verticalLayoutWidget_13)
        self.searchByFourthRightsCheckBox.setObjectName("searchByFourthRightsCheckBox")
        self.searchByRightsVerticalLayout.addWidget(self.searchByFourthRightsCheckBox)
        self.SearchByRightsLabel = QtWidgets.QLabel(self.viewInvOrUserBox)
        self.SearchByRightsLabel.setGeometry(QtCore.QRect(10, 90, 111, 20))
        self.SearchByRightsLabel.setObjectName("SearchByRightsLabel")
        self.searchByPosGroupBox = QtWidgets.QGroupBox(self.viewInvOrUserBox)
        self.searchByPosGroupBox.setGeometry(QtCore.QRect(0, 200, 401, 51))
        self.searchByPosGroupBox.setObjectName("searchByPosGroupBox")
        self.label_36 = QtWidgets.QLabel(self.searchByPosGroupBox)
        self.label_36.setGeometry(QtCore.QRect(0, 30, 101, 16))
        self.label_36.setObjectName("label_36")
        self.label_37 = QtWidgets.QLabel(self.searchByPosGroupBox)
        self.label_37.setGeometry(QtCore.QRect(180, 30, 141, 16))
        self.label_37.setObjectName("label_37")
        self.searchByHeightSpinBox = QtWidgets.QSpinBox(self.searchByPosGroupBox)
        self.searchByHeightSpinBox.setGeometry(QtCore.QRect(110, 30, 61, 22))
        self.searchByHeightSpinBox.setObjectName("searchByHeightSpinBox")
        self.searchByPosFromLeftSpinBox = QtWidgets.QSpinBox(self.searchByPosGroupBox)
        self.searchByPosFromLeftSpinBox.setGeometry(QtCore.QRect(320, 30, 71, 22))
        self.searchByPosFromLeftSpinBox.setObjectName("searchByPosFromLeftSpinBox")
        self.searchByNameOrEmailLineEdit = QtWidgets.QLineEdit(self.viewInvOrUserBox)
        self.searchByNameOrEmailLineEdit.setGeometry(QtCore.QRect(30, 30, 311, 22))
        self.searchByNameOrEmailLineEdit.setObjectName("searchByNameOrEmailLineEdit")
        self.searchPushButton = QtWidgets.QPushButton(self.viewInvOrUserBox)
        self.searchPushButton.setGeometry(QtCore.QRect(20, 260, 351, 28))
        self.searchPushButton.setObjectName("searchPushButton")
        self.RequestsGroupBox = QtWidgets.QGroupBox(self.groupBox)
        self.RequestsGroupBox.setGeometry(QtCore.QRect(370, 40, 801, 241))
        self.RequestsGroupBox.setObjectName("RequestsGroupBox")
        self.textBrowser = QtWidgets.QTextBrowser(self.RequestsGroupBox)
        self.textBrowser.setGeometry(QtCore.QRect(20, 50, 341, 111))
        self.textBrowser.setObjectName("textBrowser")
        self.AcceptReqPushButton = QtWidgets.QPushButton(self.RequestsGroupBox)
        self.AcceptReqPushButton.setGeometry(QtCore.QRect(20, 170, 181, 28))
        self.AcceptReqPushButton.setObjectName("AcceptReqPushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.RequestsGroupBox)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 200, 181, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_2 = QtWidgets.QLabel(self.RequestsGroupBox)
        self.label_2.setGeometry(QtCore.QRect(20, 30, 151, 16))
        self.label_2.setObjectName("label_2")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.RequestsGroupBox)
        self.textBrowser_2.setGeometry(QtCore.QRect(530, 50, 271, 111))
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.label_7 = QtWidgets.QLabel(self.RequestsGroupBox)
        self.label_7.setGeometry(QtCore.QRect(530, 30, 181, 16))
        self.label_7.setObjectName("label_7")
        self.pushButton = QtWidgets.QPushButton(self.RequestsGroupBox)
        self.pushButton.setGeometry(QtCore.QRect(370, 50, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_3 = QtWidgets.QPushButton(self.RequestsGroupBox)
        self.pushButton_3.setGeometry(QtCore.QRect(370, 80, 93, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        self.label_8 = QtWidgets.QLabel(self.RequestsGroupBox)
        self.label_8.setGeometry(QtCore.QRect(370, 110, 111, 16))
        self.label_8.setObjectName("label_8")
        self.setCentralWidget(self.centralwidget)
        _translate = QtCore.QCoreApplication.translate
        # MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        # self.burgerButton.setText(_translate("MainWindow", "Меню"))
        self.addSmthBox.setTitle(_translate("MainWindow", "Добавление инвентаря"))
        self.nameOrEmailLabel.setText(_translate("MainWindow", "Название"))
        self.rightsLabel.setText(_translate("MainWindow", "Кто может получить "))
        self.firstRightsCheckBox.setText(_translate("MainWindow", "Обычный пользователь"))
        self.secondRightsCheckBox.setText(_translate("MainWindow", "Редактор-модератор"))
        self.thirdRightsCheckBox_3.setText(_translate("MainWindow", "Инженер"))
        self.fourthRightsCheckBox.setText(_translate("MainWindow", "Главный инженер"))
        self.addUserOrInvButton.setText(_translate("MainWindow", "Добавить"))
        self.label_3.setText(_translate("MainWindow", "Идентификационный номер"))
        self.radioButton_User.setText(_translate("MainWindow", "Пользователь"))
        self.radioButton_Admin.setText(_translate("MainWindow", "Администратор"))
        self.adminRightsCheckBox.setText(_translate("MainWindow", "Добавление пользователей"))
        self.admin2RightsCheckBox.setText(_translate("MainWindow", "Удаление или редактирование пользователей"))
        self.admin3RightsCheckBox.setText(_translate("MainWindow", "Добавление инвентаря"))
        self.admin4RightsCheckBox.setText(_translate("MainWindow", "Удаление или редактирование инвентаря"))
        self.admin5RightsCheckBox.setText(_translate("MainWindow", "Вынесение решений по запросам"))
        self.rightsLabel_2.setText(_translate("MainWindow", "Имеет права:"))
        self.label_5.setText(_translate("MainWindow", "Зарезервированное  количество"))
        self.label_4.setText(_translate("MainWindow", "Доступное количество"))
        self.label_6.setText(_translate("MainWindow", "Описание"))
        self.label_26.setText(_translate("MainWindow", "Высота(от пола)"))
        self.label_27.setText(_translate("MainWindow", "Номер от левого края"))
        self.addUserButton.setText(_translate("MainWindow", "Добавить пользователя"))
        self.changeUserInfButton.setText(
            _translate("MainWindow", "Просмотр и редактирование информации о пользователях"))
        self.addInventoryButton.setText(_translate("MainWindow", "Добавить инвентарь"))
        self.changeInventoryButton.setText(_translate("MainWindow", "Изменить информацио об инвентаре и расположении"))
        self.requestsButton.setText(_translate("MainWindow", "Ответить на запросы"))
        self.viewInvOrUserBox.setTitle(_translate("MainWindow", "Просмотр инвентаря"))
        self.searchByIdLabel.setText(_translate("MainWindow", "ID"))
        self.searchByEmailOrNameLabel.setText(_translate("MainWindow", "Email"))
        self.listLabel.setText(_translate("MainWindow", "Все элементы"))
        self.searchByFirstRightsCheckBox.setText(_translate("MainWindow", "Обычный пользователь"))
        self.searchBySecondRightsCheckBox.setText(_translate("MainWindow", "Редактор-модератор"))
        self.searchByThirdRightsCheckBox.setText(_translate("MainWindow", "Инженер"))
        self.searchByFourthRightsCheckBox.setText(_translate("MainWindow", "Главный инженер"))
        self.SearchByRightsLabel.setText(_translate("MainWindow", "Права на выдачу"))
        self.searchByPosGroupBox.setTitle(_translate("MainWindow", "Поиск по расположению в шкафу"))
        self.label_36.setText(_translate("MainWindow", "Высота(от пола)"))
        self.label_37.setText(_translate("MainWindow", "Номер от левого края"))
        self.searchPushButton.setText(_translate("MainWindow", " Поиск"))
        self.RequestsGroupBox.setTitle(_translate("MainWindow", "Принятие решений по запросам"))
        self.AcceptReqPushButton.setText(_translate("MainWindow", "Одобрить запрос"))
        self.pushButton_2.setText(_translate("MainWindow", "Отклонить запрос"))
        self.label_2.setText(_translate("MainWindow", "Информация по запросу"))
        self.label_7.setText(_translate("MainWindow", "Информация из базы данных"))
        self.pushButton.setText(_translate("MainWindow", "Предыдущий"))
        self.pushButton_3.setText(_translate("MainWindow", "Следующий"))
        self.label_8.setText(_translate("MainWindow", "Необработанных:"))
        self.heightSpinBox.setMinimum(1)
        self.posFromLeftSpinBox.setMinimum(1)
        self.ableNowSpinBox.setMinimum(0)
        self.searchByPosFromLeftSpinBox.setMinimum(1)
        self.searchByHeightSpinBox.setMinimum(1)
        self.addInventoryButton.clicked.connect(self.openEqAdder)
        self.changeUserInfButton.clicked.connect(self.openPeopleViewer)
        self.changeInventoryButton.clicked.connect(self.openEqViewer)
        self.addUserButton.clicked.connect(self.openPeopleAdder)
        self.requestsButton.clicked.connect(self.showReqBox)
        self.radioButton_Admin.clicked.connect(self.adminRightsGroupBox.show)
        self.radioButton_User.clicked.connect(self.adminRightsGroupBox.hide)
        #self.addUserOrInvButton.clicked.connect(self.addEqOrUser)
        self.heightSpinBox.setMinimum(-1)
        self.posFromLeftSpinBox.setMinimum(-1)
        #self.hideEverything()
        self.show()

    def showMessage(self, title: str, info: str):
        msgBox = QMessageBox()
        msgBox.setText(info)
        msgBox.setWindowTitle(title)
        msgBox.exec()

    def addEqOrUser(self):
        codeError = -1
        if (self.__addingEq):
            if self.nameOrEmailLineEdit.text() == "":
                codeError = 1
            if self.descriptionTextEdit.toPlainText() == "":
                codeError = 3
            tg = 0
            if self.firstRightsCheckBox.isChecked():
                tg += 1
            if self.secondRightsCheckBox.isChecked():
                tg += 10
            if self.thirdRightsCheckBox_3.isChecked():
                tg += 100
            if self.fourthRightsCheckBox.isChecked():
                tg += 1000
            if tg == 0:
                codeError = 2
            if codeError == -1:
                eq = Equipment(self.nameOrEmailLineEdit.text(), self.descriptionTextEdit.toPlainText(),
                               self.ableNowSpinBox.value(), self.reservedSpinBox.value(), tg,
                               self.heightSpinBox.value(), self.posFromLeftSpinBox.value())
                self.heightSpinBox.setValue(-1)
                self.posFromLeftSpinBox.setValue(-1)
                self.firstRightsCheckBox.setChecked(False)
                self.secondRightsCheckBox.setChecked(False)
                self.thirdRightsCheckBox_3.setChecked(False)
                self.fourthRightsCheckBox.setChecked(False)
                self.nameOrEmailLineEdit.setText("")
                self.descriptionTextEdit.setText("")
            else:
                if codeError == 1:
                    self.showMessage("Ошибка добавления", "Введите название")
                elif codeError == 2:
                    self.showMessage("Ошибка добавления", "Не отмечены требования выдачи")
                elif codeError == 3:
                    self.showMessage("Ошибка добавления", "отсутствует описание")

    def addEqOrUser2(self):
        codeError = -1
        ar=0
        tg = 0
        if self.nameOrEmailLineEdit.text() == "":
            codeError = 1
        if self.descriptionTextEdit.toPlainText() == "":
            codeError = 3
        if not self.__addingEq:
            if self.IdCardLineEdit == "":
                codeError = 4
        if not self.radioButton_User.isChecked() and (not self.radioButton_Admin.isChecked()):
            codeError = 5
        if self.radioButton_Admin.isChecked():
            if self.adminRightsCheckBox.isChecked():
                ar += 1
            if self.admin2RightsCheckBox.isChecked():
                ar += 10
            if self.admin3RightsCheckBox.isChecked():
                ar += 100
            if self.admin4RightsCheckBox.isChecked():
                ar += 1000
            if tg == 0:
                codeError = 5
        if self.firstRightsCheckBox.isChecked():
            tg += 1
        if self.secondRightsCheckBox.isChecked():
            tg += 10
        if self.thirdRightsCheckBox_3.isChecked():
            tg += 100
        if self.fourthRightsCheckBox.isChecked():
            tg += 1000
        if tg == 0:
            codeError = 2
        if codeError == -1:
            if(self.__addingEq):
                eq = Equipment(self.nameOrEmailLineEdit.text(), self.descriptionTextEdit.toPlainText(),
                           self.ableNowSpinBox.value(), self.reservedSpinBox.value(), tg, self.heightSpinBox.value(),
                           self.posFromLeftSpinBox.value())
            self.heightSpinBox.setValue(-1)
            self.posFromLeftSpinBox.setValue(-1)
            self.firstRightsCheckBox.setChecked(False)
            self.secondRightsCheckBox.setChecked(False)
            self.thirdRightsCheckBox_3.setChecked(False)
            self.fourthRightsCheckBox.setChecked(False)
            self.nameOrEmailLineEdit.setText("")
            self.descriptionTextEdit.setText("")
            self.IdCardLineEdit.setText("")

        else:
            if codeError == 1:
                if self.__addingEq:
                    self.showMessage("Ошибка добавления", "Введите название")
                else:
                    self.showMessage("Ошибка добавления", "Введите Email")
            elif codeError == 2:
                if self.__addingEq:
                    self.showMessage("Ошибка добавления", "Не отмечены требования выдачи")
                else:
                    self.showMessage("Ошибка добавления", "Не отмечены права на получение")
            elif codeError == 3:
                self.showMessage("Ошибка добавления", "отсутствует описание")
            elif codeError ==4:
                self.showMessage("Ошибка добавления","не введен ID карты сотрудника")
            elif codeError==5:
                self.showMessage("Ошибка добавления", "не добавлены права администратора")


def hideEverything(self):
    self.addHuman_groupBox.hide()
    self.label_3.hide()
    self.nameOrEmailLineEdit.hide()
    self.addSmthBox.hide()
    self.inventoryWidgetsGroupBox.hide()
    self.searchByIdSpinBox.hide()
    self.searchByNameOrEmailLineEdit.hide()
    self.viewInvOrUserBox.hide()
    self.searchByIdSpinBox.hide()
    self.searchByPosGroupBox.hide()
    self.RequestsGroupBox.hide()
    self.IdCardLineEdit.hide()


def showReqBox(self):
    self.hideEverything()
    self.RequestsGroupBox.show()


def showMenuButtons(self):
    if self.user_buttons_groupBox.isVisible():
        self.user_buttons_groupBox.hide()
    else:
        self.user_buttons_groupBox.show()
    return 0


def openEqAdder(self):
    self.__addingEq = True
    self.hideEverything()
    self.label_3.show()
    self.label_3.setText("ID")
    self.addSmthBox.setTitle("Добавление инвентаря")
    self.nameOrEmailLabel.setText("Название")
    self.nameOrEmailLineEdit.show()
    self.nameOrEmailLineEdit.setText("")
    self.inventoryWidgetsGroupBox.show()
    self.IdCardLineEdit.show()
    self.rightsLabel.setText("Кто может получить")
    self.firstRightsCheckBox.setChecked(False)
    self.secondRightsCheckBox.setChecked(False)
    self.thirdRightsCheckBox_3.setChecked(False)
    self.fourthRightsCheckBox.setChecked(False)
    self.firstRightsCheckBox.setText("Любой пользователь")
    self.secondRightsCheckBox.setText("Редактор-модератор")
    self.thirdRightsCheckBox_3.setText("Инженер")
    self.fourthRightsCheckBox.setText("Главный инженер")
    self.label_4.setText("Доступное количество")
    self.ableNowSpinBox.setMinimum(0)
    self.label_5.setText("Зарезервированное количество")
    self.reservedSpinBox.setMinimum(0)
    self.label_6.setText("Описание")
    self.heightSpinBox.setValue(-1)
    self.posFromLeftSpinBox.setValue(-1)
    self.firstRightsCheckBox.setChecked(False)
    self.secondRightsCheckBox.setChecked(False)
    self.thirdRightsCheckBox_3.setChecked(False)
    self.fourthRightsCheckBox.setChecked(False)
    self.nameOrEmailLineEdit.setText("")
    self.descriptionTextEdit.setText("")
    self.addSmthBox.show()


def openPeopleAdder(self):
    self.__addingEq = False
    self.hideEverything()
    self.adminRightsGroupBox.hide()
    self.addHuman_groupBox.show()
    self.IdCardLineEdit.show()
    self.nameOrEmailLineEdit.show()
    self.addSmthBox.show()
    self.addSmthBox.setTitle("Добавление пользователей и администраторов")
    self.nameOrEmailLabel.setText("Email")
    self.label_3.setText("ID карты пропуска")
    self.label_3.show()
    self.rightsLabel.setText("Что может получать")
    self.firstRightsCheckBox.setChecked(False)
    self.secondRightsCheckBox.setChecked(False)
    self.thirdRightsCheckBox_3.setChecked(False)
    self.fourthRightsCheckBox.setChecked(False)
    self.firstRightsCheckBox.setText("Простейшее оборудование")
    self.secondRightsCheckBox.setText("Только в рамках проекта")
    self.thirdRightsCheckBox_3.setText("Сложное оборуд.")
    self.fourthRightsCheckBox.setText("Любое")


def openPeopleViewer(self):
    self.__viewingEq = False
    self.hideEverything()
    self.viewInvOrUserBox.show()
    self.searchByNameOrEmailLineEdit.show()
    self.viewInvOrUserBox.setTitle("Просмотр и поиск пользователей")
    self.listLabel.setText("Все пользователи")
    self.searchByEmailOrNameLabel.setText("Email")
    self.SearchByRightsLabel.setText("Статус")
    self.searchByFirstRightsCheckBox.setChecked(False)
    self.searchBySecondRightsCheckBox.setChecked(False)
    self.searchByThirdRightsCheckBox.setChecked(False)
    self.searchByFourthRightsCheckBox.setChecked(False)
    self.searchByFirstRightsCheckBox.setText("Любой пользователь")
    self.searchBySecondRightsCheckBox.setText("Редактор-модератор")
    self.searchByThirdRightsCheckBox.setText("Инженер")
    self.searchByFourthRightsCheckBox.setText("Главный инженер")


def openEqViewer(self):
    self.__viewingEq = True
    self.hideEverything()
    self.viewInvOrUserBox.show()
    self.searchByPosGroupBox.show()
    self.viewInvOrUserBox.setTitle("Просмотр и поиск инвентаря")
    self.listLabel.setText("Весь инвентарь")
    self.searchByIdSpinBox.show()
    self.searchByEmailOrNameLabel.setText("Название")
    self.SearchByRightsLabel.setText("Кому выдавать")
    self.searchByFirstRightsCheckBox.setChecked(False)
    self.searchBySecondRightsCheckBox.setChecked(False)
    self.searchByThirdRightsCheckBox.setChecked(False)
    self.searchByFourthRightsCheckBox.setChecked(False)
    self.searchByFirstRightsCheckBox.setText("Всем пользователям")
    self.searchBySecondRightsCheckBox.setText("Искл. в рамках проекта")
    self.searchByThirdRightsCheckBox.setText("только инженерам")
    self.searchByFourthRightsCheckBox.setText("главным инженерам")
    self.searchByPosFromLeftSpinBox.setValue(1)
    self.searchByHeightSpinBox.setValue(1)"""
from PyQt6.QtWidgets import QMainWindow, QLineEdit, QPushButton, QLabel, QFrame, QMessageBox
from PyQt6 import QtCore, QtGui, QtWidgets
from user_collections import *
from equipment import*
from database import*
from accesses import*
from users import *
from accesses import *
class LogWindow(QMainWindow):
    loggedSignal = QtCore.pyqtSignal()

    def __init__(self, user_list: UserCollection, db: DataBase):
        super(LogWindow, self).__init__()
        self.__db=DataBase
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
            self.__main_window = MainWindow(self.__user_list, user, self.__db)
        else:
            self.__label.setText("Введены неверные данные!")
            self.__password_field.setText("")


class MainWindow(QMainWindow):
    def __init__(self, user_list: UserCollection, current_user, db: DataBase):
        super(MainWindow, self).__init__()
        self.__db=DataBase
        self.setWindowTitle("App")
        self.setFixedSize(1280, 720)
        self.setStyleSheet("background-color:#F0F8FF;")
        self.__current_user = current_user
        self.__user_list = user_list
        self.__addingEq=False #либо добавляет оборудование, либо пользователя
        self.__viewingEq=False #аналогично с просмотром
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
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, 1181, 921))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.addSmthBox = QtWidgets.QGroupBox(self.groupBox)
        self.addSmthBox.setGeometry(QtCore.QRect(370, 40, 401, 431))
        self.addSmthBox.setObjectName("addSmthBox")
        self.label = QtWidgets.QLabel(self.addSmthBox)
        self.label.setGeometry(QtCore.QRect(10, 30, 61, 21))
        self.label.setText("")
        self.label.setObjectName("label")
        self.nameOrEmailLabel = QtWidgets.QLabel(self.addSmthBox)
        self.nameOrEmailLabel.setGeometry(QtCore.QRect(10, 30, 61, 16))
        self.nameOrEmailLabel.setObjectName("nameOrEmailLabel")
        self.nameOrEmailLineEdit = QtWidgets.QLineEdit(self.addSmthBox)
        self.nameOrEmailLineEdit.setGeometry(QtCore.QRect(80, 30, 311, 22))
        self.nameOrEmailLineEdit.setObjectName("nameOrEmailLineEdit")
        self.rightsLabel = QtWidgets.QLabel(self.addSmthBox)
        self.rightsLabel.setGeometry(QtCore.QRect(60, 100, 121, 16))
        self.rightsLabel.setObjectName("rightsLabel")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.addSmthBox)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(230, 90, 170, 126))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.firstRightsCheckBox = QtWidgets.QCheckBox(self.verticalLayoutWidget_3)
        self.firstRightsCheckBox.setObjectName("firstRightsCheckBox")
        self.verticalLayout.addWidget(self.firstRightsCheckBox)
        self.secondRightsCheckBox = QtWidgets.QCheckBox(self.verticalLayoutWidget_3)
        self.secondRightsCheckBox.setObjectName("secondRightsCheckBox")
        self.verticalLayout.addWidget(self.secondRightsCheckBox)
        self.thirdRightsCheckBox_3 = QtWidgets.QCheckBox(self.verticalLayoutWidget_3)
        self.thirdRightsCheckBox_3.setObjectName("thirdRightsCheckBox_3")
        self.verticalLayout.addWidget(self.thirdRightsCheckBox_3)
        self.fourthRightsCheckBox = QtWidgets.QCheckBox(self.verticalLayoutWidget_3)
        self.fourthRightsCheckBox.setObjectName("fourthRightsCheckBox")
        self.verticalLayout.addWidget(self.fourthRightsCheckBox)
        self.addUserOrInvButton = QtWidgets.QPushButton(self.addSmthBox)
        self.addUserOrInvButton.setGeometry(QtCore.QRect(0, 390, 401, 41))
        self.addUserOrInvButton.setObjectName("addUserOrInvButton")
        self.label_3 = QtWidgets.QLabel(self.addSmthBox)
        self.label_3.setGeometry(QtCore.QRect(10, 60, 171, 16))
        self.label_3.setObjectName("label_3")
        self.IdCardLineEdit = QtWidgets.QLineEdit(self.addSmthBox)
        self.IdCardLineEdit.setGeometry(QtCore.QRect(180, 60, 211, 22))
        self.IdCardLineEdit.setObjectName("IdCardLineEdit")
        self.addHuman_groupBox = QtWidgets.QGroupBox(self.addSmthBox)
        self.addHuman_groupBox.setGeometry(QtCore.QRect(-10, 220, 411, 171))
        self.addHuman_groupBox.setTitle("")
        self.addHuman_groupBox.setObjectName("addHuman_groupBox")
        self.radioButton_User = QtWidgets.QRadioButton(self.addHuman_groupBox)
        self.radioButton_User.setGeometry(QtCore.QRect(270, 20, 111, 20))
        self.radioButton_User.setObjectName("radioButton_User")
        self.radioButton_Admin = QtWidgets.QRadioButton(self.addHuman_groupBox)
        self.radioButton_Admin.setGeometry(QtCore.QRect(270, 0, 121, 20))
        self.radioButton_Admin.setObjectName("radioButton_Admin")
        self.adminRightsGroupBox = QtWidgets.QGroupBox(self.addHuman_groupBox)
        self.adminRightsGroupBox.setGeometry(QtCore.QRect(-10, 40, 411, 131))
        self.adminRightsGroupBox.setTitle("")
        self.adminRightsGroupBox.setObjectName("adminRightsGroupBox")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.adminRightsGroupBox)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(110, 0, 317, 130))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.adminRightsCheckBox = QtWidgets.QCheckBox(self.verticalLayoutWidget_4)
        self.adminRightsCheckBox.setObjectName("adminRightsCheckBox")
        self.verticalLayout_2.addWidget(self.adminRightsCheckBox)
        self.admin2RightsCheckBox = QtWidgets.QCheckBox(self.verticalLayoutWidget_4)
        self.admin2RightsCheckBox.setObjectName("admin2RightsCheckBox")
        self.verticalLayout_2.addWidget(self.admin2RightsCheckBox)
        self.admin3RightsCheckBox = QtWidgets.QCheckBox(self.verticalLayoutWidget_4)
        self.admin3RightsCheckBox.setObjectName("admin3RightsCheckBox")
        self.verticalLayout_2.addWidget(self.admin3RightsCheckBox)
        self.admin4RightsCheckBox = QtWidgets.QCheckBox(self.verticalLayoutWidget_4)
        self.admin4RightsCheckBox.setObjectName("admin4RightsCheckBox")
        self.verticalLayout_2.addWidget(self.admin4RightsCheckBox)
        self.admin5RightsCheckBox = QtWidgets.QCheckBox(self.verticalLayoutWidget_4)
        self.admin5RightsCheckBox.setObjectName("admin5RightsCheckBox")
        self.verticalLayout_2.addWidget(self.admin5RightsCheckBox)
        self.rightsLabel_2 = QtWidgets.QLabel(self.adminRightsGroupBox)
        self.rightsLabel_2.setGeometry(QtCore.QRect(20, 0, 81, 16))
        self.rightsLabel_2.setObjectName("rightsLabel_2")
        self.inventoryWidgetsGroupBox = QtWidgets.QGroupBox(self.addSmthBox)
        self.inventoryWidgetsGroupBox.setGeometry(QtCore.QRect(0, 210, 401, 181))
        self.inventoryWidgetsGroupBox.setTitle("")
        self.inventoryWidgetsGroupBox.setObjectName("inventoryWidgetsGroupBox")
        self.label_5 = QtWidgets.QLabel(self.inventoryWidgetsGroupBox)
        self.label_5.setGeometry(QtCore.QRect(10, 40, 201, 16))
        self.label_5.setObjectName("label_5")
        self.descriptionTextEdit = QtWidgets.QTextEdit(self.inventoryWidgetsGroupBox)
        self.descriptionTextEdit.setGeometry(QtCore.QRect(70, 70, 321, 51))
        self.descriptionTextEdit.setObjectName("descriptionTextEdit")
        self.ableNowSpinBox = QtWidgets.QSpinBox(self.inventoryWidgetsGroupBox)
        self.ableNowSpinBox.setGeometry(QtCore.QRect(240, 10, 151, 22))
        self.ableNowSpinBox.setObjectName("ableNowSpinBox")
        self.label_4 = QtWidgets.QLabel(self.inventoryWidgetsGroupBox)
        self.label_4.setGeometry(QtCore.QRect(50, 10, 141, 16))
        self.label_4.setObjectName("label_4")
        self.reservedSpinBox = QtWidgets.QSpinBox(self.inventoryWidgetsGroupBox)
        self.reservedSpinBox.setGeometry(QtCore.QRect(240, 40, 151, 22))
        self.reservedSpinBox.setObjectName("reservedSpinBox")
        self.label_6 = QtWidgets.QLabel(self.inventoryWidgetsGroupBox)
        self.label_6.setGeometry(QtCore.QRect(10, 70, 61, 16))
        self.label_6.setObjectName("label_6")
        self.label_26 = QtWidgets.QLabel(self.inventoryWidgetsGroupBox)
        self.label_26.setGeometry(QtCore.QRect(0, 150, 101, 16))
        self.label_26.setObjectName("label_26")
        self.label_27 = QtWidgets.QLabel(self.inventoryWidgetsGroupBox)
        self.label_27.setGeometry(QtCore.QRect(180, 150, 141, 16))
        self.label_27.setObjectName("label_27")
        self.heightSpinBox = QtWidgets.QSpinBox(self.inventoryWidgetsGroupBox)
        self.heightSpinBox.setGeometry(QtCore.QRect(110, 150, 61, 22))
        self.heightSpinBox.setObjectName("heightSpinBox")
        self.posFromLeftSpinBox = QtWidgets.QSpinBox(self.inventoryWidgetsGroupBox)
        self.posFromLeftSpinBox.setGeometry(QtCore.QRect(320, 150, 71, 22))
        self.posFromLeftSpinBox.setObjectName("posFromLeftSpinBox")
        self.user_buttons_groupBox = QtWidgets.QGroupBox(self.groupBox)
        self.user_buttons_groupBox.setGeometry(QtCore.QRect(0, 40, 371, 211))
        self.user_buttons_groupBox.setTitle("")
        self.user_buttons_groupBox.setObjectName("user_buttons_groupBox")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.user_buttons_groupBox)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 361, 205))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.usersLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.usersLayout.setContentsMargins(0, 0, 0, 0)
        self.usersLayout.setObjectName("usersLayout")
        self.addUserButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.addUserButton.setObjectName("addUserButton")
        self.usersLayout.addWidget(self.addUserButton)
        self.changeUserInfButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.changeUserInfButton.setObjectName("changeUserInfButton")
        self.usersLayout.addWidget(self.changeUserInfButton)
        self.addInventoryButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.addInventoryButton.setObjectName("addInventoryButton")
        self.usersLayout.addWidget(self.addInventoryButton)
        self.changeInventoryButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.changeInventoryButton.setObjectName("changeInventoryButton")
        self.usersLayout.addWidget(self.changeInventoryButton)
        self.requestsButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.requestsButton.setObjectName("requestsButton")
        self.usersLayout.addWidget(self.requestsButton)
        self.viewInvOrUserBox = QtWidgets.QGroupBox(self.groupBox)
        self.viewInvOrUserBox.setGeometry(QtCore.QRect(370, 30, 661, 341))
        self.viewInvOrUserBox.setObjectName("viewInvOrUserBox")
        self.listView = QtWidgets.QListView(self.viewInvOrUserBox)
        self.listView.setGeometry(QtCore.QRect(400, 30, 251, 311))
        self.listView.setObjectName("listView")
        self.searchByIdLabel = QtWidgets.QLabel(self.viewInvOrUserBox)
        self.searchByIdLabel.setGeometry(QtCore.QRect(10, 30, 21, 16))
        self.searchByIdLabel.setObjectName("searchByIdLabel")
        self.searchByEmailOrNameLabel = QtWidgets.QLabel(self.viewInvOrUserBox)
        self.searchByEmailOrNameLabel.setGeometry(QtCore.QRect(10, 60, 71, 16))
        self.searchByEmailOrNameLabel.setObjectName("searchByEmailOrNameLabel")
        self.searchByIdSpinBox = QtWidgets.QSpinBox(self.viewInvOrUserBox)
        self.searchByIdSpinBox.setGeometry(QtCore.QRect(30, 30, 161, 22))
        self.searchByIdSpinBox.setObjectName("searchByIdSpinBox")
        self.searchByEmailOrNameLineEdit = QtWidgets.QLineEdit(self.viewInvOrUserBox)
        self.searchByEmailOrNameLineEdit.setGeometry(QtCore.QRect(80, 60, 161, 22))
        self.searchByEmailOrNameLineEdit.setObjectName("searchByEmailOrNameLineEdit")
        self.listLabel = QtWidgets.QLabel(self.viewInvOrUserBox)
        self.listLabel.setGeometry(QtCore.QRect(400, 10, 111, 16))
        self.listLabel.setObjectName("listLabel")
        self.verticalLayoutWidget_13 = QtWidgets.QWidget(self.viewInvOrUserBox)
        self.verticalLayoutWidget_13.setGeometry(QtCore.QRect(120, 90, 171, 103))
        self.verticalLayoutWidget_13.setObjectName("verticalLayoutWidget_13")
        self.searchByRightsVerticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_13)
        self.searchByRightsVerticalLayout.setContentsMargins(0, 0, 0, 0)
        self.searchByRightsVerticalLayout.setObjectName("searchByRightsVerticalLayout")
        self.searchByFirstRightsCheckBox = QtWidgets.QCheckBox(self.verticalLayoutWidget_13)
        self.searchByFirstRightsCheckBox.setObjectName("searchByFirstRightsCheckBox")
        self.searchByRightsVerticalLayout.addWidget(self.searchByFirstRightsCheckBox)
        self.searchBySecondRightsCheckBox = QtWidgets.QCheckBox(self.verticalLayoutWidget_13)
        self.searchBySecondRightsCheckBox.setObjectName("searchBySecondRightsCheckBox")
        self.searchByRightsVerticalLayout.addWidget(self.searchBySecondRightsCheckBox)
        self.searchByThirdRightsCheckBox = QtWidgets.QCheckBox(self.verticalLayoutWidget_13)
        self.searchByThirdRightsCheckBox.setObjectName("searchByThirdRightsCheckBox")
        self.searchByRightsVerticalLayout.addWidget(self.searchByThirdRightsCheckBox)
        self.searchByFourthRightsCheckBox = QtWidgets.QCheckBox(self.verticalLayoutWidget_13)
        self.searchByFourthRightsCheckBox.setObjectName("searchByFourthRightsCheckBox")
        self.searchByRightsVerticalLayout.addWidget(self.searchByFourthRightsCheckBox)
        self.SearchByRightsLabel = QtWidgets.QLabel(self.viewInvOrUserBox)
        self.SearchByRightsLabel.setGeometry(QtCore.QRect(10, 90, 111, 20))
        self.SearchByRightsLabel.setObjectName("SearchByRightsLabel")
        self.searchByPosGroupBox = QtWidgets.QGroupBox(self.viewInvOrUserBox)
        self.searchByPosGroupBox.setGeometry(QtCore.QRect(0, 200, 401, 51))
        self.searchByPosGroupBox.setObjectName("searchByPosGroupBox")
        self.label_36 = QtWidgets.QLabel(self.searchByPosGroupBox)
        self.label_36.setGeometry(QtCore.QRect(0, 30, 101, 16))
        self.label_36.setObjectName("label_36")
        self.label_37 = QtWidgets.QLabel(self.searchByPosGroupBox)
        self.label_37.setGeometry(QtCore.QRect(180, 30, 141, 16))
        self.label_37.setObjectName("label_37")
        self.searchByHeightSpinBox = QtWidgets.QSpinBox(self.searchByPosGroupBox)
        self.searchByHeightSpinBox.setGeometry(QtCore.QRect(110, 30, 61, 22))
        self.searchByHeightSpinBox.setObjectName("searchByHeightSpinBox")
        self.searchByPosFromLeftSpinBox = QtWidgets.QSpinBox(self.searchByPosGroupBox)
        self.searchByPosFromLeftSpinBox.setGeometry(QtCore.QRect(320, 30, 71, 22))
        self.searchByPosFromLeftSpinBox.setObjectName("searchByPosFromLeftSpinBox")
        self.searchByNameOrEmailLineEdit = QtWidgets.QLineEdit(self.viewInvOrUserBox)
        self.searchByNameOrEmailLineEdit.setGeometry(QtCore.QRect(30, 30, 311, 22))
        self.searchByNameOrEmailLineEdit.setObjectName("searchByNameOrEmailLineEdit")
        self.searchPushButton = QtWidgets.QPushButton(self.viewInvOrUserBox)
        self.searchPushButton.setGeometry(QtCore.QRect(20, 260, 351, 28))
        self.searchPushButton.setObjectName("searchPushButton")
        self.RequestsGroupBox = QtWidgets.QGroupBox(self.groupBox)
        self.RequestsGroupBox.setGeometry(QtCore.QRect(370, 40, 801, 241))
        self.RequestsGroupBox.setObjectName("RequestsGroupBox")
        self.textBrowser = QtWidgets.QTextBrowser(self.RequestsGroupBox)
        self.textBrowser.setGeometry(QtCore.QRect(20, 50, 341, 111))
        self.textBrowser.setObjectName("textBrowser")
        self.AcceptReqPushButton = QtWidgets.QPushButton(self.RequestsGroupBox)
        self.AcceptReqPushButton.setGeometry(QtCore.QRect(20, 170, 181, 28))
        self.AcceptReqPushButton.setObjectName("AcceptReqPushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.RequestsGroupBox)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 200, 181, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_2 = QtWidgets.QLabel(self.RequestsGroupBox)
        self.label_2.setGeometry(QtCore.QRect(20, 30, 151, 16))
        self.label_2.setObjectName("label_2")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.RequestsGroupBox)
        self.textBrowser_2.setGeometry(QtCore.QRect(530, 50, 271, 111))
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.label_7 = QtWidgets.QLabel(self.RequestsGroupBox)
        self.label_7.setGeometry(QtCore.QRect(530, 30, 181, 16))
        self.label_7.setObjectName("label_7")
        self.pushButton = QtWidgets.QPushButton(self.RequestsGroupBox)
        self.pushButton.setGeometry(QtCore.QRect(370, 50, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_3 = QtWidgets.QPushButton(self.RequestsGroupBox)
        self.pushButton_3.setGeometry(QtCore.QRect(370, 80, 93, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        self.label_8 = QtWidgets.QLabel(self.RequestsGroupBox)
        self.label_8.setGeometry(QtCore.QRect(370, 110, 111, 16))
        self.label_8.setObjectName("label_8")
        self.setCentralWidget(self.centralwidget)
        _translate = QtCore.QCoreApplication.translate
        #MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        #self.burgerButton.setText(_translate("MainWindow", "Меню"))
        self.addSmthBox.setTitle(_translate("MainWindow", "Добавление инвентаря"))
        self.nameOrEmailLabel.setText(_translate("MainWindow", "Название"))
        self.rightsLabel.setText(_translate("MainWindow", "Кто может получить "))
        self.firstRightsCheckBox.setText(_translate("MainWindow", "Обычный пользователь"))
        self.secondRightsCheckBox.setText(_translate("MainWindow", "Редактор-модератор"))
        self.thirdRightsCheckBox_3.setText(_translate("MainWindow", "Инженер"))
        self.fourthRightsCheckBox.setText(_translate("MainWindow", "Главный инженер"))
        self.addUserOrInvButton.setText(_translate("MainWindow", "Добавить"))
        self.label_3.setText(_translate("MainWindow", "Идентификационный номер"))
        self.radioButton_User.setText(_translate("MainWindow", "Пользователь"))
        self.radioButton_Admin.setText(_translate("MainWindow", "Администратор"))
        self.adminRightsCheckBox.setText(_translate("MainWindow", "Добавление пользователей"))
        self.admin2RightsCheckBox.setText(_translate("MainWindow", "Удаление или редактирование пользователей"))
        self.admin3RightsCheckBox.setText(_translate("MainWindow", "Добавление инвентаря"))
        self.admin4RightsCheckBox.setText(_translate("MainWindow", "Удаление или редактирование инвентаря"))
        self.admin5RightsCheckBox.setText(_translate("MainWindow", "Вынесение решений по запросам"))
        self.rightsLabel_2.setText(_translate("MainWindow", "Имеет права:"))
        self.label_5.setText(_translate("MainWindow", "Зарезервированное  количество"))
        self.label_4.setText(_translate("MainWindow", "Доступное количество"))
        self.label_6.setText(_translate("MainWindow", "Описание"))
        self.label_26.setText(_translate("MainWindow", "Высота(от пола)"))
        self.label_27.setText(_translate("MainWindow", "Номер от левого края"))
        self.addUserButton.setText(_translate("MainWindow", "Добавить пользователя"))
        self.changeUserInfButton.setText(
            _translate("MainWindow", "Просмотр и редактирование информации о пользователях"))
        self.addInventoryButton.setText(_translate("MainWindow", "Добавить инвентарь"))
        self.changeInventoryButton.setText(_translate("MainWindow", "Изменить информацио об инвентаре и расположении"))
        self.requestsButton.setText(_translate("MainWindow", "Ответить на запросы"))
        self.viewInvOrUserBox.setTitle(_translate("MainWindow", "Просмотр инвентаря"))
        self.searchByIdLabel.setText(_translate("MainWindow", "ID"))
        self.searchByEmailOrNameLabel.setText(_translate("MainWindow", "Email"))
        self.listLabel.setText(_translate("MainWindow", "Все элементы"))
        self.searchByFirstRightsCheckBox.setText(_translate("MainWindow", "Обычный пользователь"))
        self.searchBySecondRightsCheckBox.setText(_translate("MainWindow", "Редактор-модератор"))
        self.searchByThirdRightsCheckBox.setText(_translate("MainWindow", "Инженер"))
        self.searchByFourthRightsCheckBox.setText(_translate("MainWindow", "Главный инженер"))
        self.SearchByRightsLabel.setText(_translate("MainWindow", "Права на выдачу"))
        self.searchByPosGroupBox.setTitle(_translate("MainWindow", "Поиск по расположению в шкафу"))
        self.label_36.setText(_translate("MainWindow", "Высота(от пола)"))
        self.label_37.setText(_translate("MainWindow", "Номер от левого края"))
        self.searchPushButton.setText(_translate("MainWindow", " Поиск"))
        self.RequestsGroupBox.setTitle(_translate("MainWindow", "Принятие решений по запросам"))
        self.AcceptReqPushButton.setText(_translate("MainWindow", "Одобрить запрос"))
        self.pushButton_2.setText(_translate("MainWindow", "Отклонить запрос"))
        self.label_2.setText(_translate("MainWindow", "Информация по запросу"))
        self.label_7.setText(_translate("MainWindow", "Информация из базы данных"))
        self.pushButton.setText(_translate("MainWindow", "Предыдущий"))
        self.pushButton_3.setText(_translate("MainWindow", "Следующий"))
        self.label_8.setText(_translate("MainWindow", "Необработанных:"))
        self.heightSpinBox.setMinimum(1)
        self.posFromLeftSpinBox.setMinimum(1)
        self.ableNowSpinBox.setMinimum(0)
        self.searchByPosFromLeftSpinBox.setMinimum(1)
        self.searchByHeightSpinBox.setMinimum(1)
        self.addInventoryButton.clicked.connect(self.openEqAdder)
        self.changeUserInfButton.clicked.connect(self.openPeopleViewer)
        self.changeInventoryButton.clicked.connect(self.openEqViewer)
        self.addUserButton.clicked.connect(self.openPeopleAdder)
        self.requestsButton.clicked.connect(self.showReqBox)
        self.radioButton_Admin.clicked.connect(self.adminRightsGroupBox.show)
        self.radioButton_User.clicked.connect(self.adminRightsGroupBox.hide)
        self.addUserOrInvButton.clicked.connect(self.addEqOrUser2)
        self.heightSpinBox.setMinimum(-1)
        self.posFromLeftSpinBox.setMinimum(-1)
        self.hideEverything()
        self.show()
    def addEqOrUser(self):
        codeError = -1
        ar=0
        tg = 0
        if self.nameOrEmailLineEdit.text() == "":
            codeError = 1
        if self.descriptionTextEdit.toPlainText() == "":
            codeError = 3
        if not self.__addingEq:
            if self.IdCardLineEdit == "":
                codeError = 4
        if not self.radioButton_User.isChecked() and (not self.radioButton_Admin.isChecked()):
            codeError = 5
        if self.radioButton_Admin.isChecked():
            if self.adminRightsCheckBox.isChecked():
                ar += 1
            if self.admin2RightsCheckBox.isChecked():
                ar += 10
            if self.admin3RightsCheckBox.isChecked():
                ar += 100
            if self.admin4RightsCheckBox.isChecked():
                ar += 1000
            if tg == 0:
                codeError = 5
        if self.firstRightsCheckBox.isChecked():
            tg += 1
        if self.secondRightsCheckBox.isChecked():
            tg += 10
        if self.thirdRightsCheckBox_3.isChecked():
            tg += 100
        if self.fourthRightsCheckBox.isChecked():
            tg += 1000
        if tg == 0:
            codeError = 2
        if codeError == -1:
            if(self.__addingEq):
                eq = Equipment(self.nameOrEmailLineEdit.text(), self.descriptionTextEdit.toPlainText(),
                           self.ableNowSpinBox.value(), self.reservedSpinBox.value(), tg, self.heightSpinBox.value(),
                           self.posFromLeftSpinBox.value())
            self.heightSpinBox.setValue(-1)
            self.posFromLeftSpinBox.setValue(-1)
            self.firstRightsCheckBox.setChecked(False)
            self.secondRightsCheckBox.setChecked(False)
            self.thirdRightsCheckBox_3.setChecked(False)
            self.fourthRightsCheckBox.setChecked(False)
            self.nameOrEmailLineEdit.setText("")
            self.descriptionTextEdit.setText("")
            self.IdCardLineEdit.setText("")

        else:
            if codeError == 1:
                if self.__addingEq:
                    self.showMessage("Ошибка добавления", "Введите название")
                else:
                    self.showMessage("Ошибка добавления", "Введите Email")
            elif codeError == 2:
                if self.__addingEq:
                    self.showMessage("Ошибка добавления", "Не отмечены требования выдачи")
                else:
                    self.showMessage("Ошибка добавления", "Не отмечены права на получение")
            elif codeError == 3:
                self.showMessage("Ошибка добавления", "отсутствует описание")
            elif codeError ==4:
                self.showMessage("Ошибка добавления","не введен ID карты сотрудника")
            elif codeError==5:
                self.showMessage("Ошибка добавления", "не добавлены права администратора")

    def showMessage(self, title:str, info:str):
        msgBox = QMessageBox()
        msgBox.setText(info)
        msgBox.setWindowTitle(title)
        msgBox.exec()
    def hideEverything(self):
        self.addHuman_groupBox.hide()
        self.label_3.hide()
        self.nameOrEmailLineEdit.hide()
        self.addSmthBox.hide()
        self.inventoryWidgetsGroupBox.hide()
        self.searchByIdSpinBox.hide()
        self.searchByNameOrEmailLineEdit.hide()
        self.viewInvOrUserBox.hide()
        self.searchByIdSpinBox.hide()
        self.searchByPosGroupBox.hide()
        self.RequestsGroupBox.hide()
        self.IdCardLineEdit.hide()
    def showReqBox(self):
        self.hideEverything()
        self.RequestsGroupBox.show()
    def showMenuButtons(self):
        if self.user_buttons_groupBox.isVisible():
            self.user_buttons_groupBox.hide()
        else:
            self.user_buttons_groupBox.show()
        return 0
    def openEqAdder(self):
        self.__addingEq=True
        self.hideEverything()
        self.label_3.show()
        self.label_3.setText("ID")
        self.addSmthBox.setTitle("Добавление инвентаря")
        self.nameOrEmailLabel.setText("Название")
        self.nameOrEmailLineEdit.show()
        self.nameOrEmailLineEdit.setText("")
        self.inventoryWidgetsGroupBox.show()
        self.IdCardLineEdit.show()
        self.rightsLabel.setText("Кто может получить")
        self.firstRightsCheckBox.setChecked(False)
        self.secondRightsCheckBox.setChecked(False)
        self.thirdRightsCheckBox_3.setChecked(False)
        self.fourthRightsCheckBox.setChecked(False)
        self.firstRightsCheckBox.setText("Любой пользователь")
        self.secondRightsCheckBox.setText("Редактор-модератор")
        self.thirdRightsCheckBox_3.setText("Инженер")
        self.fourthRightsCheckBox.setText("Главный инженер")
        self.label_4.setText("Доступное количество")
        self.ableNowSpinBox.setMinimum(0)
        self.label_5.setText("Зарезервированное количество")
        self.reservedSpinBox.setMinimum(0)
        self.label_6.setText("Описание")
        self.heightSpinBox.setValue(-1)
        self.posFromLeftSpinBox.setValue(-1)
        self.firstRightsCheckBox.setChecked(False)
        self.secondRightsCheckBox.setChecked(False)
        self.thirdRightsCheckBox_3.setChecked(False)
        self.fourthRightsCheckBox.setChecked(False)
        self.nameOrEmailLineEdit.setText("")
        self.descriptionTextEdit.setText("")
        self.addSmthBox.show()

    def openPeopleAdder(self):
        self.__addingEq=False
        self.hideEverything()
        self.adminRightsGroupBox.hide()
        self.addHuman_groupBox.show()
        self.IdCardLineEdit.show()
        self.nameOrEmailLineEdit.show()
        self.addSmthBox.show()
        self.addSmthBox.setTitle("Добавление пользователей и администраторов")
        self.nameOrEmailLabel.setText("Email")
        self.label_3.setText("ID карты пропуска")
        self.label_3.show()
        self.rightsLabel.setText("Что может получать")
        self.firstRightsCheckBox.setChecked(False)
        self.secondRightsCheckBox.setChecked(False)
        self.thirdRightsCheckBox_3.setChecked(False)
        self.fourthRightsCheckBox.setChecked(False)
        self.firstRightsCheckBox.setText("Простейшее оборудование")
        self.secondRightsCheckBox.setText("Только в рамках проекта")
        self.thirdRightsCheckBox_3.setText("Сложное оборуд.")
        self.fourthRightsCheckBox.setText("Любое")
    def openPeopleViewer(self):
        self.__viewingEq=False
        self.hideEverything()
        self.viewInvOrUserBox.show()
        self.searchByNameOrEmailLineEdit.show()
        self.viewInvOrUserBox.setTitle("Просмотр и поиск пользователей")
        self.listLabel.setText("Все пользователи")
        self.searchByEmailOrNameLabel.setText("Email")
        self.SearchByRightsLabel.setText("Статус")
        self.searchByFirstRightsCheckBox.setChecked(False)
        self.searchBySecondRightsCheckBox.setChecked(False)
        self.searchByThirdRightsCheckBox.setChecked(False)
        self.searchByFourthRightsCheckBox.setChecked(False)
        self.searchByFirstRightsCheckBox.setText("Любой пользователь")
        self.searchBySecondRightsCheckBox.setText("Редактор-модератор")
        self.searchByThirdRightsCheckBox.setText("Инженер")
        self.searchByFourthRightsCheckBox.setText("Главный инженер")
    def openEqViewer(self):
        self.__viewingEq=True
        self.hideEverything()
        self.viewInvOrUserBox.show()
        self.searchByPosGroupBox.show()
        self.viewInvOrUserBox.setTitle("Просмотр и поиск инвентаря")
        self.listLabel.setText("Весь инвентарь")
        self.searchByIdSpinBox.show()
        self.searchByEmailOrNameLabel.setText("Название")
        self.SearchByRightsLabel.setText("Кому выдавать")
        self.searchByFirstRightsCheckBox.setChecked(False)
        self.searchBySecondRightsCheckBox.setChecked(False)
        self.searchByThirdRightsCheckBox.setChecked(False)
        self.searchByFourthRightsCheckBox.setChecked(False)
        self.searchByFirstRightsCheckBox.setText("Всем пользователям")
        self.searchBySecondRightsCheckBox.setText("Искл. в рамках проекта")
        self.searchByThirdRightsCheckBox.setText("только инженерам")
        self.searchByFourthRightsCheckBox.setText("главным инженерам")
        self.searchByPosFromLeftSpinBox.setValue(1)
        self.searchByHeightSpinBox.setValue(1)
    def addEqOrUser2(self):
        codeError = -1
        tg = 0
        if self.nameOrEmailLineEdit.text() == "":
            codeError = 1
        if self.__addingEq and self.descriptionTextEdit.toPlainText() == "":
            codeError = 3
        if not self.__addingEq and self.IdCardLineEdit.text() == "":
            codeError = 4
        if not self.radioButton_User.isChecked() and (not self.radioButton_Admin.isChecked()):
            codeError = 6
        addUs=False
        chUs=False
        addEq=False
        chEq=False
        getReq=False
        if self.radioButton_Admin.isChecked():
            if self.adminRightsCheckBox.isChecked():
                addUs=True
            if self.admin2RightsCheckBox.isChecked():
                chUs=True
            if self.admin3RightsCheckBox.isChecked():
                addEq=True
            if self.admin4RightsCheckBox.isChecked():
                chEq=True
            if self.admin5RightsCheckBox.isChecked():
                getReq= True
            if (not addUs) and (not chEq) and (not chUs)and (addEq) and (getReq):
                codeError=5
        if self.radioButton_User.isChecked():
            addUs = False
            chUs = False
            addEq = False
            chEq = False
            getReq = False
        if self.firstRightsCheckBox.isChecked():
            tg += 1
        if self.secondRightsCheckBox.isChecked():
            tg += 10
        if self.thirdRightsCheckBox_3.isChecked():
            tg += 100
        if self.fourthRightsCheckBox.isChecked():
            tg += 1000
        if tg == 0:
            codeError = 2
        """if not self.__addingEq:
            if self.__db.get_user_by_id(int([self.IdCardLineEdit.text()][16])) or self.__db.get_admin_by_id(int([self.IdCardLineEdit.text()][16])):
                codeError=7
                self.IdCardLineEdit.setText("")
            if self.__db.get_user_by_mail(str(self.nameOrEmailLineEdit.text())) or self.__db.get_admin_by_mail(str(self.nameOrEmailLineEdit.text())):
                codeError=8
                self.nameOrEmailLineEdit.setText("")
        else:
            if self.__db.get_equipment_by_title(str(self.nameOrEmailLineEdit.text())):
                codeError=8"""
        if codeError == -1:
            if(self.__addingEq):
                eq = Equipment(self.nameOrEmailLineEdit.text(), self.descriptionTextEdit.toPlainText(),
                           self.ableNowSpinBox.value(), self.reservedSpinBox.value(), tg, self.heightSpinBox.value(),
                           self.posFromLeftSpinBox.value())
                #self.__db.add_equipment(eq)
            else:
                if self.radioButton_User.isChecked():
                    ac = Access(tg)
                    us = CommonUser(int([self.IdCardLineEdit.text()][16]), str(self.nameOrEmailLineEdit.text()), ac)
                    #self.__db.add_user(us)
                if self.radioButton_Admin.isChecked():
                    ac =AdminAccess(tg,addUs,chUs,addEq,chEq, getReq)
                    adm=Admin(int([self.IdCardLineEdit.text()][16]), str(self.nameOrEmailLineEdit.text()),"", ac)
                    #self.__db.add_admin(adm)
            self.heightSpinBox.setValue(-1)
            self.posFromLeftSpinBox.setValue(-1)
            self.firstRightsCheckBox.setChecked(False)
            self.secondRightsCheckBox.setChecked(False)
            self.thirdRightsCheckBox_3.setChecked(False)
            self.fourthRightsCheckBox.setChecked(False)
            self.nameOrEmailLineEdit.setText("")
            self.descriptionTextEdit.setText("")
            self.IdCardLineEdit.setText("")

        else:
            if codeError == 1:
                if self.__addingEq:
                    self.showMessage("Ошибка добавления", "Введите название")
                else:
                    self.showMessage("Ошибка добавления", "Введите Email")
            elif codeError == 2:
                if self.__addingEq:
                    self.showMessage("Ошибка добавления", "Не отмечены требования выдачи")
                else:
                    self.showMessage("Ошибка добавления", "Не отмечены права на получение")
            elif codeError == 3:
                self.showMessage("Ошибка добавления", "отсутствует описание")
            elif codeError ==4:
                self.showMessage("Ошибка добавления","не введен ID карты сотрудника")
            elif codeError==5:
                self.showMessage("Ошибка добавления", "не выбраны права администратора")
            elif codeError==6:
                self.showMessage("Ошибка добавления", "Не выбран тип пользователя")
            elif codeError==7:
                self.showMessage("Ошибка добавления", "пользователь с такой картой уже добавлен")
            elif codeError==8:
                if self.__addingEq:
                    self.showMessage("Ошибка добавления","Оборудование с таким названием уже есть в базе")
                else:
                    self.showMessage("Ошибка добавления", "Пользователь с таким email уже добавлен")