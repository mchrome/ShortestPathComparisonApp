from argument import Argument
from algo_io import AlgoIO
from PyQt5 import QtCore, QtGui, QtWidgets
import subprocess
from PyQt5.QtGui import QPixmap
from output_format import OutputFormatItem
from PyQt5.QtWidgets import QTableWidgetItem
import geopandas as gpd

class Algorithm:

    def __init__(self, id: int, name: str, path: str, gdf):
        self.id = id
        self.name = name
        self.path = path
        self.arguments = []
        self.output_format : list[OutputFormatItem] = []
        self.ui_tab = None
        self.gdf = gdf
        self.checker = None

    def set_checker(self, checker):
        self.checker = checker

    def set_geo_data(self, gdf):
        self.gdf = gdf

    def add_argument(self, argument):
        self.arguments.append(argument)

    def remove_argument(self, id: int):
        self.arguments.pop(id)

    def add_output_format(self, item: OutputFormatItem):
        self.output_format.append(item)

    def set_tab(self, tab):
        self.ui_tab = tab

    def unset_tab(self):
        self.ui_tab = None

    def run_tab(self):
        try:
            try:
                lon1 = float(self.ui_tab.findChild(QtWidgets.QLineEdit,
                                                   "algo_" + str(self.id) + "_" + "lineEdit_1").text())
                lat1 = float(self.ui_tab.findChild(QtWidgets.QLineEdit,
                                                   "algo_" + str(self.id) + "_" + "lineEdit_2").text())
                lon2 = float(self.ui_tab.findChild(QtWidgets.QLineEdit,
                                                   "algo_" + str(self.id) + "_" + "lineEdit_3").text())
                lat2 = float(self.ui_tab.findChild(QtWidgets.QLineEdit,
                                                   "algo_" + str(self.id) + "_" + "lineEdit_4").text())
            except ValueError:
                self.show_error_message('Координаты некорректны')
                return

            if self.gdf is None:
                # self.show_error_message('Не выбрана входная область')
                return

            # if not (lat1 > self.bbox[1] and lon1 > self.bbox[0] and lat2 < self.bbox[3] and lon2 < self.bbox[2]):
            #     self.show_error_message('Входные координаты не входят в рассматриваемую область')
            #     return

            io = AlgoIO(self.output_format,
                        input_path="../input/input.txt",
                        output_path="../output/output_" + str(self.id) + ".txt")

            tableWidgetWithParams = self.ui_tab.findChild(QtWidgets.QTableWidget,
                                                          "algo_" + str(self.id) + "_" + "tableWidget_1")

            params = []

            for i in range(tableWidgetWithParams.rowCount()):
                params.append(tableWidgetWithParams.item(i, 1).text())

            self.run(lon1, lat1, lon2, lat2, params, io)

            print()

            fig, numbers = io.make_map_with_result(self.gdf)

            show_correct = self.ui_tab.findChild(QtWidgets.QCheckBox,
                                                          'checkBox_correct').isChecked()

            if show_correct:
                params_correct = params
                params_correct[1] = '../output/correct.txt'
                io_checked = AlgoIO(self.checker.output_format,
                                    input_path="../input/input.txt",
                                    output_path='../output/correct.txt')
                self.checker.run(lon1, lat1, lon2, lat2, params, io_checked)
                correct_path = io_checked.get_path_from_output()
                correct_path_gdf = gpd.GeoDataFrame(geometry=correct_path)
                correct_path_gdf.crs = {"init": "epsg:4326"}
                correct_path_gdf = correct_path_gdf.to_crs(epsg=3857)
                fig = correct_path_gdf.plot(ax = fig.get_axes()[0], color='green').get_figure()


            fig.savefig('..\\images\\img_' + 'algo_' + str(self.id) + '.jpg', dpi=200)

            pathFindingResult = self.ui_tab.findChild(QtWidgets.QLabel,
                                                      "algo_" + str(self.id) + "_pathFindingResult_1")

            pathFindingResult.setPixmap(QPixmap('..\\images\\img_' + 'algo_' + str(self.id) + '.jpg'))
            pathFindingResult.setScaledContents(True)

            tableWidgetWithNumbers = self.ui_tab.findChild(QtWidgets.QTableWidget,
                                                           "algo_" + str(self.id) + "_" + "tableWidget_2")
            for i in range(tableWidgetWithNumbers.rowCount()):
                tableWidgetWithNumbers.setItem(i,
                                               1,
                                               QTableWidgetItem(str(numbers[i][0])))
        except Exception as e:
            print(e)

    def run(self, lon1, lat1, lon2, lat2, params, io):
        try:

            io.gdf_to_input(self.gdf, (lon1, lat1), (lon2, lat2))

            shell_command = ""
            shell_command += self.path + " "

            for param in params:
                shell_command += param + " "

            print("SHELL COMMAND: ", shell_command)
            subprocess.run(shell_command, shell=True)



        except Exception as e:
            print(e)