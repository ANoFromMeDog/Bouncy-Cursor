###############################
#Imports 
###############################
from keyboard import on_press
from mouse import get_position, move
from time import time
from random import randint
from math import sin, cos
from time import sleep


###############################
#Function Definition 
###############################
def onkeypress(event):
    global stop
    global fullstop
    
    if event.name == 'f12':
        fullstop=True
    elif event.name != '':
        stop = True
        

on_press(onkeypress)

def giverandvec(mag):
    vec=[0,0]
    ang = randint(0, 360)
    vec = [mag*sin(ang), mag*cos(ang)]
    return vec
    

def bouncethemouse(mag,offset,gravitybool):
    ###############################
    #Variables 
    ###############################   
    FailSafe = False
    xTimeout = 1
    yTimeout = 2
    count = 0

    nextPos=[0,0]
    oldPos=[0,0]
    res=[1920,1080]

    gravity=0.05
    energyloss=0.95
    buffer=5
    

    
    ###############################
    #Generate Initial Direction
    ###############################
    refTime=time()
    vec=giverandvec(mag)
    refPos = get_position()
    nextPos = list(refPos)
    oldPos = list(refPos)



    ###############################
    #Cursor Loop
    ###############################
    while not FailSafe:
        #Stop Program at F12
        if( fullstop== True):
                exit()
        
        curtime=time()           
        refPos = get_position()
        
        #Exit Due to Keyboard or Mouse Movement
        if ((refPos[0] != int(nextPos[0])) | stop)  :
            FailSafe = True
            print("Exit from failsafe")
            
        if curtime >= refTime:
            if(gravitybool):
                refTime = curtime + offset
                vec[1]+=gravity
                
                if (refPos[0] <= buffer) or (refPos[0] >= (res[0]-buffer)):
                    print("inverting x")
                    vec[0] = -vec[0] * energyloss
                if (refPos[1] <= buffer) or (refPos[1] >= (res[1]-buffer)):
                    print("inverting y")
                    vec[1] = -vec[1] * energyloss
                
                nextPos[0] = vec[0] + oldPos[0]
                nextPos[1] = vec[1] + oldPos[1]
                oldPos[0] = nextPos[0]
                oldPos[1] = nextPos[1]
                move(nextPos[0], nextPos[1])
                
                
            else:
                refTime = curtime + offset
                count += 1
                if (refPos[0] <= 5) or (refPos[0] >= (res[0]-5)) & ((count - xTimeout) >= 10):
                    xTimeout = count
                    print("inverting x")
                    vec[0] = -vec[0]
                if (refPos[1] <= 5) or (refPos[1] >= (res[1]-5)) & ((count - yTimeout) >= 10):
                    yTimeout = count
                    print("inverting y")
                    vec[1] = -vec[1]
                if (count == xTimeout) & (count == yTimeout):
                    print("LETS GOOOOOOOOOOOOOO")
                nextPos[0] = vec[0] + oldPos[0]
                nextPos[1] = vec[1] + oldPos[1]
                oldPos[0] = nextPos[0]
                oldPos[1] = nextPos[1]
                move(nextPos[0], nextPos[1])
                    
    


###############################
#Variables 
###############################

timeout=1
refresh = 60
speed=300
offset = 1/refresh
mag=speed/refresh
stop = False
fullstop = False

###############################
#Main Code Loop
###############################

while True:
    refPos = get_position()
    sleep(timeout)
    if(list(refPos) == list(get_position())):
        stop=False
        bouncethemouse(mag,offset,True)