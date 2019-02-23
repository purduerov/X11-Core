#This is a playground to use for getting our vector math correct.  Felt kinda necessary, might delete later

def getVectorStartPoint(prevVector):
	xCamWidth = 640
	yCamHeight = 360
	origin = [0, 0]
	prevMag = sqrt((prevVector[0])**2 + (prevVector[1]**2))
	unitVect = [prevVector[0]/prevMag, prevVector[1]/prevMag]
	if(abs(unitVect[0]) > abs(unitVect[1])):
		if (unitVect[0] > 0):
			#This origin point is the left middle
			startPoint = [origin[0], origin[1] + yCamHeight / 2]
		else:
			#This origin point is the right middle
			startPoint = [origin[0] + xCamWidth, origin[1] + yCamHeight / 2]	
	else:
		if (unitVect[1] > 0);
			#This origin point is the bottom middle
			startPoint = [origin[0] + xCamWidth / 2, origin[1] + yCamHeight]
		else:
			#This origin point is the top middle
			startPoint = [origin[0] + xCamWidth / 2, origin[1]]
	return startPoint

def getThrustVect(prevVector, startPoint, center):
	resultantVector = [center[0] - startPoint[0], center[1] - startPoint[1]
	thrustVect = [resultantVector[0] - prevVector[0], resultantvector[1] - prevVector[1]]
	
	return thrustVect,resultantVector


