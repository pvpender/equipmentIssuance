from PyQt6.QtWidgets import QApplication, QWidget
from interface import MainWindow
from users import *
from user_collections import *


app = QApplication([])

window = MainWindow()
window.show()

app.exec()
