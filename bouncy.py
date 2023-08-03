###############################
#Imports 
###############################
from keyboard import on_press
from time import time
from random import randint
from math import sin, cos, floor
from time import sleep
from win32api import SetCursorPos,GetCursorPos,EnumDisplayMonitors

###############################
#Keyboard Listener
###############################
def onkeypress(event):
    global stop
    global fullstop
    global vecoffset
    global gravitybool
    global energyconst
    
    
    if event.name == 'f12':
        fullstop=True
    elif event.name == 'f11':
        gravitybool=True
        energyconst=0.95
    elif event.name == 'f10':
        gravitybool=False
        energyconst=1
    elif event.name == 'up':
        vecoffset=[0,-arrowkeymag]
    elif event.name == 'down':
        vecoffset=[0,arrowkeymag]
    elif event.name == 'left':
        vecoffset=[-arrowkeymag,0]
    elif event.name == 'right':
        vecoffset=[arrowkeymag,0]
    elif event.name != '':
        stop = True

on_press(onkeypress)

###############################
#Class Definition 
###############################
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
            self.botright=[rect[2],rect[3]]
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
            elif(self.topleft[1]==other.topleft[1]):#Side to side
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


###############################
#Function Definition 
###############################
def createrectangles():
    rect_initial=[]
    rect=[]
    screenlist=[]
    result=0

    screenlist=EnumDisplayMonitors()

    for item in screenlist:
        rect_initial.append(Rect(item[2]))

    #If Length is 1 don't try to combine
    if (len(rect_initial) == 1 ):
        rect=rect_initial
        return rect
    
    # Combine Rectangles if possible
    while(rect_initial):
        result=0
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

def giverandvec(mag):
    ang = randint(0, 360)
    vec = [mag*sin(ang), mag*cos(ang)]
    return vec
    

def bouncethemouse():
    ###############################
    #Variables 
    ###############################
    global vecoffset

    FailSafe = True
    nextPos=[0,0]
    oldPos=[0,0]
    offMap=False
    rectangle=Rect([]) 
    
    ###############################
    #Generate Initial Direction
    ###############################
    refTime=time()
    vec=giverandvec(mag)
    refPos = GetCursorPos()
    nextPos = list(refPos)
    oldPos = list(refPos)



    ###############################
    #Cursor Loop
    ###############################
    while FailSafe:
        #Stop Program at F12
        if( fullstop== True):
                exit()
        
        curtime=time()           
        refPos = GetCursorPos()
        
        #Exit Due to Keyboard or Mouse Movement
        if ((refPos[0] != floor(nextPos[0])) | stop)  :
            FailSafe = False
            #print("Exit from failsafe")
            
        if curtime >= refTime:
            refTime = curtime + offset
            for item in rect:
                if(item.pointinrectangle(refPos)):
                    rectangle=item
                    break
            
            vec=[vec[0]+vecoffset[0],vec[1]+vecoffset[1]]
            vecoffset=[0,0]       
                   
            if(gravitybool):
                vec[1]+=gravity
                
            #Calculate Next
            nextPos = tuple(map(sum, zip(vec, oldPos)))
                
            #Check that Next Value is in a valid Spot
            for item in rect:
                if(item.pointinrectangle(nextPos)):
                    offMap=False
                    break

            #If it is going off map reflect
            if(offMap):
                if (floor(nextPos[0])<=rectangle.xint[0] or floor(nextPos[0])>=rectangle.xint[1] ):
                    #print("inverting x")
                    vec[0] = -vec[0] * energyconst
                if (floor(nextPos[1])<=rectangle.yint[0] or floor(nextPos[1])>=rectangle.yint[1] ):
                    #print("inverting y")
                    vec[1] = -vec[1] * energyconst
                nextPos = tuple(map(sum, zip(vec, oldPos)))
                
            SetCursorPos((floor(nextPos[0]), floor(nextPos[1])))
                    

            offMap=True
            oldPos=nextPos   

           
###############################
#Global Variables
###############################
vecoffset=(0,0)
stop = False
fullstop = False    

###############################
# Config Variables 
###############################
gravitybool=True
arrowkeymag=10
timeout=1
refresh = 60
speed=300
gravity=0.05
energyloss=0.95



offset = 1/refresh
mag=speed/refresh
energyconst=energyloss
if(not gravity):
    mag*=2
    arrowkeymag/=5
    energyconst= 1

###############################
#Main Code Loop
###############################
rect=createrectangles()

while True:
    refPos = GetCursorPos()
    sleep(timeout)
    if(list(refPos) == list(GetCursorPos())):
        stop=False
        bouncethemouse()