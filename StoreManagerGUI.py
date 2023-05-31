from PySide6.QtWidgets import *


class Window:
    def __init__(self):
        self.win = QMainWindow(None)


if __name__ == '__main__':
    app = QApplication()
    w = Window()
    w.win.show()
    app.exec()
