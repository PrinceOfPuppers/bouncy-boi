def convertCoords(worldComplex,screenPos):
    screenTup=(int(screenPos[0]+worldComplex.real),int(screenPos[1]+worldComplex.imag))
    return(screenTup)

def convertCoordsInv(screenTup,screenPos):
    worldComplex=screenTup[0]-screenPos[0]+(screenTup[1]-screenPos[1])*1j
    return(worldComplex)