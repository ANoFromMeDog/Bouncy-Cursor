import mouse
import sys

from PyQt5 import QtWidgets


def getlines(lines):
    app = QtWidgets.QApplication(sys.argv)
    d = app.desktop()
    rect=[]
    coord=[]

    for item in range(0,d.screenCount()):
        rect.append(list(d.screenGeometry(item).getRect()))

    for item in rect:
        coord.append([item[0]          ,item[1]           ])
        coord.append([item[0]+ item[2] ,item[1]           ])
        coord.append([item[0]          ,item[1] + item[3] ])
        coord.append([item[0]+ item[2] ,item[1] + item[3] ])
    
        
    
    




lines=[]

getlines(lines)
print(lines)





#while True:
   # pos = mouse.get_position()
    #print(pos, end="")
    #print()
    #for x in range(50):
        #print("\b", end="")
