import os
from PyQt4 import QtCore, QtGui
import urllib2
import multiprocessing as mp
from main import dziecko, del_and_combine

def download1(url, file_size1, file_size2, data_block, N1, N2, dir_tmp):
    #headers = {
    #    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0",
    #    "Accept-Encoding": "gzip, deflate, sdch",
    #    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    #    "Accept-Language": "pl-PL,pl;q=0.8,en-US;q=0.6,en;q=0.4",
    #    "Connection": "keep-alive",
    #}

    N = N2-N1
    p = mp.Pool(N)
    if N1 !=0:
        for i in range(N1,N2):
            start = (i-N1)*data_block + file_size1
            stop = 0
            if not i == N2-1:
                stop = (i-N1)*data_block + data_block -1 + file_size1
                req = urllib2.Request(url, headers={"Range":"bytes=" + str(start) + "-" + str(stop)})
                #req.add_header("Range","bytes=" + str(start) + "-" + str(stop))
                print "1: %s - %s" % (start, stop)
                p.apply_async(dziecko, [i, req, dir_tmp])
                #del req.headers["Range"]
            else:
                stop = file_size2+file_size1
                #req = urllib2.Request(url, headers=headers)
                #req.add_header("Range","bytes=" + str(start) + "-" + str(stop))
                req = urllib2.Request(url, headers={"Range":"bytes=" + str(start) + "-" + str(stop)})
                print "2: %s - %s" % (start, stop)
                p.apply_async(dziecko, [i, req, dir_tmp])
                #del req.headers["Range"]
            print "i = %s, %s - %s, %s" % ( i, start, stop, N)

    elif N1 == 0:
        for i in range(N1, N2):
            # algorytm podzialu dla sciagania. W przypadku ostatniego watku musimy dopelnic zakres pobierania do wielkosci pliku
            start = i * data_block
            stop = 0
            if not i == N2 - 1:
                stop = i * data_block + data_block - 1
                print "3: %s - %s" % (start, stop)
                #req = urllib2.Request(url, headers=headers)
                #req.add_header("Range","bytes=" + str(start) + "-" + str(stop))
                req = urllib2.Request(url, headers={"Range":"bytes=" + str(start) + "-" + str(stop)})
                p.apply_async(dziecko, [i, req, dir_tmp])
                #del req.headers["Range"]
            else:
                stop = file_size1
                print "4: %s - %s" % (start, stop)
                req = urllib2.Request(url, headers={"Range":"bytes=" + str(start) + "-" + str(stop)})
                #req = urllib2.Request(url, headers=headers)
                #req.add_header("Range","bytes=" + str(start) + "-" + str(stop))
                p.apply_async(dziecko, [i, req, dir_tmp])
                #del req.headers["Range"]
            print "i = %s, %s - %s, %s" % ( i, start, stop, N)

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

    p.apply_async(dziecko, [0,req,dir_tmp,0])
    return p

def supervisor2(*args):
    N = args[0]
    url1 = args[1]
    url2 = args[2]
    val = (args[3] * 0.01)
    dir = args[4]
    ww = args[5]
    data_block = 0
    data_block1 = 0
    data_block2 = 0
    checkInt = 0
    f_name = url1.split("/")[len(url1.split("/")) - 1]
    dir_tmp = dir + "\\TMP." + f_name
    try:
        os.mkdir(dir_tmp)
    except:
        pass

    data1 = urllib2.urlopen(url1)
    data2 = urllib2.urlopen(url1)
    if data1.headers["Accept-Ranges"] == "bytes" and data2.headers["Accept-Ranges"] == "bytes":
        if data1.headers["Content-Length"] and data2.headers["Content-Length"] and data1.headers["Content-Length"] == data2.headers["Content-Length"]:
            for n in range(0, N):
                with open(dir_tmp + "\\file" + str(n), "w+b") as f:
                    pass
            file_size = round(float((data1.headers["Content-Length"].strip())))  # odnajdujemy w naglowku linijke "Content-Length", a nastepnie zapisujemy informacje o wielkosci pliku
            file_size1 = file_size*val
            file_size2 = file_size-file_size1
            check = N*val
            checkInt = int(round(check))

            if checkInt == 0:
                data_block1 = data_block2 = data_block = file_size/N
                p = download1(url2, int(file_size), 0, int(data_block), 0, N, dir_tmp)
            elif checkInt == N:
                data_block1 = data_block2 = data_block = file_size/N
                p = download1(url1, int(file_size), 0, int(data_block), 0, N, dir_tmp)
            elif checkInt < check or checkInt > check or checkInt == check:
                data_block1 = file_size1/checkInt
                data_block2 = file_size2/(N-checkInt)
                p1 = download1(url1, int(file_size1)-1, 0, int(data_block1), 0, checkInt, dir_tmp)
                p2 = download1(url2, int(file_size1), int(file_size2), int(data_block2), checkInt, N, dir_tmp)

        else:
            with open(dir_tmp + "\\file0", "w+b") as f:
                pass
            N = 1
            data_block1 = data_block2 = data_block
            checkInt=0
            p = download2(url1, dir_tmp)

    else:
        with open(dir_tmp + "\\file0", "w+b") as f:
            pass
        N = 1
        data_block1 = data_block2 = data_block
        checkInt=0
        p = download2(url1, dir_tmp)

    while True:
        QtCore.QCoreApplication.processEvents()
        sum = 0
        for n in range(0, N):
            sum = sum + os.path.getsize(dir_tmp + "\\file" + str(n))
            #print "suma = %.2f, file_size = %.2f" % (sum, file_size)
        if not sum < file_size:
            try:
                p.close()
                p.join()
            except:
                try:
                    p1.close()
                    p2.close()
                    p1.join()
                    p2.join()
                except:
                    pass

            ww.end.setEnabled(True)
            for n in range(0,checkInt):
                s = float(os.path.getsize(dir_tmp + "\\file" + str(n)))
                item = QtGui.QTableWidgetItem("%.2f/%.2f (100.00%%)" % (data_block1/(1024**2), data_block1/(1024**2)))
                item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
                ww.tableWidget.setItem(n,0,item)
            for n in range(checkInt,N):
                s = float(os.path.getsize(dir_tmp + "\\file" + str(n)))
                item = QtGui.QTableWidgetItem("%.2f/%.2f (100.00%%)" % (data_block2/(1024**2), data_block2/(1024**2)))
                item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
                ww.tableWidget.setItem(n,0,item)
            print "N = %s" % (N)
            del_and_combine(dir, dir_tmp, f_name, N)
            break

        for n in range(0,checkInt):
            s = float(os.path.getsize(dir_tmp + "\\file" + str(n)))
            item = QtGui.QTableWidgetItem("%.2f/%.2f (%2.2f%%)" % (s/(1024**2), float(data_block1/(1024**2)), ((s*100)/data_block1)))
            item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
            ww.tableWidget.setItem(n,0,item)

        for n in range(checkInt,N):
            s = float(os.path.getsize(dir_tmp + "\\file" + str(n)))
            item = QtGui.QTableWidgetItem("%.2f/%.2f (%2.2f%%)" % (s/(1024**2), float(data_block2/(1024**2)), ((s*100)/data_block2)))
            item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
            ww.tableWidget.setItem(n,0,item)


