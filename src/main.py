from PyQt5 import QtWidgets
import sys
from app import App
import pickle

def run_application():
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    ret = app.exec_()

    for algo in window.algorithms:
        algo.unset_tab()

    outputFile = open('../session/session.pfa', 'wb')

    pickle.dump(window.algorithms, outputFile)
    outputFile.close()
    with open('../session/session.pfa', 'rb') as f:
        w_list = pickle.load(f)
    for w in w_list:
        print(w)
    sys.exit(ret)


if __name__ == '__main__':
    run_application()
