from PyQt6.QtWidgets import QApplication, QWidget
from interface import MainWindow

app = QApplication([])

window = MainWindow()
window.show()

app.exec()
