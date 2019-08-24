import numpy as np
from math import sin,cos
def convertCoords(worldComplex,screenPos):
    screenTup=(int(screenPos[0]+worldComplex.real),int(screenPos[1]+worldComplex.imag))
    return(screenTup)

def convertCoordsInv(screenTup,screenPos):
    worldComplex=screenTup[0]-screenPos[0]+(screenTup[1]-screenPos[1])*1j
    return(worldComplex)

def rotateVecs(matrixToRotate,matrixToWrite,angle,rotMatrix):
    #this is the transpose of the usual rotation matrix because
    #vecs are represented as row vectors
    rotMatrix[0][0]=round(cos(angle),5)
    rotMatrix[0][1]=round(sin(angle),5)
    rotMatrix[1][0]=round((-1)*sin(angle),5)
    rotMatrix[1][1]=round(cos(angle),5)

    #note vectors are rendered as row vectors, hence the order is reversed
    np.matmul(matrixToRotate,rotMatrix,matrixToWrite)