from PyQt6.QtWidgets import QMainWindow


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("App")
        self.resize(1280, 720)
