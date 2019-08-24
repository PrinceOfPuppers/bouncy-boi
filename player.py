import pygame as pg
import numpy as np
from cmath import phase
from math import pi,floor
from helperFuncts import convertCoords, rotateVecs
class DynamicObj:
    def __init__(self,config,startPos,startVel,startMass):
        #all vectors are rendered as complex numbers
        self.pos=startPos
        self.vel=startVel

        self.hasGrav=True
        self.config=config
        self.mass=startMass
        #spf is seconds per frame
        self.spf=round(1/config.fps,config.round)
    
    def applyForce(self,forceVec):
        self.vel+=forceVec*self.spf/self.mass

    def applyTickMotion(self):
        if self.hasGrav:
            self.vel+=self.spf*self.config.grav
        
        self.pos+=self.vel*self.spf


class Player(DynamicObj):
    def __init__(self,config,teather,booster,startPos,startVel=0+0j,startMass=1,startColor=(255,255,255)):
        super().__init__(config,startPos,startVel,startMass)
        self.rotMatrix=np.zeros((2,2),dtype=float)

        self.asset=config.playerAsset
        self.displayPoints=np.copy(config.playerAsset)
        self.displayPointsLen=len(self.displayPoints)

        self.teather=teather
        self.booster=booster
        self.color=startColor
        self.alive=True

    def draw(self,display,screenSize,screenPos):
        #draws player
        rotateVecs(self.asset,self.displayPoints,round(phase(self.vel),5)+pi/2,self.rotMatrix)
        plrPos=convertCoords(self.pos,screenPos)
        for i in range(0,self.displayPointsLen):
            self.displayPoints[i][0]+=plrPos[0]
            self.displayPoints[i][1]+=plrPos[1]
        pg.draw.aalines(display,self.color,True,self.displayPoints)

        #draws teather
        if self.teather.active:
            self.teather.draw(display,self.pos,screenPos)
            
        
        #draws boost bar
        self.booster.drawBoostBar(display,screenSize)

    def handler(self,display,screenSize,screenPos):
        self.applyTickMotion()
        if self.alive:
            self.draw(display,screenSize,screenPos)
        if self.teather.active:
            if self.teather.len/abs(self.teather.pivot.pos-self.pos)<1:
                displacement=(1-self.teather.len/abs(self.teather.pivot.pos-self.pos))*(self.teather.pivot.pos-self.pos)
                self.applyForce(self.teather.springConst*(displacement))

        #recharges boost
        if self.booster.boostAmmount<self.booster.boostMax:
            self.booster.boostAmmount+=self.booster.boostRechargeRate


        #checks if player is dead

        #they must be below the screen
        if convertCoords(self.pos,screenPos)[1]>screenSize[1]:
            #teather must not be active
            if not self.teather.active:
                self.alive=False
            #or the teather pivot must also be below the screen
            elif convertCoords(self.teather.pivot.pos,screenPos)[1]>screenSize[1]:
                self.alive=False



class Booster:
    def __init__(self,config):
        self.boostMax=config.boostMax
        self.boostAmmount=self.boostMax
        self.boostRechargeRate=config.boostRechargeRate
        self.boostForce=config.boostForce

        self.boostBarDimensions=(8*config.screenSize[0]/10,config.screenSize[1]/50)
        self.boostBar=pg.Rect(((config.screenSize[0]/10,config.screenSize[1]*(9/10),self.boostBarDimensions[0],self.boostBarDimensions[1])))

        self.animation=config.boosterAnimation
        self.animationRelPlayer=np.copy(config.boosterAnimation)
        self.numFrames=len(self.animation)
  
    
    def boost(self,display,player,screenPos,tickNumber):
        if self.boostAmmount>1+self.boostRechargeRate:
            #draws booster animation
            frameNum=tickNumber%self.numFrames
            rotateVecs(self.animation[frameNum],self.animationRelPlayer[frameNum],round(phase(player.vel),5)+pi/2,player.rotMatrix)
            plrPos=convertCoords(player.pos,screenPos)
            for i in range(0,len(self.animation[frameNum])):
                self.animationRelPlayer[frameNum][i][0]+=plrPos[0]
                self.animationRelPlayer[frameNum][i][1]+=plrPos[1]
            pg.draw.aalines(display,(255,0,0),True,self.animationRelPlayer[frameNum])

            self.boostAmmount-=2
            player.applyForce(self.boostForce*player.vel/abs(player.vel))
    
    def drawBoostBar(self,display,screenSize):
        self.boostBar.width=self.boostBarDimensions[0]*self.boostAmmount/self.boostMax
        pg.draw.rect(display,(255,0,0),self.boostBar,1)



class Teather:
    def __init__(self,config):
        self.active=False
        self.pivot='dummyData'
        self.len=0
        self.springConst=config.teatherSpringConst
        self.maxStrech=config.teatherMaxStrech
    
    def activate(self,plrPos,pivotMnger,clickPos):
        pivot=pivotMnger.teatherNearestPivot(clickPos)

        self.active=True
        self.pivot=pivot
        pivot.teathered=True
        self.len=abs(plrPos-pivot.pos)
    
    def deactivate(self):
        if self.active:
            self.active=False
            self.pivot.teathered=False
    
    def draw(self,display,pos,screenPos):
        #gets color and checks if teather is broken
        strechColor=int(255*(1-self.checkStrain(pos)))

        if self.active:
            pg.draw.aaline(display,(255,strechColor,strechColor),convertCoords(pos,screenPos),convertCoords(self.pivot.pos,screenPos))

    def checkStrain(self,plrPos):
        #checked in self.draw to return the color, also deactivates the teather if strain is too high
        strech=abs(self.pivot.pos-plrPos)-self.len
        strechRatio=strech/self.maxStrech
        if strechRatio<0:
            strechRatio=0
        if strechRatio>1:
            self.deactivate()
        
        return(strechRatio)