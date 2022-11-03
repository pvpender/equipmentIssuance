from PyQt6.QtWidgets import QApplication, QWidget
from interface import MainWindow
from users import *
from user_collections import *

zero_admin = Admin(0, "superuser", "superpassword", AdminAccess(True, True, True, True, True))

user_list = UserCollection()
user_list.append_user(zero_admin)

app = QApplication([])

window = MainWindow()

app.exec()
