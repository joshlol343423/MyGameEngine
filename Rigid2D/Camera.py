from Rigid2D.Utilities.util import *
from Rigid2D.Utilities.math import *
from Rigid2D.Utilities.Engine import *

class Camera:
    def __init__(self,app):
        self.app = app
        self.Position = Vector2(0,0)

        self.target = None

        self.cameraSpeed = 100
        self.setToCameraTarget = True

        self.cameraScale = 1

        self.maxScale = 50
        self.minScale = 0
        self.scrollSpeed = 0.1
        self.scroll = 0
        self.lineThickness = 1

    def getWorldTileScale(self) -> Vector2:
        worldScale = Vector2(0, 0)
        worldScale.x = self.cameraScale * self.app.worldScaleFactor * self.app.worldScaleWidth
        worldScale.y = self.cameraScale * self.app.worldScaleFactor * self.app.worldScaleHeight
        return worldScale

    def worldToScreen(self,pos) -> Vector2:

        camScale = self.getWorldTileScale()
        pos = pos * Vector2(1,-1)

        pos = pos - (self.Position * Vector2(1,-1)) * self.app.worldScaleFactor * Vector2(
            self.app.worldScaleWidth,
            self.app.worldScaleHeight
        )

        pos = pos + Vector2( 
            self.app.width / 2, 
            self.app.height / 2
        )

        return pos

    def worldToScreen_GL(self, pos):
        return self.Position - pos
    
    def setToTarget(self) -> Vector2:
        if not self.setToCameraTarget: return
        target = self.app.ObjectManager.getObject_byID(self.target)
        if target == None: return
        
        self.Position = target.Position 

    def cameraDebug(self):
    
        center = self.worldToScreen(Vector2(0,0))
        keys = pg.key.get_pressed()

        if keys[pg.K_LCTRL]:
            if self.scroll == 1:
                self.cameraScale += self.scrollSpeed
                if self.cameraScale > self.maxScale:
                    self.cameraScale = self.maxScale
                
            if self.scroll == -1:
                self.cameraScale -= self.scrollSpeed
                if self.cameraScale <= self.minScale:
                    self.cameraScale = self.minScale

        # vertical line (top to bottom)
        pg.draw.line(
            self.app.Renderer.display, 
            (255,0,0),
            (center.x, 0),
            (center.x, self.app.height), self.lineThickness)

        # horizontal line (left to right)
        pg.draw.line(
            self.app.Renderer.display, 
            (255,0,0),
            (0, center.y),
            (self.app.width, center.y), self.lineThickness)
            
        # Highlights the target
        if not self.target == None:
        
            targetPos = self.app.ObjectManager.getObject(self.target)
            if not targetPos == None:
                targetPos = Vector2(
                    targetPos["Position"]["x"],
                    targetPos["Position"]["y"]
                ) * 100 * self.cameraScale * Vector2(self.app.worldScaleWidth, self.app.worldScaleWidth)
                pg.draw.circle(
                    self.app.veiwPort, 
                    (255,0,0), 
                    self.fixAxies(targetPos).list, 10 * self.cameraScale)

        
        if keys[pg.K_UP] and keys[pg.K_LCTRL]:
            self.Position += Vector2(0,self.cameraSpeed)
        if keys[pg.K_DOWN] and keys[pg.K_LCTRL]:
            print("Down")
            self.Position -= Vector2(0,self.cameraSpeed)
        if keys[pg.K_LEFT] and keys[pg.K_LCTRL]:
            self.Position -= Vector2(self.cameraSpeed,0)
        if keys[pg.K_RIGHT] and keys[pg.K_LCTRL]:
            self.Position += Vector2(self.cameraSpeed,0)

        if keys[pg.K_RSHIFT]:
            self.Position = Vector2(0,0)
        if keys[pg.K_LSHIFT]:
            if not self.target == None: 
                targetPos = self.app.ObjectManager.getObject(self.target)
                targetPos = Vector2(
                    targetPos["Position"]["x"],
                    targetPos["Position"]["y"]
                ) * 100 * self.cameraScale * Vector2(self.app.worldScaleWidth, self.app.worldScaleWidth)
                self.Position = targetPos

        #self.draw_view_box(center)
    