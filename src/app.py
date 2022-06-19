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
import os
import random


class App(PFA.Ui_MainWindow, QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.bbox = None
        self.geo_data = None
        self.tab_cnt = 1

        self.pushButton.clicked.connect(self.set_map)
        self.pushButton_7.clicked.connect(self.run_multiple)

        self.lineEdit.setText('56.19457')
        self.lineEdit_2.setText('57.97275')
        self.lineEdit_3.setText('56.31843')
        self.lineEdit_4.setText('58.01179')

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

        # Сессии
        # self.action_4.triggered.connect(self.kek)

        self.init_base_algorithms()

        self.comboBox.currentIndexChanged.connect(self.show_first_algo_args)
        self.comboBox_3.currentIndexChanged.connect(self.show_second_algo_args)

        self.pushButton_3.clicked.connect(self.show_stat_first)
        self.pushButton_4.clicked.connect(self.show_stat_second)

        self.pushButton_2.clicked.connect(self.show_first_algo_result)
        self.pushButton_5.clicked.connect(self.show_second_algo_result)

    def show_first_algo_result(self):
        try:
            first_algo = self.algorithms[self.comboBox.currentIndex()]

            if len(self.tableWidget_2.selectionModel().selectedRows()) == 0:
                return

            test_num = self.tableWidget_2.selectionModel().selectedRows()[0].row()

            lon1 = self.tableWidget_2.item(test_num, 0).text()
            lat1 = self.tableWidget_2.item(test_num, 1).text()
            lon2 = self.tableWidget_2.item(test_num, 2).text()
            lat2 = self.tableWidget_2.item(test_num, 3).text()

            first_algo.ui_tab.findChild(QtWidgets.QLineEdit,
                                  "algo_" + str(first_algo.id) + "_" + "lineEdit_1").setText(lon1)
            first_algo.ui_tab.findChild(QtWidgets.QLineEdit,
                                  "algo_" + str(first_algo.id) + "_" + "lineEdit_2").setText(lat1)
            first_algo.ui_tab.findChild(QtWidgets.QLineEdit,
                                  "algo_" + str(first_algo.id) + "_" + "lineEdit_3").setText(lon2)
            first_algo.ui_tab.findChild(QtWidgets.QLineEdit,
                                  "algo_" + str(first_algo.id) + "_" + "lineEdit_4").setText(lat2)

            first_algo.ui_tab.findChild(QtWidgets.QCheckBox,
                                  'checkBox_correct').setChecked(True)

            first_algo.run_tab()

            self.tabWidget.setCurrentIndex(self.comboBox.currentIndex()+3)

        except Exception as e:
            print(e)

    def show_second_algo_result(self):

        try:
            second_algo = self.algorithms[self.comboBox_3.currentIndex()]

            if len(self.tableWidget_2.selectionModel().selectedRows()) == 0:
                return

            test_num = self.tableWidget_2.selectionModel().selectedRows()[0].row()

            lon1 = self.tableWidget_2.item(test_num, 0).text()
            lat1 = self.tableWidget_2.item(test_num, 1).text()
            lon2 = self.tableWidget_2.item(test_num, 2).text()
            lat2 = self.tableWidget_2.item(test_num, 3).text()

            second_algo.ui_tab.findChild(QtWidgets.QLineEdit,
                                        "algo_" + str(second_algo.id) + "_" + "lineEdit_1").setText(lon1)
            second_algo.ui_tab.findChild(QtWidgets.QLineEdit,
                                        "algo_" + str(second_algo.id) + "_" + "lineEdit_2").setText(lat1)
            second_algo.ui_tab.findChild(QtWidgets.QLineEdit,
                                        "algo_" + str(second_algo.id) + "_" + "lineEdit_3").setText(lon2)
            second_algo.ui_tab.findChild(QtWidgets.QLineEdit,
                                        "algo_" + str(second_algo.id) + "_" + "lineEdit_4").setText(lat2)

            second_algo.ui_tab.findChild(QtWidgets.QCheckBox,
                                        'checkBox_correct').setChecked(True)

            second_algo.run_tab()

            self.tabWidget.setCurrentIndex(self.comboBox_3.currentIndex() + 3)

        except Exception as e:
            print(e)

    def make_stat_graph(self, data_path, format, runs, x_id, y_id, out_path):
        try:
            x = []
            y = []
            print(x_id, y_id)
            for run in range(runs):
                with open(data_path+str(run)+'.txt', 'r') as f:
                    for i, format_item in enumerate(format):
                        print(i, format_item.type)
                        if format_item.type == "Вершины" or format_item.type == "Дуги":
                            count = int(f.readline())
                            for j in range(count):
                                f.readline()
                            if i == x_id:
                                x.append(float(count))
                            elif i == y_id:
                                y.append(float(count))
                        if format_item.type == "Числа":
                            number_count = int(f.readline())
                            for j in range(number_count):
                                print(j,x_id,y_id)
                                if i == x_id:
                                    x.append(float(f.readline()))
                                elif i == y_id:
                                    y.append(float(f.readline()))
                                else:
                                    f.readline()
            print(x)
            print(y)

            res = sorted(zip(x,y))

            x_res = []
            y_res = []
            for i in range(len(res)):
                x_res.append(res[i][0])
                y_res.append(res[i][1])

            print(x_res)
            print(y_res)

            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)
            ax.plot(x_res, y_res)

            if format[x_id].name != "Числа":
                ax.set_xlabel("Количество " + format[x_id].name)
            else:
                ax.set_xlabel(format[x_id].name)

            if format[y_id].name != "Числа":
                ax.set_ylabel("Количество " + format[y_id].name)
            else:
                ax.set_ylabel(format[y_id].name)

            fig.savefig(out_path)
        except Exception as e:
            print(e)

    def show_stat_first(self):
        first_algo = self.algorithms[self.comboBox.currentIndex()]
        self.make_stat_graph("../output/first_multiple_output/",  first_algo.output_format,
                             int(self.lineEdit_21.text()),
                             self.comboBox_4.currentIndex(),
                             self.comboBox_5.currentIndex(),
                             '../images/first_testing_graph.jpg')
        self.label_11.setPixmap(QPixmap('../images/first_testing_graph.jpg'))
        self.label_11.setScaledContents(True)

    def show_stat_second(self):
        second_algo = self.algorithms[self.comboBox_3.currentIndex()]
        self.make_stat_graph("../output/second_multiple_output/", second_algo.output_format,
                                  int(self.lineEdit_21.text()),
                                  self.comboBox_6.currentIndex(),
                                  self.comboBox_7.currentIndex(),
                             '../images/second_testing_graph.jpg')
        self.label_12.setPixmap(QPixmap('../images/second_testing_graph.jpg'))
        self.label_12.setScaledContents(True)

    def show_first_algo_args(self):

        self.tableWidget_3.setRowCount(0)

        first_algo = self.algorithms[self.comboBox.currentIndex()]

        for i in range(len(first_algo.arguments)):
            self.tableWidget_3.insertRow(self.tableWidget_3.rowCount())
            self.tableWidget_3.setItem(self.tableWidget_3.rowCount() - 1, 0, QTableWidgetItem(first_algo.arguments[i]))
        self.tableWidget_3.setItem(0, 1, QTableWidgetItem('../input/input.txt'))
        self.tableWidget_3.setItem(1, 1, QTableWidgetItem(
            "../output/first_multiple_output" + "/"))

    def show_second_algo_args(self):
        self.tableWidget_4.setRowCount(0)

        second_algo = self.algorithms[self.comboBox_3.currentIndex()]

        for i in range(len(second_algo.arguments)):
            self.tableWidget_4.insertRow(self.tableWidget_4.rowCount())
            self.tableWidget_4.setItem(self.tableWidget_4.rowCount() - 1, 0, QTableWidgetItem(second_algo.arguments[i]))
        self.tableWidget_4.setItem(0, 1, QTableWidgetItem('../input/input.txt'))
        self.tableWidget_4.setItem(1, 1, QTableWidgetItem(
            "../output/second_multiple_output" + "/"))

    def fill_testing_combobox(self):
        for algo in self.algorithms:
            self.comboBox.addItem(algo.name)
            self.comboBox_3.addItem(algo.name)
        self.show_first_algo_args()
        self.show_second_algo_args()

    def init_base_algorithms(self):

        algo_names = {'dijkstra.exe': 'Алгоритм Дейкстры',
                      'bidijkstra.exe': 'Двунаправленный алгоритм Дейкстры',
                      'astar.exe': 'A*',
                      'alt.exe': 'ALT'}

        for dir_path, _, filenames in os.walk('../algorithms'):
            for f in filenames:
                self.algorithms.append(Algorithm(id=self.tab_cnt,
                                                 name=algo_names[f],
                                                 path=os.path.abspath(os.path.join(dir_path, f)),
                                                 gdf=self.geo_data))

                self.algorithms[-1].add_argument('Файл ввода')
                self.algorithms[-1].add_argument('Файл вывода')

                self.algorithms[-1].add_output_format(OutputFormatItem(
                    'Кратчайший путь',
                    'Дуги',
                    'red'))

                self.algorithms[-1].add_output_format(OutputFormatItem(
                    'Проверенные дуги',
                    'Дуги',
                    'black'))



                self.algorithms[-1].add_output_format(OutputFormatItem(
                    'Время выполнения',
                    'Числа',
                    '-'))

                if f == 'alt.exe':
                    self.algorithms[-1].add_output_format(OutputFormatItem(
                        'Ориентиры',
                        'Вершины',
                        'yellow'))
                    self.algorithms[-1].add_output_format(OutputFormatItem(
                        'Время предобработки',
                        'Числа',
                        '-'))

                self.algorithms[-1].set_tab(self.add_algorithm_tab(self.algorithms[-1]))

        for algo in self.algorithms:
            algo.set_checker(self.algorithms[0])

        self.fill_testing_combobox()

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
        self.fill_testing_combobox()

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

        # Показывать корректный путь
        checkBox = QtWidgets.QCheckBox(tab)
        checkBox.setObjectName('checkBox_correct')
        checkBox.setGeometry(QtCore.QRect(1040,390,250,17))
        checkBox.setText('Показать корректный кратчайший путь')

        # Добавление в интерфейс параметров
        for i in range(len(algo.arguments)):
            tableWidget.insertRow(tableWidget.rowCount())
            tableWidget.setItem(tableWidget.rowCount() - 1, 0, QTableWidgetItem(algo.arguments[i]))

        # Файлы ввода-вывода в параметрах
        tableWidget.setItem(0, 1, QTableWidgetItem('../input/input.txt'))
        tableWidget.setItem(1, 1, QTableWidgetItem("../output/output_" + str(algo.id) + ".txt"))

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

        # Добавление числовых характеристик алгоритма

        for output_item in algo.output_format:
            if output_item.type == 'Числа':
                tableWidget.insertRow(tableWidget.rowCount())
                tableWidget.setItem(tableWidget.rowCount() - 1, 0, QTableWidgetItem(output_item.name))

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
            self.algorithms[-1].run_tab)
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

        self.tableWidget.insertRow(self.tableWidget.rowCount())

        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, QTableWidgetItem(self.lineEdit_25.text()))

        if self.radioButton_3.isChecked():
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, QTableWidgetItem("Вершины"))
        if self.radioButton_4.isChecked():
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, QTableWidgetItem("Дуги"))
        if self.radioButton_5.isChecked():
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, QTableWidgetItem("Числа"))

        if not self.radioButton_5.isChecked():
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1,
                                     2,
                                     QTableWidgetItem(self.comboBox_2.currentText()))
        else:
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1,
                                     2,
                                     QTableWidgetItem('-'))

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
        fig.savefig('../images/img.jpg', dpi=200)
        self.pathFindingResult.setPixmap(QPixmap('../images/img.jpg'))
        self.pathFindingResult.setScaledContents(True)

        for algo in self.algorithms:
            tab = algo.ui_tab
            print(tab)
            map_lbl = tab.findChild(QtWidgets.QLabel,
                                    "algo_" + str(algo.id) + "_pathFindingResult_1")

            algo.set_geo_data(self.geo_data)
            print(map_lbl)
            map_lbl.setPixmap(QPixmap('../images/img.jpg'))
            print(1)

    def generate_coords(self):
        return (random.uniform(self.bbox[0], self.bbox[2]), random.uniform(self.bbox[1], self.bbox[3]))

    def run_multiple(self):
        try:
            if self.geo_data is None:
                self.show_error_message('Не выбрана входная область')
                return

            self.tableWidget_2.setRowCount(0)

            first_algo = self.algorithms[self.comboBox.currentIndex()]
            second_algo = self.algorithms[self.comboBox_3.currentIndex()]

            params_first = []
            params_second = []

            for i in range(self.tableWidget_3.rowCount()):
                params_first.append(self.tableWidget_3.item(i, 1).text())

            for i in range(self.tableWidget_4.rowCount()):
                params_second.append(self.tableWidget_4.item(i, 1).text())


            cnt_correct = 0
            for i in range(int(self.lineEdit_21.text())):
                start_lon, start_lan = self.generate_coords()
                end_lon, end_lat = self.generate_coords()

                param_first_cur = params_first.copy()
                param_second_cur = params_second.copy()
                param_first_cur[1] += str(i) + '.txt'
                param_second_cur[1] += str(i) + '.txt'

                io_first = AlgoIO(first_algo.output_format, param_first_cur[0], param_first_cur[1])
                io_second = AlgoIO(second_algo.output_format, param_second_cur[0], param_second_cur[1])

                first_algo.run(start_lon, start_lan, end_lon, end_lat, param_first_cur, io_first)
                second_algo.run(start_lon, start_lan, end_lon, end_lat, param_second_cur, io_second)

                path_first = io_first.get_path_from_output()
                path_second = io_second.get_path_from_output()

                print(len(path_first), len(path_second))

                self.tableWidget_2.insertRow(self.tableWidget_2.rowCount())
                self.tableWidget_2.setItem(self.tableWidget_2.rowCount() - 1, 0, QTableWidgetItem(str(start_lon)))
                self.tableWidget_2.setItem(self.tableWidget_2.rowCount() - 1, 1, QTableWidgetItem(str(start_lan)))
                self.tableWidget_2.setItem(self.tableWidget_2.rowCount() - 1, 2, QTableWidgetItem(str(end_lon)))
                self.tableWidget_2.setItem(self.tableWidget_2.rowCount() - 1, 3, QTableWidgetItem(str(end_lat)))

                if path_first == path_second:
                    self.tableWidget_2.setItem(self.tableWidget_2.rowCount() - 1, 4, QTableWidgetItem('OK'))
                    cnt_correct+=1
                else:
                    self.tableWidget_2.setItem(self.tableWidget_2.rowCount() - 1, 4, QTableWidgetItem('Different'))


            self.label_13.setText(f'{cnt_correct} из {self.lineEdit_21.text()}')
            self.fill_graph_comboboxes()

        except Exception as e:
            print(e)

    def fill_graph_comboboxes(self):

        first_algo = self.algorithms[self.comboBox.currentIndex()]
        second_algo = self.algorithms[self.comboBox_3.currentIndex()]

        for item in first_algo.output_format:
            self.comboBox_4.addItem(item.name)
            self.comboBox_5.addItem(item.name)

        for item in second_algo.output_format:
            self.comboBox_6.addItem(item.name)
            self.comboBox_7.addItem(item.name)

    def show_error_message(self, text="Error"):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(text)
        msg.setWindowTitle("Error")
        msg.exec_()
