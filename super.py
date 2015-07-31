import os
from PyQt4 import QtCore, QtGui
import urllib2
import multiprocessing as mp
from main import dziecko, del_and_combine, fileLogSave
from test2 import setTableParts, setTableDwn

def download1(url, file_size, data_block, N, dir_tmp):
    p = mp.Pool(N)
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
        p.apply_async(dziecko, [i, req, dir_tmp])
    return p


def download2(url,dir_tmp):
    N=1
    p = mp.Pool(N)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "pl-PL,pl;q=0.8,en-US;q=0.6,en;q=0.4",
        "Connection": "keep-alive",
    }
    req = urllib2.Request(url,headers=headers)
    p.apply_async(dziecko, [0,req,dir_tmp])
    return p


def supervisor1(*args):
    N = args[0]
    url = args[1]
    dir = args[2]
    ww = args[3]
    tableDwn = args[4]

    f_name = url.split("/")[len(url.split("/")) - 1]
    dir_tmp = dir + "\\TMP." + f_name
    try:
        os.mkdir(dir_tmp)
    except:
        pass

    data = urllib2.urlopen(url)
    if data.headers["Accept-Ranges"] == "bytes":
        if data.headers["Content-Length"]:
            for n in range(0, N):
                with open(dir_tmp + "\\file" + str(n), "w+b") as f:
                    pass
            setTableParts(ww.tableParts, N)

            file_size = round(float((data.headers["Content-Length"].strip())))  # odnajdujemy w naglowku linijke "Content-Length", a nastepnie zapisujemy informacje o wielkosci pliku
            data_block = float(file_size / N)
            p = download1(url, int(file_size), int(data_block), N, dir_tmp)
        else:
            N=1
            for n in range(0, N):
                with open(dir_tmp + "\\file" + str(n), "w+b") as f:
                    pass
            setTableParts(ww.tableParts, N)
            p = download2(url, dir_tmp)

    else:
        N=1
        for n in range(0, N):
            with open(dir_tmp + "\\file" + str(n), "w+b") as f:
                pass
        setTableParts(ww.tableParts, N)
        p = download2(url, dir_tmp)

    while True:
        QtCore.QCoreApplication.processEvents()
        sum = 0
        for n in range(0, N):
            sum = sum + os.path.getsize(dir_tmp + "\\file" + str(n))
        if not sum < file_size:
            p.close()
            p.join()

            ww.end.setEnabled(True)
            for n in range(0,N):
                s = float(os.path.getsize(dir_tmp + "\\file" + str(n)))
                item = QtGui.QTableWidgetItem("%.2f/%.2f (100.00%%)" % (data_block/(1024**2), data_block/(1024**2)))
                item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
                ww.tableParts.setItem(n,0,item)
            del_and_combine(dir, dir_tmp, f_name, N)
            fileLogSave(f_name, url)
            setTableDwn(tableDwn)
            break

        for n in range(0,N):
            s = float(os.path.getsize(dir_tmp + "\\file" + str(n)))
            item = QtGui.QTableWidgetItem("%.2f/%.2f (%2.2f%%)" % (s/(1024**2), float(data_block/(1024**2)), ((s*100)/data_block)))
            item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
            ww.tableParts.setItem(n,0,item)
