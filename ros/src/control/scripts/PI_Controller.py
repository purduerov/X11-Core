import numpy

class PI(object):
    """A generic PID loop controller which can be inherited and used in other control algorithms"""

    def __init__(self, p=1, i=0):
        """Return a instance of a un tuned PID controller"""
        self._p = p
        self._i = i
        self._esum = 0              #Error sum for integral term
        self._count = 0

    def calculate(self, error, dt):

        """Calculates the output of the PI controller"""
        self._esum += error*dt
        u = self._p*error + self._i*self._esum
        return u


    def reset(self):
        """Resets the integral sum"""
        self._esum = 0

    @property
    def p(self):
        return self._p

    @p.setter
    def p(self, value):
        self._p = value

    @property
    def i(self):
        return self._i

    @i.setter
    def i(self, value):
        self._i = value
