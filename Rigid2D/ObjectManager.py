from Rigid2D.Utilities.util import *
from Rigid2D.Utilities.math import *
from Rigid2D.Utilities.Engine import *

import pygame as pg

class ObjectManagerClass:
    def __init__(self,app):
        self.app = app

        self.objects = []

    def getPhysics(self):
        return self.app.Physics
        
    def _updateObjects(self, obj):  
        self.getPhysics().update(obj)
        #pass

    def _screenTexDraw(self, obj):
        camera = self.app.Camera
        pos = obj.Position
        size = obj.Size
        trans = 255 * obj.Transparency
        rot = obj.Rotation
        color = obj.Color

        camScale = camera.getWorldTileScale()

        size = size * camScale
        size_list = size.list

        pos_list = camera.worldToScreen(pos * camScale).list

        tex = None

        if (not obj.Texture == None):
            tex = pg.image.load(obj.Texture).convert_alpha()
        else:
            tex_color = ColorToTuple(color)
            tex = pg.surface.Surface(size_list)
            tex.fill(tex_color)

        if (tex == None): return 
        
        tex = pg.transform.scale(tex, size_list)
        tex = pg.transform.rotate(tex, rot)
        tex.set_alpha(trans)

        texRect = tex.get_rect(center=pos_list)
        self.app.Renderer.display.blit(tex, texRect)

    def _drawObjects(self, obj):
        #if (not self.app.Renderer.checkRenderDistance(obj)): return
        #self._screenTexDraw(obj)
        self.app.Renderer.drawRect(obj)
  
    def sortObjectList(self):
        if (len(self.objects) == 0): return 
        max_Zval = max(obj.ZValue for obj in self.objects)

        count = [[] for _ in range(max_Zval + 1)]

        for obj in self.objects:
            count[obj.ZValue].append(obj)

        sorted_list = []

        for bucket in count:
            sorted_list.extend(bucket)

        self.objects = sorted_list

    def getObject_byID(self,oID):
        for obj in self.objects:
            if type(oID) == int:
                if obj.Id == oID:
                    return obj
            elif type(oID) == GameObject:
                if obj.Id == oID.Id:
                    return obj
        return None

    def getObject_byName(self, Name):
        for obj in self.objects:
            if obj.Name == Name:
                return obj

        return None

    def createObject(self):
        obj = GameObject(self.app)
        self.sortObjectList()
        return obj
        
    def Start(self):
        for obj in self.objects:
            self._updateObjects(obj)
            self._drawObjects(obj)
        
