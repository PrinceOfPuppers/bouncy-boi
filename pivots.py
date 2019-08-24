import pygame as pg
from helperFuncts import convertCoords
from numpy.random import randint
from math import inf
class PivotManager:
    def __init__(self,config):
        #total number of pivots on the screen
        self.numPivots=5

        self.activePivots=[]
        self.pivotRadius=config.pivotRadius

        for i in range(0,self.numPivots):
            self.activePivots.append(Pivot(config,randint(0,config.screenSize[0])+randint(0,config.screenSize[1])*1j))
    
    def resetPivots(self,screenPos):
        for pivot in self.activePivots:
            posRelScreen=convertCoords(pivot.pos,screenPos)
            pivot.pos=posRelScreen[0]+posRelScreen[1]*1j
        
    def cyclePivots(self,screenPos,screenSize):
        #sets pivots to active if they are on the screen, sets them to inactive if they are not
        for pivot in self.activePivots:

            pivotScreenCoords=convertCoords(pivot.pos,screenPos)
            if not pivot.teathered:
                if pivotScreenCoords[1]>screenSize[1]+10:
                    pivot.pos=randint(0,screenSize[0])-(screenPos[1])*1j

                if pivotScreenCoords[0]>screenSize[0]:
                    pivot.pos-=screenSize[0]
                elif pivotScreenCoords[0]<0:
                    pivot.pos+=screenSize[0]

            

    def drawPivots(self,display,screenPos,mousePos):

        nearestPivotIndex=-1
        nerestPivotDist=inf
        oneTeathered=False
        #gets the pivot to the mouse or the current teathered pivot
        for i,pivot in enumerate(self.activePivots):
            if pivot.teathered:
                oneTeathered=True
                nearestPivotIndex=i
            elif not oneTeathered:
                pivotDist=abs(pivot.pos-mousePos)
                if pivotDist<nerestPivotDist:
                    nearestPivotIndex=i
                    nerestPivotDist=pivotDist
        
        for i,pivot in enumerate(self.activePivots):
            if i==nearestPivotIndex:
                pg.draw.circle(display,pivot.highlightedColor,convertCoords(pivot.pos,screenPos),self.pivotRadius,2)
            else:
                pg.draw.circle(display,pivot.color,convertCoords(pivot.pos,screenPos),self.pivotRadius,2)

    def handler(self,display,screenPos,screenSize,mousePos):
        self.cyclePivots(screenPos,screenSize)
        self.drawPivots(display,screenPos,mousePos)

    def teatherNearestPivot(self,clickPos):
        nearestPivotIndex=-1
        nerestPivotDist=inf
        for i,pivot in enumerate(self.activePivots):
            pivotDist=abs(pivot.pos-clickPos)
            if pivotDist<nerestPivotDist:
                nearestPivotIndex=i
                nerestPivotDist=pivotDist
        return(self.activePivots[nearestPivotIndex])

class Pivot:
    def __init__(self,config,startPos,startVel=0+0j,color=(255,0,0),highlightedColor=(0,255,0)):
        self.pos=startPos
        self.vel=startVel
        self.color=color
        self.highlightedColor=highlightedColor
        self.teathered=False
