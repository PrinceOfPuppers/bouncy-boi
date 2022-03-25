import pygame as pg
from config import Config
from random import random
import os
from player import Player,Booster,Teather
from pivots import PivotManager
from helperFuncts import convertCoords,convertCoordsInv
from menu import Button,TextBox

class Background:
    def __init__(self,config,screenPos):
        self.starRadius=config.starRadius
        self.starDensity=.2*(10)**(-4)
        self.starNumber=int(self.starDensity*(config.screenSize[0]*config.screenSize[1]))
        self.starColor=config.starColor
        self.starParalaxCoefficents = config.starParalaxCoefficents

        self.starsInitalPos=[]
        self.starsCurrentPos=[]
        for i in range(0,self.starNumber):
            star=random()*config.screenSize[0]+random()*config.screenSize[1]*1j
            self.starsInitalPos.append(star)
            self.starsCurrentPos.append(list(convertCoords(star,screenPos)))





    def handler(self,display,screenSize,screenPos):
        pg.Surface.fill(display,(0,0,0))
        for i in range(0,self.starNumber):
            currentPos=convertCoords(self.starsInitalPos[i],screenPos)
            self.starsCurrentPos[i][0]=currentPos[0]
            self.starsCurrentPos[i][1]=currentPos[1]

            self.starsCurrentPos[i][0]%=screenSize[0]
            self.starsCurrentPos[i][1]%=screenSize[1]

            for paralaxCoeff in self.starParalaxCoefficents:
                pg.draw.circle(display,self.starColor,(int(paralaxCoeff*self.starsCurrentPos[i][0]),int(paralaxCoeff*self.starsCurrentPos[i][1])),self.starRadius,1)





class GameManager: 

    def __init__(self,config):

        self.hasQuit=False
        self.tickNumber=0
        self.display=pg.display.set_mode((config.screenSize[0], config.screenSize[1]))
        self.pivotMnger=PivotManager(config)
        self.clock=pg.time.Clock()
        self.initalPlrVel=config.initalPlayerVel
        self.initalPlrPos=config.screenSize[0]/2+1j*config.screenSize[1]

        #screen height is height of top left corner from start (value will get more negative as player goes up)
        self.screenPosition=[0,0]

        self.plr=Player(config,Teather(config),Booster(config),self.initalPlrPos,self.initalPlrVel)
        self.bg=Background(config,self.screenPosition)

        self.config=config
        #used for reading and writing score
        self.fileName=os.path.basename(__file__)
        self.dirPath=os.path.realpath(__file__)[0:-len(self.fileName)]
        self.screenSize=config.screenSize
        self.screenVelSlope=config.screenVelSlope
        self.spf=1/config.fps
        
        self.scoreDivisor=config.scoreDivisor

        self.scoreDisplay=TextBox('PLACEHOLDER',(255,0,0),(self.screenSize[0]/15,self.screenSize[1]/20),round(config.fontSize/2))
        self.scoreDisplay.initalizeTextBox()

        self.resetButton=Button((self.screenSize[0]/2,2*self.screenSize[1]/3),self.screenSize[0]/8,self.screenSize[0]/8,config.resetSymbol,(255,0,0),(255,255,255),True)
        self.resetText=TextBox('PLACEHOLDER',(255,0,0),(self.screenSize[0]/2,self.screenSize[1]/3),config.fontSize)
        self.resetText.initalizeTextBox()

        self.startButton=Button((self.screenSize[0]/2,2*self.screenSize[1]/3),self.screenSize[0]/8,self.screenSize[0]/8,config.playSymbol,(255,0,0),(255,255,255),True)
        self.startText=TextBox('BOUNCY BOI',(255,0,0),(self.screenSize[0]/2,self.screenSize[1]/3),config.fontSize)
        self.startText.initalizeTextBox()

    def applyControls(self):
        for event in pg.event.get():
            # checks if user has quit
            if event.type == pg.QUIT:
                self.hasQuit=True
                
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button== pg.BUTTON_LEFT:
                    self.plr.teather.activate(self.plr.pos,self.pivotMnger,convertCoordsInv(event.pos,self.screenPosition))
            
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button== pg.BUTTON_LEFT:
                    self.plr.teather.deactivate()

            elif event.type ==pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.plr.booster.enable()

            elif event.type == pg.KEYUP:
                if event.key ==pg.K_SPACE:
                    self.plr.booster.disable()

    def applyControlsMenu(self,button):
        mouseClicked=False
        for event in pg.event.get():
            # checks if user has quit
            if event.type == pg.QUIT:
                self.hasQuit=True
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button== pg.BUTTON_LEFT:
                    mouseClicked=True
                    button.displayAndGetClicked(event.pos,pg.mouse.get_pressed(),self.display)
        
        if not mouseClicked:
             button.displayAndGetClicked(pg.mouse.get_pos(),(False,False,False),self.display)

    def scrollScreen(self):
        if self.screenPosition[1]+self.plr.pos.imag<self.screenSize[1]/2:
            self.screenPosition[1]=-self.plr.pos.imag+self.screenSize[1]/2
        
        self.screenPosition[1]+=self.screenVelSlope*self.tickNumber*self.spf
        
        self.screenPosition[0]=self.screenSize[0]/2 -self.plr.pos.real
    
    def resetValues(self):
        self.plr.alive=True
        self.plr.booster.disable()
        self.tickNumber=0
        self.screenVelSlope=self.config.screenVelSlope
        self.plr.pos=self.initalPlrPos
        self.plr.vel=self.initalPlrVel
        self.pivotMnger.resetPivots(self.screenPosition)
        self.screenPosition=[0,0]
        self.resetButton.wasPressed=False

        #keeps stars fixed when jumping between menus
        for i in range(0,self.bg.starNumber):
            self.bg.starsInitalPos[i]=self.bg.starsCurrentPos[i][0]+self.bg.starsCurrentPos[i][1]*1j

    def resetScreen(self):
            #intialize score text
            try:
                highScore=int(open(self.dirPath+"highscore.txt", "r").read())
            except:
                highScore=0
            score=round(self.screenPosition[1]/self.scoreDivisor)

            if score>=highScore:
                self.resetText.changeText('HIGHSCORE'+' '+str(score))
                writeHighscore=open(self.dirPath+"highscore.txt", "w+")
                writeHighscore.write(str(score))
            else:
                self.resetText.changeText('SCORE'+' '+str(abs(score)))
            
            self.plr.teather.deactivate()
            while not self.hasQuit and not self.resetButton.wasPressed:

                if not self.resetText.allLinesActivated:
                    self.resetText.activateRandomLine()

                self.scrollScreen()
                self.tickNumber+=1
                self.clock.tick_busy_loop(self.config.fps)

                self.bg.handler(self.display,self.screenSize,self.screenPosition)
                self.resetText.displayActiveLines(self.display)
                self.plr.handler(self.display,self.screenSize,self.screenPosition,self.tickNumber)
                self.pivotMnger.handler(self.display,self.screenPosition,self.screenSize,convertCoordsInv(pg.mouse.get_pos(),self.screenPosition))
                self.applyControlsMenu(self.resetButton)
                pg.display.update()

    def titleScreen(self):
            while not self.hasQuit and not self.startButton.wasPressed:

                if not self.startText.allLinesActivated:
                    self.startText.activateRandomLine()
                
                self.scrollScreen()
                self.tickNumber+=1
                self.clock.tick_busy_loop(self.config.fps)

                self.bg.handler(self.display,self.screenSize,self.screenPosition)
                self.startText.displayActiveLines(self.display)
                self.pivotMnger.handler(self.display,self.screenPosition,self.screenSize,convertCoordsInv(pg.mouse.get_pos(),self.screenPosition))
                self.applyControlsMenu(self.startButton)
                pg.display.update()

    def gameLoop(self):
            self.resetValues()
            while not self.hasQuit and self.plr.alive:
                self.scrollScreen()
                self.tickNumber+=1
                self.clock.tick_busy_loop(self.config.fps)
                self.bg.handler(self.display,self.screenSize,self.screenPosition)

                #displays score in top left
                score=abs(round(self.screenPosition[1]/self.scoreDivisor))
                self.scoreDisplay.changeText(str(score),True)
                self.scoreDisplay.displayActiveLines(self.display)

                self.plr.handler(self.display,self.screenSize,self.screenPosition,self.tickNumber)
                self.pivotMnger.handler(self.display,self.screenPosition,self.screenSize,convertCoordsInv(pg.mouse.get_pos(),self.screenPosition))
                self.applyControls()
                pg.display.update()

    def mainLoop(self):
        pg.init()
        pg.display.set_caption("Bouncy Boi")
        self.titleScreen()
        while not self.hasQuit:
            self.gameLoop()
            self.resetScreen()

if __name__=='__main__':
    cfg=Config()
    gMgr=GameManager(cfg)
    gMgr.mainLoop()
    pg.quit()  
