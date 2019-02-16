#This is a playground to use for getting our vector math correct.  Felt kinda necessary, might delete later

def getVectorStartPoint(prevVector):
	prevMag = sqrt((prevVector[0])**2 + (prevVector[1]**2))
	unitVect = [prevVector[0]/prevMag, prevVector[1]/prevMag]
	if(abs(unitVect[0]) > abs(unitVect[1])):
		if (unitVect[0] > 0):
			#This origin point is the left middle
		else:
			#This origin point is the right middle

	else:
		if (unitVect[1] > 0);
			#This origin point is the bottom middle
		else:
			#This origin point is the top middle
	return startPoint

def getThrustVect(prevVector, startPoint, center):
	resultantVector = [center[0] - startPoint[0], center[1] - startPoint[1]
	thrustVect = [resultantVector[0] - prevVector[0], resultantvector[1] - prevVector[1]]
	
	return thrustVect,resultantVector


