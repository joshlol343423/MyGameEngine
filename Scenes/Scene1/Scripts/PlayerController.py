from Rigid2D.Utilities.math import *
from Rigid2D.Utilities.util import *
from Rigid2D.Utilities.Engine import *

class PlayerController:
    def __init__(self, app):
        self.app = app

        self.playerSpeed = 1

        self.player = self.app.ObjectManager.getObject_byName("Player")
        
        self.playerMod = self.app.GetModule("Player")

        self.player.Mass = 20.6
        self.playerSpeed = 320
        self.playerJumpForce = 1000

        self.clampDelta = (1/100)
        
    def update(self, dt):

        if (self.app.input.is_key_pressed(Key.SPACE) and 
            not self.player.colliderBox["Bottom"] == False):
            self.player.Velocity.y += min(self.playerJumpForce * dt, self.playerJumpForce * self.clampDelta)

        if (self.app.input.is_key_pressed(Key.A)):
            if (self.player.Velocity.x < 0): self.player.Velocity.x = 0
            self.player.Velocity.x -= min(self.playerSpeed * dt, self.playerSpeed * self.clampDelta)
            self.player.Velocity.x = max(self.player.Velocity.x, -self.playerSpeed)
        elif (self.app.input.is_key_pressed(Key.D)):
            if (self.player.Velocity.x > 0): self.player.Velocity.x = 0
            self.player.Velocity.x += min(self.playerSpeed * dt, self.playerSpeed * self.clampDelta)
            self.player.Velocity.x = min(self.player.Velocity.x, self.playerSpeed)
        else:
            self.player.Velocity.x = 0


        


    