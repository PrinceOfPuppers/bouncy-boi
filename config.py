import tkinter
import numpy as np
root=tkinter.Tk()

class Config:
    def __init__(self):
        self.fps=60
        self.round=5

        self.pivotRadius=10
        self.grav=0+981j

        self.screenVelSlope=0#0.1
        self.initalPlayerVel=0-1000j

        self.teatherSpringConst=100
        self.teatherMaxStrech=100

        #applied in boosthandler
        self.screenShake=3

        self.starRadius=3
        self.starParalaxCoefficents = [1,1.5,2.74]
        self.starColor=(120,120,120)
        self.scoreDivisor=10

        self.fontSize=60
        self.boostMax=100
        self.boostRechargeRate=1
        self.boostConsumptionRate=1
        self.boostForce=500
        #screen dimensions and scaling
        screenWidth=root.winfo_screenwidth()-100
        screenHeight=root.winfo_screenheight()-100
        self.screenSize=[screenWidth,screenHeight]

        devWidth=1500
        self.screenScaling=screenWidth/devWidth

        self.randPivotYOffsetCap=50
        self.numPivots=6

        self.resetSymbol=[[[-50, 0], [-70, -30], [-60, -30], [-60, -60], [60, -60], [60, 60], [-60, 60], [-60, 10], [-40, 10], [-40, 40], [40, 40], [40, -40], [-40, -40], [-40, -30], [-30, -30]]]
        self.playSymbol=[[[-30, -40], [-30, 40]], [[-30, 40], [50, 0]], [[50, 0], [-30, -40]]]
        
        self.playerAsset=np.array([[-10.0, 15], [0.0, -15.0], [10.0, 15], [0.0, 5.0]])
        self.pivotAssets=np.array([[[-15, 0], [-15, 0], [-10, 5], [-10, 10], [-5, 10], [0, 15], [5, 10], [10, 10], [10, 5], [15, 0], [10, -5], [10, -10], [5, -10], [0, -15], [-5, -10], [-10, -10],[-10, -5]],[[0, 5], [5, 0], [0, -5], [-5, 0]]])
        
        self.boosterAnimation=np.array([
            [[0.0, 10.0], [-5.0, 15.0], [0.0, 30.0], [5.0, 15.0]], 
            [[0.0, 10.0], [-5.0, 15.0], [0.0, 35.0], [5.0, 15.0]], 
            [[0.0, 10.0], [-5.0, 15.0], [0.0, 40.0], [5.0, 15.0]], 
            [[0.0, 10.0], [-5.0, 15.0], [0.0, 45.0], [5.0, 15.0]],
            [[0.0, 10.0], [-5.0, 15.0], [0.0, 40.0], [5.0, 15.0]],
            [[0.0, 10.0], [-5.0, 15.0], [0.0, 35.0], [5.0, 15.0]]
            ])