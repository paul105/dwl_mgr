#!/usr/bin/env python
#-*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

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
        self.btn1 = QtGui.QPushButton("Nowy", self.cw)
        self.btn1.setGeometry(QtCore.QRect(10, 10, 100, 60))

        self.dele = QtGui.QPushButton("Usun", self.cw)
        self.dele.setGeometry(QtCore.QRect(10, 130, 100, 60))

        self.connect(self.btn1, QtCore.SIGNAL("clicked()"), self.new_dl)
        self.tableDwn = QtGui.QTableWidget(self.cw)
        self.tableDwn.setGeometry(QtCore.QRect(145, 130, 630, 400))
        self.tableDwn.horizontalHeader().setVisible(False)
        self.tableDwn.horizontalHeader().setStretchLastSection(True)
        self.tableDwn.setObjectName("tableDownloads")
        self.tableDwn.setColumnCount(3)
        self.tableDwn.setRowCount(0)
        setTableDwn(self.tableDwn)

        self.connect(self.dele, QtCore.SIGNAL("clicked()"), self.deleRow)

    def deleRow(self):
        a = self.tableDwn.currentRow()
        try:
            with open("files","rb") as f:
                x = f.readlines()
                del x[a]
                with open("files","wb") as ff:
                    [ff.write(x[i]) for i in range(0, len(x))]
            setTableDwn(self.tableDwn)
        except:
            pass

    def new_dl(self):
        self.w = Ui_new_dl(self.tableDwn)
        self.w.setGeometry(QtCore.QRect(100, 100, 600, 400))
        self.w.show()
        return self.w

###okno do wprowadzenia danych
class Ui_new_dl(QtGui.QMainWindow):
    def __init__(self,table):
        QtGui.QMainWindow.__init__(self)
        #self.filename = ""
        self.tableDwn = table
        self.dir = ""
        #self.n = 0
        #self.__url = ""
        self.cw2 = QtGui.QWidget(self)
        self.setWindowTitle("Nowe Pobieranie")
        self.setCentralWidget(self.cw2)

        self.url = QtGui.QLineEdit(self.cw2)
        self.url.setGeometry(QtCore.QRect(150,100,400,30))
        self.url.setObjectName("url_1")

        self.parts = QtGui.QLineEdit(self.cw2)
        self.parts.setGeometry(QtCore.QRect(40,100,40,30))
        self.parts.setObjectName("Parts")

        self.urlBox = QtGui.QCheckBox(self.cw2)
        self.urlBox.setGeometry(QtCore.QRect(50, 170, 70, 17))
        self.urlBox.setObjectName("urlBox")

        self.url2 = QtGui.QLineEdit(self.cw2)
        self.url2.setGeometry(QtCore.QRect(150,160,400,30))
        self.url2.setObjectName("url_2")
        self.url2.setDisabled(True)

        self.propSlider = QtGui.QSlider(self.cw2)
        self.propSlider.setGeometry(QtCore.QRect(150, 220, 400, 30))
        self.propSlider.setOrientation(QtCore.Qt.Horizontal)
        self.propSlider.setObjectName("Proportion slider")
        self.propSlider.setDisabled(True)
        self.propSlider.setValue(50)
        self.propSlider.setRange(0,100)

        self.propValue = QtGui.QLineEdit(self.cw2)
        self.propValue.setGeometry(QtCore.QRect(40,220,40,30))
        self.propValue.setObjectName("Proportion Value")
        self.propValue.setDisabled(True)
        self.propValue.setText(str(self.propSlider.value()))
        self.propValue.setMouseTracking(False)
        self.propValue.setMaxLength(3)


        self.__search = QtGui.QPushButton("Przegladaj", self.cw2)
        self.__search.setGeometry(QtCore.QRect(10,10,100,30))
        self.connect(self.__search, QtCore.SIGNAL("clicked()"), self.get_dir)
        self.dodaj = QtGui.QPushButton("Dodaj", self.cw2)
        self.dodaj.setGeometry(QtCore.QRect(400,300,150,70))
        self.connect(self.dodaj, QtCore.SIGNAL("clicked()"), self.download_decide)

        self.connect(self.urlBox, QtCore.SIGNAL("clicked()"), self.undis)
        self.connect(self.propSlider, QtCore.SIGNAL("valueChanged(int)"), self.slid_ch)
        self.connect(self.propValue, QtCore.SIGNAL("textEdited(QString)"), self.val_ch)


    def val_ch(self):
        x = self.propValue.text()
        try:
            x = int(x)
        except:
            x = ""
            self.propValue.clear()
        if x == "":
            self.propValue.setMaxLength(3)
        if len(str(x)) == 1:
            if x > 1 and x < 10 :
                self.propValue.setMaxLength(2)
            elif x == 0:
                self.propValue.setMaxLength(1)
            elif x == 1:
                self.propValue.setMaxLength(3)
            else:
                self.propValue.clear()
                self.propValue.setMaxLength(3)
        elif len(str(x)) == 2:
            if x == 10:
                self.propValue.setMaxLength(3)
            elif x > 9 and x < 100:
                self.propValue.setMaxLength(2)
            else:
                self.propValue.clear()
                self.propValue.setMaxLength(3)
        elif len(str(x)) == 3:
            if not x == 100:
                self.propValue.setText("100")
                x = 100
        if not x == "":
            self.propSlider.setValue(x)
        else:
            self.propSlider.setValue(0)


    def slid_ch(self):
        self.propValue.setText(str(self.propSlider.value()))

    def undis(self):
        if self.urlBox.isChecked():
            self.url2.setDisabled(False)
            self.propSlider.setDisabled(False)
            self.propValue.setDisabled(False)
        else:
            self.url2.setDisabled(True)
            self.propSlider.setDisabled(True)
            self.propValue.setDisabled(True)
        return None

    def get_url1(self):
        url = str(self.url.text())
        return url

    def get_url2(self):
        url = str(self.url2.text())
        return url

    def get_parts(self):
        try:
            parts = int(self.parts.text())
        except:
            #QtGui.QMessageBox.about(self,"Error!","Nie wybrano ilosci czesci lub liczba jest niepoprawna")
            parts = ""
        finally:
            return parts


    def get_dir(self):
        fd = QtGui.QFileDialog(self)
        self.dir = str(fd.getExistingDirectory(self))
        from os.path import isdir
        try:
            if not isdir(self.dir):
                self.dir=""
        finally:
            return self.dir

    def check_url(self,url):
        import urllib2
        try:
            urllib2.urlopen(url)
            return url
        except:
            try:
                url2 = "http://" + (url.split("//",1))[1]
                urllib2.urlopen(url2)
                return url2
            except:
                try:
                    url3 = "http://" + url
                    urllib2.urlopen(url3)
                    return url3
                except:
                    try:
                        url4 = "ftp://" + url
                        urllib2.urlopen(url4)
                        return url4
                    except:
                        QtGui.QMessageBox.about(self,"Error!","Nie wpisano adresu lub adres jest niepoprawny (serwer docelowy nie odpowiada)")
                        return ""

    def download_decide(self):
        if not self.urlBox.isChecked():
            self.download1()
        else:
            self.download2()

    def download1(self):
        url1 = self.check_url(self.get_url1())
        n = self.get_parts()
        try:
            if self.dir=="":
                QtGui.QMessageBox.about(self,"Error!","Nie wybrano katalogu lub katalog nie istnieje")
            elif not isinstance(n,int) or n <= 0:
                QtGui.QMessageBox.about(self,"Error!","Nie wybrano ilosci czesci lub liczba jest niepoprawna")
            elif url1!="":
                self.ww = UI_dl(n)
                self.ww.setGeometry(QtCore.QRect(500,500,400,300))
                self.ww.show()
                from super import supervisor1
                supervisor1(n, url1, self.dir, self.ww, self.tableDwn)
            else:
                pass
        except:
            pass


    def download2(self):
        url2 = self.check_url(self.get_url2())
        val = int(self.propSlider.value())
        url1 = self.check_url(self.get_url1())
        n = self.get_parts()
        try:
            if self.dir=="":
                QtGui.QMessageBox.about(self,"Error!","Nie wybrano katalogu lub katalog nie istnieje")
            elif not isinstance(n,int) or n <= 0 :
                QtGui.QMessageBox.about(self,"Error!","Nie wybrano ilosci czesci lub liczba jest niepoprawna")
            elif url1!="" and url2!="":
                self.ww = UI_dl(n)
                self.ww.setGeometry(QtCore.QRect(500,500,400,300))
                self.ww.show()
                from super2 import supervisor2
                supervisor2(n, url1, url2, val, self.dir, self.ww, self.tableDwn)

            else:
                pass
        except:
            pass

####okno pobierania
class UI_dl(QtGui.QMainWindow):
    def __init__(self,n):
        QtGui.QMainWindow.__init__(self)
        self.cw3 = QtGui.QWidget(self)
        self.setCentralWidget(self.cw3)
        self.setWindowTitle("Pobieranie pliku...")
        self.end = QtGui.QPushButton("Zakoncz", self.cw3)
        self.end.setGeometry(QtCore.QRect(250,250,100,30))
        self.end.setEnabled(False)
        self.connect(self.end, QtCore.SIGNAL("clicked()"), self.close)
        self.tableParts = QtGui.QTableWidget(self.cw3)
        self.tableParts.setGeometry(QtCore.QRect(10, 10, 300, 200))
        self.tableParts.horizontalHeader().setVisible(False)
        self.tableParts.horizontalHeader().setStretchLastSection(True)
        self.tableParts.setObjectName("tableParts")
        self.tableParts.setColumnCount(1)



def setTableParts(table,n):
    table.setRowCount(n)
    for i in range(0,n):
        item = QtGui.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
        table.setItem(i, 0, item)

def setTableDwn(table):
    try:
        with open("files","rb") as file:
            x = file.readlines()
            table.setRowCount(len(x))
            for i in range(0,10):

                import json
                y = json.loads(x[i])

                name = QtGui.QTableWidgetItem(y["name"])
                name.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
                date = QtGui.QTableWidgetItem(y["date"])
                date.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
                url = QtGui.QTableWidgetItem(str(y["url"]))
                url.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
                table.setItem(i, 0, name)
                table.setItem(i, 1, date)
                table.setItem(i, 2, url)
    except:
        pass

