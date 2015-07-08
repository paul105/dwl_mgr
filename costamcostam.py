__author__ = 'p'
import urllib2 as u
import re

url = "http://127.0.0.1/gf.exe"
data = u.urlopen(url)
#print data.headers
if data.headers["Accept-Ranges"] == "bytes":
    if data.headers["Content-Length"]:
        print "cos"



'''
def funkcja():
    url = "htp://127.0.0.1/gf.exe"
    k = 1
    try:
        u.urlopen(url)
        return url
    except:
        try:
            url2 = "http://" + url
            u.urlopen(url2)
            url = url2
            return url
        except:
            try:
                url3 = "http://" + (url.split("//",1))[1]
                u.urlopen(url3)
                print "2"
                return url3
            except:
                try:
                    url4 = "ftp://" + url
                    u.urlopen(url4)
                    return url4
                except:
                    k = 0

    finally:
        pass
        #return k

#a = funkcja()
#print a

a=""
print isinstance(a,int)
'''
'''
if funkcja():
    print "cos"
else:
    print "nic"

#print funkcja()
czas = []
for i in range(5):
    url = "htp://127.0.0.1/gf.exe"
    import time
    start = time.time()
    try:
        u.urlopen(url)
    except:
        try:
            #url2 = "http://" + url
            url2 = "http://" + (url.split("//",1))[1]
            u.urlopen(url2)
            print "1"
        except:
            try:
                url3 = "http://" + url
                #url3 = "http://" + (url.split("//",1))[1]
                u.urlopen(url3)
                print "2"
            except:
                print "3"
                pass
    finally:
        czas.append(time.time()-start)
suma = 0
for x in czas:
    print x
    suma = suma + x
print "srednia = ", suma/len(czas)


try:
    ur = "cos.cos"
    a = (ur.split("//",1))
    #print a[1]
except:
    print "nic"
'''