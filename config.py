import tkinter
root=tkinter.Tk()

class Config:
    def __init__(self):
        self.fps=60
        self.round=5

        self.pivotRadius=10
        self.grav=0+981j

        #screen dimensions and scaling
        screenWidth=root.winfo_screenwidth()-100
        screenHeight=root.winfo_screenheight()-100
        self.screenSize=[screenWidth,screenHeight]

        devWidth=1500
        self.screenScaling=screenWidth/devWidth
        self.resetSymbol=[[[-50, 0], [-70, -30], [-60, -30], [-60, -60], [60, -60], [60, 60], [-60, 60], [-60, 10], [-40, 10], [-40, 40], [40, 40], [40, -40], [-40, -40], [-40, -30], [-30, -30]]]
        self.playSymbol=[[[-30, -40], [-30, 40]], [[-30, 40], [50, 0]], [[50, 0], [-30, -40]]]
        
        