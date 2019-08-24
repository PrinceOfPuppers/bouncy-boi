import pygame as pg
from config import Config
from player import Player,Booster,Teather
from pivots import PivotManager
from helperFuncts import convertCoords,convertCoordsInv
from menu import Button,TextBox

class GameManager:

    def __init__(self,config):

        self.hasQuit=False
        self.tickNumber=0
        self.display=pg.display.set_mode((config.screenSize[0], config.screenSize[1]))
        self.pivotMnger=PivotManager(config)
        self.clock=pg.time.Clock()
        self.initalPlrVel=config.initalPlayerVel
        self.initalPlrPos=config.screenSize[0]/2+1j*config.screenSize[1]

        self.plr=Player(config,Teather(config),Booster(config),self.initalPlrPos,self.initalPlrVel)


        self.config=config
        #screen height is height of top left corner from start (value will get more negative as player goes up)
        self.screenPosition=[0,0]
        self.screenSize=config.screenSize
        self.screenVelSlope=config.screenVelSlope
        self.spf=1/config.fps
        
        self.scoreDisplay=TextBox('PLACEHOLDER',(255,0,0),(self.screenSize[0]/10,self.screenSize[1]/10),40)

        self.resetButton=Button((self.screenSize[0]/2,2*self.screenSize[1]/3),self.screenSize[0]/8,self.screenSize[0]/8,config.resetSymbol,(255,0,0),(255,255,255),True)
        self.resetText=TextBox('PLACEHOLDER',(255,0,0),(self.screenSize[0]/2,self.screenSize[1]/3),80)
        self.resetText.initalizeTextBox()

        self.startButton=Button((self.screenSize[0]/2,2*self.screenSize[1]/3),self.screenSize[0]/8,self.screenSize[0]/8,config.playSymbol,(255,0,0),(255,255,255),True)
        self.startText=TextBox('BOUNCY BOI',(255,0,0),(self.screenSize[0]/2,self.screenSize[1]/3),80)
        self.startText.initalizeTextBox()

    def applyControls(self):
        for event in pg.event.get():
            # checks if user has quit
            if event.type == pg.QUIT:
                self.hasQuit=True
                
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button== pg.BUTTON_LEFT:
                    self.plr.teather.activate(self.plr.pos,self.pivotMnger,convertCoordsInv(event.pos,self.screenPosition))
            
            if event.type == pg.MOUSEBUTTONUP:
                if event.button== pg.BUTTON_LEFT:
                    self.plr.teather.deactivate()
        
        keys=pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            self.plr.booster.boost(self.display,self.plr,self.screenPosition,self.tickNumber)

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
        self.tickNumber=0
        self.screenVelSlope=self.config.screenVelSlope
        self.plr.pos=self.initalPlrPos
        self.plr.vel=self.initalPlrVel
        self.pivotMnger.resetPivots(self.screenPosition)
        self.screenPosition=[0,0]
        self.resetButton.wasPressed=False

    def resetScreen(self):
            #intialize score text
            score=round(self.screenPosition[1]/10)
            self.resetText.changeText('SCORE'+' '+str(score))
            self.plr.teather.deactivate()
            while not self.hasQuit and not self.resetButton.wasPressed:

                if not self.resetText.allLinesActivated:
                    self.resetText.activateRandomLine()

                self.scrollScreen()
                self.tickNumber+=1
                self.clock.tick_busy_loop(self.config.fps)

                pg.Surface.fill(self.display,(0,0,0))
                self.resetText.displayActiveLines(self.display)
                self.plr.handler(self.display,self.screenSize,self.screenPosition)
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

                pg.Surface.fill(self.display,(0,0,0))
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

                pg.Surface.fill(self.display,(0,0,0))
                self.plr.handler(self.display,self.screenSize,self.screenPosition)
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