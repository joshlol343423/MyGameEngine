from Rigid2D.Utilities.math import *
from Rigid2D.Utilities.util import *


class Player:
    def __init__(self,app):
        self.app = app

        self.playerHealth = 3
    
    def killPlayer(self):
        print("Kill")
        
    def getHealth(self):
        return self.playerHealth