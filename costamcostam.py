from PyQt4 import QtGui, QtCore
import sys
###aplikacja
class App(QtGui.QApplication):
    def __init__(self, *args):
        QtGui.QApplication.__init__(self, *args)
        self.main = MainWindow()
        self.main.setGeometry(QtCore.QRect(100,100,800,600))
        self.connect(self, QtCore.SIGNAL("lastWindowClosed()"), self.byebye )
        self.main.show()
    def byebye( self ):
        self.exit(0)


###glowne okno
class MainWindow(QtGui.QMainWindow):
    def __init__(self, *args):
        QtGui.QMainWindow.__init__(self, *args)
        self.cw = QtGui.QWidget(self)
        self.setWindowTitle("Pobieracz")
        self.setCentralWidget(self.cw)
        self.btn1 = QtGui.QPushButton("New", self.cw)
        self.btn1.setGeometry(QtCore.QRect(10, 10, 100, 60))
        self.connect(self.btn1,QtCore.SIGNAL("clicked()"), self.updatet)
        self.tableWidget = QtGui.QTableWidget(self.cw)
        self.tableWidget.setGeometry(QtCore.QRect(140, 110, 550, 300))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(11)
        #self.tableWidget.setEnabled(False)

        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, QtGui.QTableWidgetItem("cos"))
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, QtGui.QTableWidgetItem("cos2"))
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, QtGui.QTableWidgetItem("cos3"))
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)

    def updatet(self):
        with open("json_file","rb") as file:
            x = file.readlines()
            for i in range(0,10):
                #for x in file:

                    import json
                    y = json.loads(x[i])
                    print y
                    name = QtGui.QTableWidgetItem(y["name"])
                    date = QtGui.QTableWidgetItem(y["date"])
                    size = QtGui.QTableWidgetItem(str(y["size"]))
                    self.tableWidget.setItem(i, 0, name)
                    self.tableWidget.setItem(i, 1, size)
                    self.tableWidget.setItem(i, 2, date)


        '''
        #self.connect(self.btn1, QtCore.SIGNAL("clicked()"), self.new_dl)
        self.tabelka = QtGui.QTextEdit(self)
        self.tabelka.setGeometry(QtCore.QRect(200, 100, 400, 400))
        self.tabelka.setObjectName("tabelka")
        self.tabelka.setText("Tutaj beda \nsie znajdowaly \ndane wszystkich \npobranych plikow")
        '''



def main(self):
    global app
    app = App(self)
    app.exec_()


if __name__ == '__main__':
    #mp.freeze_support()
    main(sys.argv)