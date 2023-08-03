import sys
from PyQt5 import QtWidgets


class Rect(object):
    def __init__(self,rect):
        if( not rect ):
            self.topleft=[]
            self.botright=[]
            self.xint=[]
            self.yint=[]
            self.height=0
            self.width=0
    
        else:
            self.topleft=[rect[0],rect[1]]
            self.botright=[rect[0]+rect[2],rect[1]+rect[3]]
            self.xint=[self.topleft[0],self.botright[0]]
            self.yint=[self.topleft[1],self.botright[1]]
            self.height=self.botright[1]-self.topleft[1]
            self.width=self.botright[0]-self.topleft[0]
    
    def __str__(self):
        return "Rect(%s,%s)\nXint(%s)\nYint(%s)\n"%(self.topleft, self.botright,self.xint,self.yint)
    
    def trycombinerectangles(self,other):#edit passed in rectangle
        #Be careful about combining rectangles as it gets messy as you cannot assume orientation
        
        if((self.height==other.height) and (self.width==other.width)):
            if(self.topleft[0] == other.topleft[0] and self.botright[0] == other.botright[0]):#On top of on another
                
                if(self.topleft[1] > other.topleft[1] ):
                    top=self
                    bottom=other
                else:
                    top=other
                    bottom=self
                
                other.topleft=top.topleft
                other.botright=bottom.botright
                other.xint=[other.topleft[0],other.botright[0]]
                other.yint=[other.topleft[1],other.botright[1]]
                other.height=other.botright[1]-other.topleft[1]
                other.width=other.botright[0]-other.topleft[0]
                return 1
            elif(self.botright[0] == other.topleft[0] or self.topleft[0] == other.botright[0]):#Side to side
                if(self.botright[0]<other.botright[0]):
                    top=self
                    bottom=other
                else:
                    top=other
                    bottom=self

                other.topleft=top.topleft
                other.botright=bottom.botright
                other.xint=[other.topleft[0],other.botright[0]]
                other.yint=[other.topleft[1],other.botright[1]]
                other.height=other.botright[1]-other.topleft[1]
                other.width=other.botright[0]-other.topleft[0]
                
                return 1
                
        return 0
    
    def pointinrectangle(self,point):
        if( self.xint[0] <= point[0] <= self.xint[1] and self.yint[0] <= point[1] <= self.yint[1] ):
            return True
        return False

    

def createrectangles():
    app = QtWidgets.QApplication(sys.argv)
    d = app.desktop()
    rect_initial=[]
    rect=[]
    screenlist=[]
    result=0

    for item in range(0,d.screenCount()):
        screenlist.append(list(d.screenGeometry(item).getRect()))
    
    for item in screenlist:
        rect_initial.append(Rect(item))

    #If Length is 1 don't try to combine
    if (len(rect) == 1 ):
        rect=rect_initial
        return rect
    
    # Combine Rectangles if possible
    while(rect_initial):
        cur_rect=rect_initial.pop(0)
        if (len(rect_initial) == 0 ):
            rect.append(cur_rect)
            return rect
        
        for x in range(0,len(rect_initial)):
            result+=cur_rect.trycombinerectangles(rect_initial[x])
            if(result):
                break

        if(result):
            continue
        else:
            rect.append(cur_rect)
   
    return rect