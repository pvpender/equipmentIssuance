# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frontier.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1459, 896)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, 1121, 821))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.burgerButton = QtWidgets.QPushButton(self.groupBox)
        self.burgerButton.setGeometry(QtCore.QRect(10, 20, 111, 31))
        self.burgerButton.setMouseTracking(True)
        self.burgerButton.setObjectName("burgerButton")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 80, 387, 81))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.InventoryLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.InventoryLayout.setContentsMargins(0, 0, 0, 0)
        self.InventoryLayout.setObjectName("InventoryLayout")
        self.addInventoryButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.addInventoryButton.setObjectName("addInventoryButton")
        self.InventoryLayout.addWidget(self.addInventoryButton)
        self.changeInventoryButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.changeInventoryButton.setObjectName("changeInventoryButton")
        self.InventoryLayout.addWidget(self.changeInventoryButton)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.groupBox)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 170, 361, 161))
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
        self.addAdminButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.addAdminButton.setObjectName("addAdminButton")
        self.usersLayout.addWidget(self.addAdminButton)
        self.changeAdminButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.changeAdminButton.setObjectName("changeAdminButton")
        self.usersLayout.addWidget(self.changeAdminButton)
        self.hideButton = QtWidgets.QPushButton(self.groupBox)
        self.hideButton.setGeometry(QtCore.QRect(10, 50, 31, 28))
        self.hideButton.setObjectName("hideButton")
        self.addSmthBox = QtWidgets.QGroupBox(self.groupBox)
        self.addSmthBox.setGeometry(QtCore.QRect(410, 70, 401, 431))
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
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(230, 90, 161, 126))
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
        self.idSpinBox = QtWidgets.QSpinBox(self.addSmthBox)
        self.idSpinBox.setGeometry(QtCore.QRect(180, 60, 121, 22))
        self.idSpinBox.setObjectName("idSpinBox")
        self.inventoryWidgetsGroupBox = QtWidgets.QGroupBox(self.addSmthBox)
        self.inventoryWidgetsGroupBox.setGeometry(QtCore.QRect(0, 180, 401, 211))
        self.inventoryWidgetsGroupBox.setTitle("")
        self.inventoryWidgetsGroupBox.setObjectName("inventoryWidgetsGroupBox")
        self.label_5 = QtWidgets.QLabel(self.inventoryWidgetsGroupBox)
        self.label_5.setGeometry(QtCore.QRect(10, 70, 201, 16))
        self.label_5.setObjectName("label_5")
        self.descriptionTextEdit = QtWidgets.QTextEdit(self.inventoryWidgetsGroupBox)
        self.descriptionTextEdit.setGeometry(QtCore.QRect(70, 100, 321, 61))
        self.descriptionTextEdit.setObjectName("descriptionTextEdit")
        self.ableNowSpinBox = QtWidgets.QSpinBox(self.inventoryWidgetsGroupBox)
        self.ableNowSpinBox.setGeometry(QtCore.QRect(240, 40, 151, 22))
        self.ableNowSpinBox.setObjectName("ableNowSpinBox")
        self.label_4 = QtWidgets.QLabel(self.inventoryWidgetsGroupBox)
        self.label_4.setGeometry(QtCore.QRect(10, 40, 141, 16))
        self.label_4.setObjectName("label_4")
        self.reservedSpinBox = QtWidgets.QSpinBox(self.inventoryWidgetsGroupBox)
        self.reservedSpinBox.setGeometry(QtCore.QRect(240, 70, 151, 22))
        self.reservedSpinBox.setObjectName("reservedSpinBox")
        self.label_6 = QtWidgets.QLabel(self.inventoryWidgetsGroupBox)
        self.label_6.setGeometry(QtCore.QRect(10, 100, 61, 16))
        self.label_6.setObjectName("label_6")
        self.label_25 = QtWidgets.QLabel(self.inventoryWidgetsGroupBox)
        self.label_25.setGeometry(QtCore.QRect(140, 160, 141, 16))
        self.label_25.setObjectName("label_25")
        self.label_26 = QtWidgets.QLabel(self.inventoryWidgetsGroupBox)
        self.label_26.setGeometry(QtCore.QRect(0, 180, 101, 16))
        self.label_26.setObjectName("label_26")
        self.label_27 = QtWidgets.QLabel(self.inventoryWidgetsGroupBox)
        self.label_27.setGeometry(QtCore.QRect(180, 180, 141, 16))
        self.label_27.setObjectName("label_27")
        self.heightSpinBox = QtWidgets.QSpinBox(self.inventoryWidgetsGroupBox)
        self.heightSpinBox.setGeometry(QtCore.QRect(110, 180, 61, 22))
        self.heightSpinBox.setObjectName("heightSpinBox")
        self.posFromLeftSpinBox = QtWidgets.QSpinBox(self.inventoryWidgetsGroupBox)
        self.posFromLeftSpinBox.setGeometry(QtCore.QRect(320, 180, 71, 22))
        self.posFromLeftSpinBox.setObjectName("posFromLeftSpinBox")
        self.IdCardLineEdit = QtWidgets.QLineEdit(self.addSmthBox)
        self.IdCardLineEdit.setGeometry(QtCore.QRect(180, 60, 211, 22))
        self.IdCardLineEdit.setObjectName("IdCardLineEdit")
        self.viewInvOrUserBox = QtWidgets.QGroupBox(self.groupBox)
        self.viewInvOrUserBox.setGeometry(QtCore.QRect(410, 80, 661, 341))
        self.viewInvOrUserBox.setObjectName("viewInvOrUserBox")
        self.listView = QtWidgets.QListView(self.viewInvOrUserBox)
        self.listView.setGeometry(QtCore.QRect(400, 30, 251, 311))
        self.listView.setObjectName("listView")
        self.searchByIdLabel = QtWidgets.QLabel(self.viewInvOrUserBox)
        self.searchByIdLabel.setGeometry(QtCore.QRect(10, 30, 21, 16))
        self.searchByIdLabel.setObjectName("searchByIdLabel")
        self.searchByEmailOrNameLabel = QtWidgets.QLabel(self.viewInvOrUserBox)
        self.searchByEmailOrNameLabel.setGeometry(QtCore.QRect(10, 60, 31, 16))
        self.searchByEmailOrNameLabel.setObjectName("searchByEmailOrNameLabel")
        self.searchByIdSpinBox = QtWidgets.QSpinBox(self.viewInvOrUserBox)
        self.searchByIdSpinBox.setGeometry(QtCore.QRect(30, 30, 161, 22))
        self.searchByIdSpinBox.setObjectName("searchByIdSpinBox")
        self.searchByEmailOrNameLineEdit = QtWidgets.QLineEdit(self.viewInvOrUserBox)
        self.searchByEmailOrNameLineEdit.setGeometry(QtCore.QRect(50, 60, 161, 22))
        self.searchByEmailOrNameLineEdit.setObjectName("searchByEmailOrNameLineEdit")
        self.listLabel = QtWidgets.QLabel(self.viewInvOrUserBox)
        self.listLabel.setGeometry(QtCore.QRect(400, 10, 91, 16))
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
        self.searchByPosGroupBox.setGeometry(QtCore.QRect(0, 200, 401, 91))
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
        self.searchPushButton = QtWidgets.QPushButton(self.searchByPosGroupBox)
        self.searchPushButton.setGeometry(QtCore.QRect(20, 60, 351, 28))
        self.searchPushButton.setObjectName("searchPushButton")
        self.hideSecPushButton = QtWidgets.QPushButton(self.groupBox)
        self.hideSecPushButton.setGeometry(QtCore.QRect(410, 40, 31, 28))
        self.hideSecPushButton.setObjectName("hideSecPushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1459, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.burgerButton.setText(_translate("MainWindow", "Меню"))
        self.addInventoryButton.setText(_translate("MainWindow", "Добавить инвентарь"))
        self.changeInventoryButton.setText(_translate("MainWindow", "Изменить информацио об инвентаре и расположении"))
        self.addUserButton.setText(_translate("MainWindow", "Добавить пользователя"))
        self.changeUserInfButton.setText(_translate("MainWindow", "Просмотр и редактирование информации о пользователях"))
        self.addAdminButton.setText(_translate("MainWindow", "Добавить сотрудника"))
        self.changeAdminButton.setText(_translate("MainWindow", "Просмотр и редактирование информации о сотрудниках"))
        self.hideButton.setText(_translate("MainWindow", "-"))
        self.addSmthBox.setTitle(_translate("MainWindow", "Добавление инвентаря"))
        self.nameOrEmailLabel.setText(_translate("MainWindow", "Название"))
        self.rightsLabel.setText(_translate("MainWindow", "Кто может получить "))
        self.firstRightsCheckBox.setText(_translate("MainWindow", "Обычный пользователь"))
        self.secondRightsCheckBox.setText(_translate("MainWindow", "Редактор-модератор"))
        self.thirdRightsCheckBox_3.setText(_translate("MainWindow", "Инженер"))
        self.fourthRightsCheckBox.setText(_translate("MainWindow", "Главный инженер"))
        self.addUserOrInvButton.setText(_translate("MainWindow", "Добавить"))
        self.label_3.setText(_translate("MainWindow", "Идентификационный номер"))
        self.label_5.setText(_translate("MainWindow", "Зарезервированное  количество"))
        self.label_4.setText(_translate("MainWindow", "Доступное количество"))
        self.label_6.setText(_translate("MainWindow", "Описание"))
        self.label_25.setText(_translate("MainWindow", "Расположение в шкафу"))
        self.label_26.setText(_translate("MainWindow", "Высота(от пола)"))
        self.label_27.setText(_translate("MainWindow", "Номер от левого края"))
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
        self.searchPushButton.setText(_translate("MainWindow", "PushButton"))
        self.hideSecPushButton.setText(_translate("MainWindow", "-"))