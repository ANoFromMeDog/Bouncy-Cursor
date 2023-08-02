import mouse
import sys
import matplotlib.pyplot as plt

from PyQt5 import QtWidgets




def getlines():
    app = QtWidgets.QApplication(sys.argv)
    d = app.desktop()
    rect=[]
    coord=[]
    
    for item in range(0,d.screenCount()):
        rect.append(list(d.screenGeometry(item).getRect()))
    
    for item in rect:
        coord.append([item[0], item[1]])
        coord.append([item[2], item[1]])
        coord.append([item[0], item[3]])
        coord.append([item[2], item[3]])
    

    print(coord)
        

   
      




getlines()
#print(lines)
