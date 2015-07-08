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
        self.btn1 = QtGui.QPushButton("New", self.cw)
        self.btn1.setGeometry(QtCore.QRect(10, 10, 100, 60))
        self.connect(self.btn1, QtCore.SIGNAL("clicked()"), self.new_dl)
        self.tabelka = QtGui.QTextEdit(self)
        self.tabelka.setGeometry(QtCore.QRect(200, 100, 400, 400))
        self.tabelka.setObjectName("tabelka")
        self.tabelka.setText("Tutaj beda \nsie znajdowaly \ndane wszystkich \npobranych plikow")

    def new_dl(self):
        self.w = Ui_new_dl()
        self.w.setGeometry(QtCore.QRect(100, 100, 600, 400))
        self.w.show()
        return self.w

###okno do wprowadzenia danych
class Ui_new_dl(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        #self.filename = ""
        self.dir = ""
        #self.n = 0
        #self.__url = ""
        self.cw2 = QtGui.QWidget(self)
        self.setWindowTitle("Nowe Pobieranie")
        self.setCentralWidget(self.cw2)
        self.url = QtGui.QTextEdit(self)
        self.url.setGeometry(QtCore.QRect(150,100,400,35))
        self.url.setObjectName("urlik")
        self.parts = QtGui.QTextEdit(self)
        self.parts.setGeometry(QtCore.QRect(40,100,40,35))
        self.__search = QtGui.QPushButton("Przegladaj", self.cw2)
        self.__search.setGeometry(QtCore.QRect(10,10,100,30))
        self.connect(self.__search, QtCore.SIGNAL("clicked()"), self.get_dir)
        self.dodaj = QtGui.QPushButton("Dodaj", self.cw2)
        self.dodaj.setGeometry(QtCore.QRect(400,300,150,70))
        self.connect(self.dodaj, QtCore.SIGNAL("clicked()"), self.pobieranie)

    def get_url(self):
        url = str(self.url.toPlainText())
        return url

    def get_parts(self):
        try:
            parts = int(self.parts.toPlainText())
        except:
            parts = ""
            #todo alert o braku czesci
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
        #print url
        k = 1
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
                        #todo:
                        #alert o zlym adresie url
                        return ""

    def pobieranie(self):
        url = self.check_url(self.get_url())
        #print url
        n = self.get_parts()
        try:
            if self.dir=="":
                #todo alert o braku wyboru katalogu
                print "1"
                pass
            elif not isinstance(n,int):
                #todo alert nie wpisano n, lub n jest niepoprawne
                print "2"
                pass
            elif url!="":
                self.ww = UI_dl(n)
                self.ww.setGeometry(QtCore.QRect(500,500,400,300))
                self.ww.show()
                from super import supervi
                supervi(n, url, self.dir, self.ww)
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
        self.tabelka=[]
        for i in range(0,n):
            self.tabelka.append(QtGui.QTextEdit(self))
            self.tabelka[i].setGeometry(QtCore.QRect(50,(50+i*23),100,25))
            self.tabelka[i].setObjectName("tabelka"+str(i))




