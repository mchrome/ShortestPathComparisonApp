from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QTableWidgetItem
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import PFA
import matplotlib.pyplot as plt
from utils import get_overpass_gdf
from algo_io import AlgoIO
import subprocess
from algorithm import Algorithm
from output_format import OutputFormatItem


class App(PFA.Ui_MainWindow, QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.bbox = None
        self.geo_data = None
        self.tab_cnt = 1

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

        self.pushButton_8.clicked.connect(self.open_file_dialog)

        self.algorithms: list[Algorithm] = []

        self.pushButton_9.clicked.connect(self.add_algo_parameter)
        self.pushButton_12.clicked.connect(self.add_output_format)
        self.pushButton_11.clicked.connect(self.delete_output_format)

        self.radioButton.clicked.connect(self.std_output_set)
        self.radioButton_2.clicked.connect(self.file_output_set)
        self.radioButton_3.clicked.connect(self.output_format_vertex_set)
        self.radioButton_4.clicked.connect(self.output_format_edge_set)

        self.pushButton_15.clicked.connect(self.add_algorithm)

    def add_algorithm(self):
        self.algorithms.append(Algorithm(id=self.tab_cnt,
                                         name=self.lineEdit_27.text(),
                                         path=self.lineEdit_22.text(),
                                         gdf=self.geo_data))

        for i in range(self.listWidget_2.count()):
            self.algorithms[-1].add_argument(self.listWidget_2.item(i).text())

        for i in range(self.tableWidget.rowCount()):
            name = self.tableWidget.item(i, 0).text()
            type = self.tableWidget.item(i, 1).text()
            color = self.tableWidget.item(i, 2).text()

            self.algorithms[-1].add_output_format(OutputFormatItem(name, type, color))

        self.algorithms[-1].set_tab(self.add_algorithm_tab(self.algorithms[-1]))

    def add_algorithm_tab(self, algo: Algorithm):

        tab = QtWidgets.QWidget()
        tab.setObjectName("tab_algo_" + str(self.tab_cnt))

        gb_cnt = 1
        le_cnt = 1
        lb_cnt = 1
        tble_cnt = 1
        pb_cnt = 1

        # Координаты
        groupBox = QtWidgets.QGroupBox(tab)
        groupBox.setGeometry(QtCore.QRect(1030, 10, 231, 131))
        groupBox.setObjectName("algo_" + str(self.tab_cnt) + "_" + "groupBox_" + str(gb_cnt))
        groupBox.setTitle("Входные данные")
        gb_cnt += 1

        lineEdit = QtWidgets.QLineEdit(groupBox)
        lineEdit.setGeometry(QtCore.QRect(30, 40, 81, 20))
        lineEdit.setObjectName("algo_" + str(self.tab_cnt) + "_" + "lineEdit_" + str(le_cnt))
        le_cnt += 1

        lineEdit_2 = QtWidgets.QLineEdit(groupBox)
        lineEdit_2.setGeometry(QtCore.QRect(140, 40, 81, 20))
        lineEdit_2.setObjectName("algo_" + str(self.tab_cnt) + "_" + "lineEdit_" + str(le_cnt))
        le_cnt += 1

        lineEdit_3 = QtWidgets.QLineEdit(groupBox)
        lineEdit_3.setGeometry(QtCore.QRect(30, 90, 81, 20))
        lineEdit_3.setObjectName("algo_" + str(self.tab_cnt) + "_" + "lineEdit_" + str(le_cnt))
        le_cnt += 1

        lineEdit_4 = QtWidgets.QLineEdit(groupBox)
        lineEdit_4.setGeometry(QtCore.QRect(140, 90, 81, 20))
        lineEdit_4.setObjectName("algo_" + str(self.tab_cnt) + "_" + "lineEdit_" + str(le_cnt))
        le_cnt += 1

        lineEdit.setText('56.21')
        lineEdit_2.setText('57.98')
        lineEdit_3.setText('56.28')
        lineEdit_4.setText('57.99')

        label = QtWidgets.QLabel(groupBox)
        label.setGeometry(QtCore.QRect(90, 20, 111, 16))
        label.setObjectName("algo_" + str(self.tab_cnt) + "_" + "label_" + str(lb_cnt))
        lb_cnt += 1

        label_2 = QtWidgets.QLabel(groupBox)
        label_2.setGeometry(QtCore.QRect(80, 70, 111, 16))
        label_2.setObjectName("algo_" + str(self.tab_cnt) + "_" + "label_" + str(lb_cnt))
        lb_cnt += 1

        label_3 = QtWidgets.QLabel(groupBox)
        label_3.setGeometry(QtCore.QRect(10, 40, 16, 16))
        label_3.setObjectName("algo_" + str(self.tab_cnt) + "_" + "label_" + str(lb_cnt))
        lb_cnt += 1

        label_4 = QtWidgets.QLabel(groupBox)
        label_4.setGeometry(QtCore.QRect(10, 90, 16, 16))
        label_4.setObjectName("algo_" + str(self.tab_cnt) + "_" + "label_" + str(lb_cnt))
        lb_cnt += 1

        label_5 = QtWidgets.QLabel(groupBox)
        label_5.setGeometry(QtCore.QRect(120, 40, 16, 16))
        label_5.setObjectName("algo_" + str(self.tab_cnt) + "_" + "label_" + str(lb_cnt))
        lb_cnt += 1

        label_6 = QtWidgets.QLabel(groupBox)
        label_6.setGeometry(QtCore.QRect(120, 90, 16, 16))
        label_6.setObjectName("algo_" + str(self.tab_cnt) + "_" + "label_" + str(lb_cnt))
        lb_cnt += 1

        label.setText("Начало пути")
        label_2.setText("Точка назначения")
        label_3.setText("Д:")
        label_4.setText("Д:")
        label_5.setText("Ш:")
        label_6.setText("Ш:")

        # Параметры
        groupBox = QtWidgets.QGroupBox(tab)
        groupBox.setGeometry(QtCore.QRect(1030, 150, 231, 211))
        groupBox.setObjectName("algo_" + str(self.tab_cnt) + "_" + "groupBox_" + str(gb_cnt))
        groupBox.setTitle("Параметры программы")
        gb_cnt += 1

        tableWidget = QtWidgets.QTableWidget(groupBox)
        tableWidget.setGeometry(QtCore.QRect(10, 20, 211, 181))
        tableWidget.setObjectName("algo_" + str(self.tab_cnt) + "_" + "tableWidget_" + str(tble_cnt))
        tableWidget.setColumnCount(2)
        tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Название")
        tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Значение")
        tableWidget.setHorizontalHeaderItem(1, item)
        tble_cnt += 1

        # Добавление в интерфейс параметров
        for i in range(len(algo.arguments)):
            tableWidget.insertRow(tableWidget.rowCount())
            tableWidget.setItem(tableWidget.rowCount() - 1, 0, QTableWidgetItem(algo.arguments[i]))

        # Файлы ввода-вывода в параметрах
        tableWidget.setItem(0, 1, QTableWidgetItem('../input/input.txt'))
        tableWidget.setItem(1, 1, QTableWidgetItem("../output/output_"+str(algo.id)+".txt"))

        # Числовой вывод

        groupBox = QtWidgets.QGroupBox(tab)
        groupBox.setGeometry(QtCore.QRect(1030, 430, 231, 211))
        groupBox.setObjectName("algo_" + str(self.tab_cnt) + "_" + "groupBox_" + str(gb_cnt))
        groupBox.setTitle("Числовые характеристики")
        gb_cnt += 1

        tableWidget = QtWidgets.QTableWidget(groupBox)
        tableWidget.setGeometry(QtCore.QRect(10, 20, 211, 181))
        tableWidget.setObjectName("algo_" + str(self.tab_cnt) + "_" + "tableWidget_" + str(tble_cnt))
        tableWidget.setColumnCount(2)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Характеристика")
        tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Значение")
        tableWidget.setHorizontalHeaderItem(1, item)
        tble_cnt += 1



        # Результат
        groupBox = QtWidgets.QGroupBox(tab)
        groupBox.setGeometry(QtCore.QRect(10, 10, 1001, 681))
        groupBox.setObjectName("algo_" + str(self.tab_cnt) + "_" + "groupBox_" + str(gb_cnt))
        groupBox.setTitle("Карта дорог")
        gb_cnt += 1

        pathFindingResult = QtWidgets.QLabel(groupBox)
        pathFindingResult.setGeometry(QtCore.QRect(10, 20, 981, 651))
        pathFindingResult.setObjectName("algo_" + str(self.tab_cnt) + "_pathFindingResult_1")
        if self.geo_data is not None:
            pathFindingResult.setPixmap(QPixmap('../images/img.jpg'))
        pathFindingResult.setScaledContents(True)
        pathFindingResult.setText("")

        # Кнопка запуска

        pushButton = QtWidgets.QPushButton(tab)
        pushButton.setGeometry(QtCore.QRect(1060, 640, 181, 23))
        pushButton.setObjectName("algo_" + str(self.tab_cnt) + "_" + "pushButton_" + str(pb_cnt))
        pushButton.setText("Запустить")
        pushButton.clicked.connect(
            self.algorithms[-1].run)  ########################################################################
        pb_cnt += 1

        self.tabWidget.addTab(tab, algo.name)

        self.tab_cnt += 1

        return tab

    def connect_algo(self):
        self.algorithms[-1].run()

    def output_format_vertex_set(self):
        self.radioButton_3.setChecked(True)
        self.radioButton_4.setChecked(False)

    def output_format_edge_set(self):
        self.radioButton_3.setChecked(False)
        self.radioButton_4.setChecked(True)

    def add_output_format(self):

        # self.add_cnt_output_format()

        self.tableWidget.insertRow(self.tableWidget.rowCount())

        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, QTableWidgetItem(self.lineEdit_25.text()))

        if self.radioButton_3.isChecked():
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, QTableWidgetItem("Вершины"))
        else:
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, QTableWidgetItem("Дуги"))

        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 2, QTableWidgetItem(self.comboBox_2.currentText()))

    def delete_output_format(self):
        for indx in self.tableWidget.selectionModel().selectedRows():
            print(indx.row())
            self.tableWidget.removeRow(indx.row())

    def add_cnt_output_format(self):
        self.tableWidget.insertRow(self.tableWidget.rowCount())
        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0,
                                 QTableWidgetItem("Количество " + self.lineEdit_25.text()))
        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, QTableWidgetItem("Число"))
        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 2, QTableWidgetItem("-"))

    def std_output_set(self):
        self.lineEdit_24.setEnabled(False)
        self.radioButton.setChecked(True)
        self.radioButton_2.setChecked(False)

    def file_output_set(self):
        self.lineEdit_24.setEnabled(True)
        self.radioButton.setChecked(False)
        self.radioButton_2.setChecked(True)

    def add_algo_parameter(self):
        parameter_name = self.lineEdit_23.text()
        self.listWidget_2.addItem(parameter_name)

    def open_file_dialog(self):
        filename = QFileDialog.getOpenFileName(self, "Open File", "", "All files (*);;Executable files (*.exe)")
        if filename:
            self.lineEdit_22.setText(filename[0])

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
        fig = gdf.plot(ax=ax, linewidth=0.5)
        fig = fig.get_figure()

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

        for algo in self.algorithms:
            tab = algo.ui_tab
            print(tab)
            map_lbl = tab.findChild(QtWidgets.QLabel,
                                    "algo_" + str(algo.id) + "_pathFindingResult_1")

            algo.set_geo_data(self.geo_data)
            print(map_lbl)
            map_lbl.setPixmap(QPixmap('../images/img.jpg'))
            print(1)

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
        subprocess.run(".\\PFA_.exe dijkstra inpt.txt", shell=True)
        fig = io.get_result_fig(self.geo_data)
        fig.savefig('.\\images\\img_dijkstra.jpg', dpi=200)
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
        subprocess.run("..\\algorithms\\PFA_.exe bidijkstra inpt.txt", shell=True)
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
        subprocess.run("..\\algorithms\\PFA_.exe astar inpt.txt", shell=True)
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
        subprocess.run("..\\algorithms\\PFA_.exe alt inpt.txt", shell=True)
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
        subprocess.run(f"..\\algorithms\\PFA_.exe {algo_names[algo_used]} inpt.txt multiple {run_num}", shell=True)
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

        # sns.histplot(data=pd.DataFrame({"Время выполнения":path_lengths}), x="Время выполнения").get_figure().savefig("execution_times.png")
        # print("hi")
        # self.label_35.setPixmap(QPixmap('execution_times.png'))
        # self.label_35.setScaledContents(True)
        # print("hi")

    def show_error_message(self, text="Error"):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(text)
        msg.setWindowTitle("Error")
        msg.exec_()
