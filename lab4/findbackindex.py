import os
import os
files= os.listdir('C:/Users/16400/Desktop/lab4/html')
for filename in files:
    f = open("C:/Users/16400/Desktop/lab4/html/"+filename, encoding='utf8')
    g = open("index.txt",'a')
    url = f.readline().strip()
    g.write(url+' '+filename+'\n')
    g.close()