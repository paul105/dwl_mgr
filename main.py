import urllib2
import shutil
import multiprocessing as mp
import os
import time
import sys
import PyQt4
import test2

def main(self):
    global app
    app = test2.App(self)
    app.exec_()
    #cos



def dziecko(i, req, dir):               #funkcja dziecko, przekazujemy "id", "Request object", oraz katalog roboczy
    data = urllib2.urlopen(req)
    CHUNK = 1024*512                #ilosc danych czytana jednorazowo
    f_path = dir+"\\file"+str(i)
    with open(f_path,"wb") as output:
        while True:
            __time_start = time.time()
            chunk = data.read(CHUNK)    #odczytujemy pobrana jednostke danych i zapisujemy, jak wszystko odczytane ->break
            __time = time.time()-__time_start
            #print i, " czas: ", __time, " rozm: ", len(chunk)
            if not chunk: break
            output.write(chunk)
            CHUNK = int((CHUNK*0.3)+(len(chunk)/__time)*0.7)


def del_and_combine(dir,dir_tmp,f_name,N):
    with open(dir + "\\" + f_name, "wb") as of:
        for i in range(0, N):
            f_path = dir_tmp + "\\file" + str(i)
            with open(f_path, "rb") as f:
                shutil.copyfileobj(f, of, 1024 * 1024 * 10)
            os.remove(f_path)
        os.rmdir(dir_tmp)


if __name__ == '__main__':
    mp.freeze_support()
    main(sys.argv)


