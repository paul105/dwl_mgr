__author__ = 'p'
import json
import os
import time
p = "json_file"

print time.strftime("%c")
try:
    os.remove(p)
except:
    pass
a=[]
for i in range(0,10):
    b = json.dumps({"name":"plik"+str(i),"size":i,"url":"http://127.0.0.1/gf.exe", "date":time.strftime("%c")}, separators=(",",":"))
    a.append(b)
    with open(p,"ab+") as f:
        #for i in a:
        f.write(b+"\n")
a=[]
i=1
with open(p,"rb") as f:
        #for line in f.readlines():
            cont=f.readlines()
            print cont[0]
            '''
            line = line.strip()
            print i, json.loads(line)["name"]
            i+=1
            #pass
            '''





