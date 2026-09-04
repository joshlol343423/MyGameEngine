from Rigid2D.Utilities.util import *
from Rigid2D.Utilities.math import *
from Rigid2D.Utilities.Engine import *

class Physics:
    def __init__(self, app):
        self.gravity = 9.81 

        self.app = app 
        self.enabled = True

        self.clampDelta = (1/100)
        self.physicsType = PhysicsType.DEFAULT

        self.scale = 2

    def ifTouched(self, obj1, obj2) -> bool:
        overlapX, overlapY = self._getObjectOverlapping(obj1, obj2)
        if overlapX > 0 and overlapY > 0:
            return True
        return False

    
    def _getObjectOverlapping(self, obj1, obj2) -> Vector2:
        
        size1 = obj1.RectSize * self.scale
        size2 = obj2.RectSize * self.scale
   

        dx = obj1.Position.x - obj2.Position.x
        dy = obj1.Position.y - obj2.Position.y

        overlapX = (size1.x / 2 + size2.x / 2) - abs(dx)
        overlapY = (size1.y / 2 + size2.y / 2) - abs(dy)

        return Vector2(overlapX, overlapY)

    def _collisionX(self, obj1, obj2):

        size1 = obj1.RectSize * self.scale
        size2 = obj2.RectSize * self.scale

        overlapX, overlapY = self._getObjectOverlapping(obj1, obj2).list

        if overlapX > 0 and overlapY > 0:
      
            # Horizontal collision
            if overlapX < overlapY:

                # Object is on the right
                if obj1.Position.x > obj2.Position.x:

                    obj1.Position.x = (
                        obj2.Position.x +
                        size2.x / 2 +
                        size1.x / 2
                    )

                    obj1.colliderBox["Left"] = True

                # Object is on the left
                else:

                    obj1.Position.x = (
                        obj2.Position.x -
                        size2.x / 2 -
                        size1.x / 2
                    )

                    obj1.colliderBox["Right"] = True


                obj1.Velocity.x = 0

    def _collisionY(self, obj1, obj2):

        size1 = obj1.RectSize * self.scale
        size2 = obj2.RectSize * self.scale

        overlapX, overlapY = self._getObjectOverlapping(obj1, obj2).list

        if overlapX > 0 and overlapY > 0:

            # Vertical collision
            if overlapY <= overlapX:

                # Object is below
                if obj1.Position.y < obj2.Position.y:

                    obj1.Position.y = (
                        obj2.Position.y -
                        size2.y / 2 -
                        size1.y / 2
                    )

                    obj1.Velocity.y = 0
                    
                    obj1.colliderBox["Top"] = True


                # Object is above
                else:

                    obj1.Position.y = (
                        obj2.Position.y +
                        size2.y / 2 +
                        size1.y / 2
                    )

                    obj1.Velocity.y = 0
                    obj1.colliderBox["Bottom"] = True

    def checkCollisionsX(self, obj):

        obj.colliderBox["Left"] = False
        obj.colliderBox["Right"] = False

        for colliderObject in self.app.ObjectManager.objects:

            if obj == colliderObject:
                continue

            if not obj.CanCollide or not colliderObject.CanCollide:
                continue

            if obj.Anchored and colliderObject.Anchored:
                continue

            self._collisionX(obj, colliderObject)

    def checkCollisionsY(self, obj):

        obj.colliderBox["Top"] = False
        obj.colliderBox["Bottom"] = False

        for colliderObject in self.app.ObjectManager.objects:

            if obj == colliderObject:
                continue

            if not obj.CanCollide or not colliderObject.CanCollide:
                continue

            if obj.Anchored and colliderObject.Anchored:
                continue

            self._collisionY(obj, colliderObject)

    def update(self, obj):
            
        if obj.Anchored:
            obj.Velocity = Vector2(0,0)
            return

        if (not self.app.Renderer.checkRenderDistance(obj)): return

        dt = self.app.deltaTime

        
        obj.Velocity.y -= self.gravity / 10 * dt * obj.Mass 
        
        obj.Position.x += obj.Velocity.x * dt
        self.checkCollisionsX(obj)

        obj.Position.y += obj.Velocity.y * dt
        self.checkCollisionsY(obj)

        if (self.physicsType == PhysicsType.DEFAULT):
            pass
        elif (self.physicsType == PhysicsType.BOX2D):
            pass
        elif (self.physicsType == PhysicsType.MUNK):
            pass
        else:
            print("Error: Physics type not valid")
