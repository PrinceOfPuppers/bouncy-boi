import pygame as pg
from helperFuncts import convertCoords
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
        self.teather=teather
        self.booster=booster
        self.color=startColor
        self.alive=True

    def draw(self,display,screenSize,screenPos):
        pg.draw.circle(display,self.color,convertCoords(self.pos,screenPos),10,2)
        #draws teather
        if self.teather.active:
            self.teather.draw(display,self.pos,screenPos)
            
        
        #draws boost bar
        self.booster.draw(display,screenSize)

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

        #teather must not be active
        if not self.teather.active:
            #they must be below the screen
            if convertCoords(self.pos,screenPos)[1]>screenSize[1]:
                self.alive=False



class Booster:
    def __init__(self,screenSize):
        self.boostMax=50
        self.boostAmmount=self.boostMax
        self.boostRechargeRate=1
        self.boostForce=500

        self.boostBarDimensions=(8*screenSize[0]/10,screenSize[1]/50)
        self.boostBar=pg.Rect(((screenSize[0]/10,screenSize[1]*(9/10),self.boostBarDimensions[0],self.boostBarDimensions[1])))
  
    
    def boost(self,player):
        if self.boostAmmount>1:
            self.boostAmmount-=2
            player.applyForce(self.boostForce*player.vel/abs(player.vel))
    
    def draw(self,display,screenSize):
        self.boostBar.width=self.boostBarDimensions[0]*self.boostAmmount/self.boostMax
        pg.draw.rect(display,(255,0,0),self.boostBar,2)



class Teather:
    def __init__(self):
        self.active=False
        self.pivot='dummyData'
        self.len=0
        self.springConst=100
        self.damping=10
        self.maxStrech=100
    
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