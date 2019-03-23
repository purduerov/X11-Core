#This is a playground to use for getting our vector math correct.  
#One of the main issues with this is that it assumes that the ROV moved exactly in the direction that it previously told it to move.  Very difficult to assume this.
import math as m

class Vector:
	prev_vector = [,]
	x_cam_width = 640
	y_cam_height = 480
	def __init__(self,thrust_vect = [,], resultant_vect = [,]):
		self.thrust_vect = thrust_vect
		self.resultant_vect = resultant_vect

	def get_vector_start_point():
		origin = [0, 0]
		prev_mag = m.sqrt((prev_vector[0])**2 + (prev_vector[1]**2))
		unit_vect = [prev_vector[0]/prev_mag, prev_vector[1]/prev_mag]
		if(abs(unit_vect[0]) > abs(unit_vect[1])):
			if (unit_vect[0] > 0):
				#This origin point is the left middle
				start_point = [origin[0], origin[1] + y_cam_height / 2]
			else:
				#This origin point is the right middle
				start_point = [origin[0] + x_cam_width, origin[1] y_cam_height / 2]	
		else:
			if (unit_vect[1] > 0):
				#This origin point is the bottom middle
				start_point = [origin[0] + x_cam_width / 2, origin[1] + y_cam_height]
			else:
				#This origin point is the top middle
				start_point = [origin[0] + x_cam_width / 2, origin[1]]
		return start_point

	def get_thrust_vect(start_point, center):
		resultant_vector = [center[0] - start_point[0], center[1] - start_point[1]]
		thrust_vect = [resultant_vector[0] - prev_vector[0], resultant_vector[1] - prev_vector[1]] 
		
		return thrust_vect,resultant_vector

