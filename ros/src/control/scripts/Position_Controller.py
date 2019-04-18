from PI_Controller import PI

class Position_Controller(object):

    def __init__(self,LOOP_CONSTANTS):
        self._isActive = False
        self._PIloop = PI(LOOP_CONSTANTS[0], LOOP_CONSTANTS[1])
        self._setpoint = 0.0

    def activate(self):
        self._isActive = True

    def deactivate(self):
        self._isActive = False

    def toggle(self):
        self._isActive = not self._isActive

    def set_setpoint(self, setpoint):
        #need to add data verification such as checking bounds of setpoint
        self._setpoint = setpoint

    def calculate(self, setpoint, sensor_data, dt):
        if(not self._isActive):
            return 0.0
        error = setpoint - sensor_data
        return PI.calculate(error, dt)

    def calculate(self, sensor_data, dt):
        return calculate(setpoint, sensor_data,dt)
