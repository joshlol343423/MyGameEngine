
from Rigid2D.Utilities.util import *
from Rigid2D.Utilities.math import *



class GameObject:
    def __init__(self,app):
        self.app = app

        self.Name = "Object"

        self.Position = Vector2(1,1)
        self.Size = Vector2(1,1)
        self.Transparency = 1.0
        self.Color = Color3(255,255,255)
        self.Rotation = 0
        self.TextureFlip = False
        self.Texture = None

        self.Velocity = Vector2(0,0)

        
        self.ZValue = 0

        self.CanCollide = True
        self.Anchored = False
        
        
        self.Static = False
        self.Mass = 1

        self.RectSize = Vector2(1, 1)

        self.Id = 0
        
        self.Animation = None
        self.AnimationIsPlaying = False
        self.AnimationFrameNum = 0

        self.scripts = []

        self.colliderBox = {
            "Top" : False,
            "Bottom" : False,
            "Left" : False,
            "Right" : False
        }

        self.TEXTUREID = None
        self.texture = False

        self.start()

    def setObjectTexture(self, tex: str):
        if type(tex) == list:
            tex = tex[0]

        folder = os.path.abspath(os.path.join("res", "Textures"))
        tex = getFile(folder, tex)

        image = pg.image.load(tex).convert_alpha()
        image = pg.transform.flip(image, False, True)  # OpenGL y is up
        w, h = image.get_size()
        pixels = pg.image.tostring(image, "RGBA", False)

        if not hasattr(self, "TEXTUREID") or self.TEXTUREID == None:
            self.TEXTUREID = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, self.TEXTUREID)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        glTexImage2D(
            GL_TEXTURE_2D, 0, GL_RGBA,
            w, h, 0,
            GL_RGBA, GL_UNSIGNED_BYTE,
            pixels
        )
        glGenerateMipmap(GL_TEXTURE_2D)

        glBindTexture(GL_TEXTURE_2D, 0)
        self.texture = True
        return tex
    
    def clone(self):
        return copy.copy(self)

    def playAnimation(self):
        if self.Animation is None: return

    def stopAnimation(self):
        if self.Animation is None: return
        
    def start(self):
        if self in self.app.ObjectManager.objects: return
        self.app.ObjectManager.objects.append(self)
            
    def end(self):
        if not self in self.app.ObjectManager.objects: return 
        self.app.ObjectManager.objects.remove(self)
