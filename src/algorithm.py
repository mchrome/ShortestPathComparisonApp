from argument import Argument
from algo_io import AlgoIO
from PyQt5 import QtCore, QtGui, QtWidgets
import subprocess
from PyQt5.QtGui import QPixmap
from output_format import OutputFormatItem
from PyQt5.QtWidgets import QTableWidgetItem

class Algorithm:

    def __init__(self, id: int, name: str, path: str, gdf):
        self.id = id
        self.name = name
        self.path = path
        self.arguments = []
        self.output_format : list[OutputFormatItem] = []
        self.ui_tab = None
        self.gdf = gdf

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

    def run(self):
        try:
            print('hi run algo')

            if self.gdf is None:
                #self.show_error_message('Не выбрана входная область')
                return

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
            # if not (lat1 > self.bbox[1] and lon1 > self.bbox[0] and lat2 < self.bbox[3] and lon2 < self.bbox[2]):
            #     self.show_error_message('Входные координаты не входят в рассматриваемую область')
            #     return

            io = AlgoIO(self.output_format,
                        input_path="../input/input.txt",
                        output_path="../output/output_"+str(self.id)+".txt")

            io.gdf_to_input(self.gdf, (lon1, lat1), (lon2, lat2))

            shell_command = ""
            shell_command += self.path + " "
            print("hi 2")
            tableWidgetWithParams = self.ui_tab.findChild(QtWidgets.QTableWidget,
                                                   "algo_" + str(self.id) + "_" + "tableWidget_1")
            for i in range(tableWidgetWithParams.rowCount()):
                shell_command += tableWidgetWithParams.item(i, 1).text() + " "

            print("SHELL COMMAND: ", shell_command)
            subprocess.run(shell_command, shell=True)

            print("AAAA")
            fig, numbers = io.parse_output(self.gdf)
            fig.savefig('..\\images\\img_'+'algo_'+str(self.id)+'.jpg', dpi=200)

            pathFindingResult = self.ui_tab.findChild(QtWidgets.QLabel,
                                                   "algo_" + str(self.id) + "_pathFindingResult_1")

            pathFindingResult.setPixmap(QPixmap('..\\images\\img_'+'algo_'+str(self.id)+'.jpg'))
            pathFindingResult.setScaledContents(True)

            tableWidgetWithNumbers = self.ui_tab.findChild(QtWidgets.QTableWidget,
                                                   "algo_" + str(self.id) + "_" + "tableWidget_2")
            for i in range(tableWidgetWithNumbers.rowCount()):
                tableWidgetWithNumbers.setItem(i,
                                               1,
                                               QTableWidgetItem(str(numbers[i][0])))

        except Exception as e:
            print(e)