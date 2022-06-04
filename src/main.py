from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPixmap
import sys
import PFA
import matplotlib.pyplot as plt
from utils import get_overpass_gdf
from algo_io import AlgoIO
import subprocess


class App(PFA.Ui_MainWindow, QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.bbox = None
        self.geo_data = None
        self.pushButton.clicked.connect(self.set_map)
        self.pushButton_2.clicked.connect(self.run_dijkstra)
        self.pushButton_3.clicked.connect(self.run_bidijkstra)
        self.pushButton_4.clicked.connect(self.run_astar)
        self.pushButton_5.clicked.connect(self.run_alt)
        self.pushButton_7.clicked.connect(self.run_multiple)

        self.lineEdit.setText('56.19457')
        self.lineEdit_2.setText('57.97275')
        self.lineEdit_3.setText('56.31843')
        self.lineEdit_4.setText('58.01179')

        self.lineEdit_5.setText('56.21')
        self.lineEdit_6.setText('57.98')
        self.lineEdit_7.setText('56.28')
        self.lineEdit_8.setText('57.99')

        self.lineEdit_9.setText('56.21')
        self.lineEdit_10.setText('57.98')
        self.lineEdit_11.setText('56.28')
        self.lineEdit_12.setText('57.99')

        self.lineEdit_13.setText('56.21')
        self.lineEdit_14.setText('57.98')
        self.lineEdit_15.setText('56.28')
        self.lineEdit_16.setText('57.99')

        self.lineEdit_17.setText('56.21')
        self.lineEdit_18.setText('57.98')
        self.lineEdit_19.setText('56.28')
        self.lineEdit_20.setText('57.99')

    def set_map(self):

        try:
            lon1 = float(self.lineEdit.text())
            lat1 = float(self.lineEdit_2.text())
            lon2 = float(self.lineEdit_3.text())
            lat2 = float(self.lineEdit_4.text())
        except ValueError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Координаты не являются числом')
            msg.setWindowTitle("Error")
            msg.exec_()
            return

        if not (lon1 <= lon2 and lat1 <= lat2):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Некорректно заданная область')
            msg.setWindowTitle("Error")
            msg.exec_()
            return

        self.bbox = (lon1, lat1, lon2, lat2)

        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('off')

        print('making overpass api request')
        self.geo_data = get_overpass_gdf(f"{lat1},{lon1},{lat2},{lon2}")
        print('received response from overpass')
        gdf = self.geo_data.copy()
        gdf.crs = {"init": "epsg:4326"}
        gdf = gdf.to_crs(epsg=3857)
        fig = gdf.plot(ax=ax, linewidth=0.5).get_figure()
        ax.margins(0)
        ax.tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)
        fig.savefig('img.jpg', dpi=200)
        self.pathFindingResult.setPixmap(QPixmap('../images/img.jpg'))
        self.pathFindingResult.setScaledContents(True)
        self.pathFindingResult_2.setPixmap(QPixmap('../images/img.jpg'))
        self.pathFindingResult_2.setScaledContents(True)
        self.pathFindingResult_3.setPixmap(QPixmap('../images/img.jpg'))
        self.pathFindingResult_3.setScaledContents(True)
        self.pathFindingResult_4.setPixmap(QPixmap('../images/img.jpg'))
        self.pathFindingResult_4.setScaledContents(True)
        self.pathFindingResult_5.setPixmap(QPixmap('../images/img.jpg'))
        self.pathFindingResult_5.setScaledContents(True)

    def run_dijkstra(self):

        if self.geo_data is None:
            self.show_error_message('Не выбрана входная область')
            return

        try:
            lon1 = float(self.lineEdit_5.text())
            lat1 = float(self.lineEdit_6.text())
            lon2 = float(self.lineEdit_7.text())
            lat2 = float(self.lineEdit_8.text())
        except ValueError:
            self.show_error_message('Координаты не являются числом')
            return

        if not (lat1 > self.bbox[1] and lon1 > self.bbox[0] and lat2 < self.bbox[3] and lon2 < self.bbox[2]):
            self.show_error_message('Входные координаты не входят в рассматриваемую область')
            return

        io = AlgoIO("dijkstra", input_path="../input/input.txt", output_path="../output/output_dijkstra.txt")
        io.gdf_to_input(self.geo_data, (lon1, lat1), (lon2, lat2))
        subprocess.run(".\\PFA_.exe dijkstra input.txt", shell=True)
        print("kek")
        fig = io.get_result_fig(self.geo_data)
        print("kek")
        fig.savefig('.\\images\\img_dijkstra.jpg', dpi=200)
        print("kek")
        self.pathFindingResult_2.setPixmap(QPixmap('../images/img_dijkstra.jpg'))
        self.pathFindingResult_2.setScaledContents(True)
        self.labelDijkstraET.setText(str(io.execution_time))

    def run_bidijkstra(self):

        if self.geo_data is None:
            self.show_error_message('Не выбрана входная область')
            return

        try:
            lon1 = float(self.lineEdit_9.text())
            lat1 = float(self.lineEdit_10.text())
            lon2 = float(self.lineEdit_11.text())
            lat2 = float(self.lineEdit_12.text())
        except ValueError:
            self.show_error_message('Координаты не являются числом')
            return

        if not (lat1 > self.bbox[1] and lon1 > self.bbox[0] and lat2 < self.bbox[3] and lon2 < self.bbox[2]):
            self.show_error_message('Входные координаты не входят в рассматриваемую область')
            return

        io = AlgoIO("bidijkstra", input_path="../input/input.txt", output_path="../output/output_bidijkstra.txt")
        io.gdf_to_input(self.geo_data, (lon1, lat1), (lon2, lat2))
        subprocess.run("..\\algorithms\\PFA_.exe bidijkstra input.txt", shell=True)
        fig = io.get_result_fig(self.geo_data)
        fig.savefig('img_bidijkstra.jpg', dpi=200)
        self.pathFindingResult_3.setPixmap(QPixmap('../images/img_bidijkstra.jpg'))
        self.pathFindingResult_3.setScaledContents(True)
        self.labelBidijkstraET.setText(str(io.execution_time))

    def run_astar(self):
        if self.geo_data is None:
            self.show_error_message('Не выбрана входная область')
            return

        try:
            lon1 = float(self.lineEdit_13.text())
            lat1 = float(self.lineEdit_14.text())
            lon2 = float(self.lineEdit_15.text())
            lat2 = float(self.lineEdit_16.text())
        except ValueError:
            self.show_error_message('Координаты не являются числом')
            return

        if not (lat1 > self.bbox[1] and lon1 > self.bbox[0] and lat2 < self.bbox[3] and lon2 < self.bbox[2]):
            self.show_error_message('Входные координаты не входят в рассматриваемую область')
            return

        io = AlgoIO("astar", input_path="../input/input.txt", output_path="../output/output_astar.txt")
        io.gdf_to_input(self.geo_data, (lon1, lat1), (lon2, lat2))
        subprocess.run("..\\algorithms\\PFA_.exe astar input.txt", shell=True)
        fig = io.get_result_fig(self.geo_data)
        fig.savefig('img_astar.jpg', dpi=200)
        self.pathFindingResult_4.setPixmap(QPixmap('../images/img_astar.jpg'))
        self.pathFindingResult_4.setScaledContents(True)
        self.labelAstarET.setText(str(io.execution_time))

    def run_alt(self):
        if self.geo_data is None:
            self.show_error_message('Не выбрана входная область')
            return

        try:
            lon1 = float(self.lineEdit_17.text())
            lat1 = float(self.lineEdit_18.text())
            lon2 = float(self.lineEdit_19.text())
            lat2 = float(self.lineEdit_20.text())
        except ValueError:
            self.show_error_message('Координаты не являются числом')
            return

        if not (lat1 > self.bbox[1] and lon1 > self.bbox[0] and lat2 < self.bbox[3] and lon2 < self.bbox[2]):
            self.show_error_message('Входные координаты не входят в рассматриваемую область')
            return

        io = AlgoIO("alt", input_path="../input/input.txt", output_path="../output/output_alt.txt")
        io.gdf_to_input(self.geo_data, (lon1, lat1), (lon2, lat2))
        subprocess.run("..\\algorithms\\PFA_.exe alt input.txt", shell=True)
        fig = io.get_result_fig(self.geo_data)
        fig.savefig('img_alt.jpg', dpi=200)
        self.pathFindingResult_5.setPixmap(QPixmap('../images/img_alt.jpg'))
        self.pathFindingResult_5.setScaledContents(True)
        self.labelAltET.setText(str(io.execution_time))
        self.labelAltPT.setText(str(io.preprocessing_time))

    def run_multiple(self):

        if self.geo_data is None:
            self.show_error_message('Не выбрана входная область')
            return

        algo_used = self.comboBox.currentIndex()
        algo_names = ["dijkstra", "bidijkstra", "astar", "alt"]
        run_num = int(self.lineEdit_21.text())
        o_path = f"output_{algo_names[algo_used]}_multiple.txt"
        io = AlgoIO("alt", input_path="../input/input.txt", output_path=o_path)
        io.gdf_to_input(self.geo_data, (0, 0), (0, 0))
        print("hi")
        subprocess.run(f"..\\algorithms\\PFA_.exe {algo_names[algo_used]} input.txt multiple {run_num}", shell=True)
        print("hi")
        with open(o_path, 'r') as f:
            self.label_51.setText(f.readline())
            self.label_52.setText(f.readline())
            self.label_53.setText(f.readline())
            self.label_54.setText(f.readline())
            if algo_used != 3:
                self.label_55.setText('-')
            else:
                self.label_55.setText(f.readline())
            self.label_56.setText(f.readline())
            self.label_57.setText(f.readline())
            self.label_58.setText(f.readline())
            self.label_59.setText(f.readline())

            exec_times = list(map(float, f.readline().split()))
            path_lengths = list(map(int, f.readline().split()))



        #sns.histplot(data=pd.DataFrame({"Время выполнения":path_lengths}), x="Время выполнения").get_figure().savefig("execution_times.png")
        #print("hi")
        #self.label_35.setPixmap(QPixmap('execution_times.png'))
        #self.label_35.setScaledContents(True)
        #print("hi")


    def show_error_message(self, text="Error"):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(text)
        msg.setWindowTitle("Error")
        msg.exec_()


def run_application():
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    run_application()
