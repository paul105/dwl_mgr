import urllib2
import shutil
import multiprocessing as mp
import os
import time
import sys
import test2

def main(self):
    global app
    app = test2.App(self)
    app.exec_()


def dziecko(i, req, dir):               #funkcja dziecko, przekazujemy "id", "Request object", oraz katalog roboczy

    data = urllib2.urlopen(req)
    CHUNK = 1024*512                #ilosc danych czytana jednorazowo
    f_path = dir+"\\file"+str(i)
    print "dziecko numer i = %s,\nheaders = %s" % (i,req.headers)
    with open(f_path,"wb") as output:
        while True:
            __time_start = time.time()
            chunk = data.read(CHUNK)    #odczytujemy pobrana jednostke danych i zapisujemy, jak wszystko odczytane ->break
     #       print "tekst = %s" % chunk
            __time = time.time()-__time_start
            #print __time
            #print i, " czas: ", __time, " rozm: ", len(chunk)
            if not chunk: break
            output.write(chunk)
            CHUNK = int((CHUNK*0.3)+(len(chunk)/__time)*0.7)


def del_and_combine(dir,dir_tmp,f_name,N):
    with open(dir + "\\" + f_name, "wb") as of:
        for i in range(0, N):
            f_path = dir_tmp + "\\file" + str(i)
            with open(f_path, "rb") as f:
                #print "kopiuje plik %s do pliku %s" % (f_path, f_name)
                shutil.copyfileobj(f, of, 1024 * 1024)
            os.remove(f_path)
        os.rmdir(dir_tmp)


if __name__ == '__main__':
    mp.freeze_support()
    main(sys.argv)


