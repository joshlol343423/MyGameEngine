from Rigid2D.Objects import *

class Tween:
    def __init__(self, startVal : int | float, endVal : int | float, intervol : int | float):

        self.start = startVal
        self.end = endVal
        self.intervol = intervol

        self.reached = False

    def startTween(self,dt : float) -> None:
        if (self.start >= self.end):
            self.reached = True
            return 
        self.reached = False
        self.start += self.intervol * dt

    def startTweenThread(self, dt : float):
        pass