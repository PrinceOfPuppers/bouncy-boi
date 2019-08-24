import pygame as pg
import numpy as np
from helperFuncts import convertCoords
from numpy.random import randint
from math import inf
class PivotManager:
    def __init__(self,config):
        #total number of pivots on the screen
        self.numPivots=config.numPivots
        self.randYOffsetCap=config.randPivotYOffsetCap
        self.activePivots=[]
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
                    pivot.pos=randint(0,screenSize[0])-(screenPos[1]+randint(0,self.randYOffsetCap))*1j

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
                pivot.draw(display,pivot.highlightedColor,screenPos)
            else:
                pivot.draw(display,pivot.color,screenPos)

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
    def __init__(self,config,startPos,startVel=0+0j,color=(255,0,0),highlightedColor=(255,255,255)):
        self.pos=startPos
        self.vel=startVel
        self.color=color
        self.highlightedColor=highlightedColor
        self.teathered=False

        self.assets=config.pivotAssets
        self.displayPoints1=np.copy(config.pivotAssets[0])
        self.displayPointsLen1=len(self.displayPoints1)

        self.displayPoints2=np.copy(config.pivotAssets[1])
        self.displayPointsLen2=len(self.displayPoints2)

    def draw(self,display,color,screenPos):
        pivPos=convertCoords(self.pos,screenPos)

        #displays body
        for i in range(0,self.displayPointsLen1):
            self.displayPoints1[i][0]=self.assets[0][i][0]+pivPos[0]
            self.displayPoints1[i][1]=self.assets[0][i][1]+pivPos[1]
        pg.draw.aalines(display,color,True,self.displayPoints1)

        #displays diamond
        for i in range(0,self.displayPointsLen2):
            self.displayPoints2[i][0]=self.assets[1][i][0]+pivPos[0]
            self.displayPoints2[i][1]=self.assets[1][i][1]+pivPos[1]
        pg.draw.aalines(display,color,True,self.displayPoints2)
