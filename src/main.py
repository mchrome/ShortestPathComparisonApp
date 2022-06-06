from PyQt5 import QtWidgets
import sys
from app import App


def run_application():
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    run_application()
