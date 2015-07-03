#!/usr/bin/env python
#-*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore


class App(QtGui.QApplication):
    def __init__(self, *args):
        QtGui.QApplication.__init__(self, *args)
        self.main = MainWindow()
        self.main.setGeometry(QtCore.QRect(100,100,800,600))
        self.connect(self, QtCore.SIGNAL("lastWindowClosed()"), self.byebye )
        self.main.show()

    def byebye( self ):
        self.exit(0)

class UI_dl(QtGui.QMainWindow):
    def __init__(self,N):
        QtGui.QMainWindow.__init__(self)
        self.cw3 = QtGui.QWidget(self)
        self.setCentralWidget(self.cw3)
        self.setWindowTitle("Pobieranie pliku...")
        n = N
        self.end = QtGui.QPushButton("Zakoncz", self.cw3)
        self.end.setGeometry(QtCore.QRect(250,250,100,30))
        self.end.setEnabled(False)
        self.connect(self.end, QtCore.SIGNAL("clicked()"), self.close)
        self.tabelka=[]

        for i in range(0,n):
            self.tabelka.append(QtGui.QTextEdit(self))
            self.tabelka[i].setGeometry(QtCore.QRect(50,(50+i*23),100,25))
            self.tabelka[i].setObjectName("tabelka"+str(i))

class Ui_new_dl(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.filename = ""
        self.path = ""
        self.n = 0
        self.__url = ""
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
        self.connect(self.__search, QtCore.SIGNAL("clicked()"), self.__file)
        self.dodaj = QtGui.QPushButton("Dodaj", self.cw2)
        self.dodaj.setGeometry(QtCore.QRect(400,300,150,70))
        self.connect(self.dodaj, QtCore.SIGNAL("clicked()"), self.pobieranie)

    def get_url(self):
        Text = str(self.url.toPlainText())
        return Text

    def get_parts(self):
        parts = int(self.parts.toPlainText())
        return parts

    def __file(self):
        fd = QtGui.QFileDialog(self)
        self.filename = fd.getExistingDirectory(self)
        from os.path import isdir
        if isdir(self.filename):
            return str(self.filename)

    def pobieranie(self):
        self.__url = self.get_url()
        self.n = self.get_parts()
        #url = "http://pluton.kt.agh.edu.pl/~pnogiec/10M"
        path = str(self.filename)
        #path = "C:\Users\p\PycharmProjects\download_mgr"
        self.path = path
        #N=4
        #self.n = N
        self.ww = UI_dl(self.n)
        self.ww.setGeometry(QtCore.QRect(500,500,400,300))
        self.ww.show()
        from super import supervi
        supervi(self.n, self.__url,self.path, self.ww)

'''
    def supervi(self):
        import os
        import urllib2
        import multiprocessing as mp
        from main import dziecko, del_and_combine
        from super import cos
        cos(self)
        N = self.n
        url = self.__url
        dir = self.path
        f_name = url.split("/")[len(url.split("/")) - 1]
        dir_tmp=dir + "\\TMP." + f_name
        try:
            os.mkdir(dir_tmp)
        except:
            pass

        for n in range(0,N):
            with open(dir_tmp+"\\file"+str(n), "w+b") as f:
                pass

        data = urllib2.urlopen(url)
        # odnajdujemy w naglowku linijke "Content-Length", a nastepnie zapisujemy informacje o wielkosci pliku
        file_size = int(data.headers["Content-Length"].strip())
        data_block = file_size/N
        p=mp.Pool(N)
        for i in range(0, N):
            # algorytm podzialu dla sciagania. W przypadku ostatniego watku musimy dopelnic zakres pobierania do wielkosci pliku
            start = i * data_block
            stop = 0
            if not i == N - 1:
                stop = i * data_block + data_block - 1
            else:
                stop = file_size

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0",
                "Accept-Encoding": "gzip, deflate, sdch",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "pl-PL,pl;q=0.8,en-US;q=0.6,en;q=0.4",
                "Connection": "keep-alive",
                "Range": "bytes=" + str(start) + "-" + str(stop)
            }
            # ustalenie obiektu Request dla konkretnego procesu
            req = urllib2.Request(url, headers=headers)
            p.apply_async(dziecko,[i,req,dir_tmp])

        while True:
            QtCore.QCoreApplication.processEvents()
            sum=0
            for n in range(0,N):
                sum=sum+os.path.getsize(dir_tmp + "\\file" + str(n))
            s = float(os.path.getsize(dir_tmp + "\\file" + str(n)))
            if not sum < file_size:
                p.close()
                p.join()
                self.ww.end.setEnabled(True)
                for n in range(0,N):
                    pass
                    #self.ww.tabelka[n].setText(str(int(s/data_block *100))+"%")
                del_and_combine(dir,dir_tmp,f_name,N)
                break
            for n in range(0,N):
                pass
                #self.ww.tabelka[n].setText(str(int(s/data_block *100))+"%")
'''

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