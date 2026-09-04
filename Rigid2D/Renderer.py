from Rigid2D.Utilities.util import *
from Rigid2D.Utilities.math import *
from Rigid2D.Utilities.Engine import *

import pygame as pg


def getShader( file):
    with open(file, encoding="utf-8") as file:
        data = file.read()

    return data

class Renderer:
    def __init__(self,app):
        self.app = app

        self.color = Color3(55,222,240)

        self.display = pg.surface.Surface((app.width, app.height))
        self.uiDisplay = pg.surface.Surface((app.width, app.height), pg.SRCALPHA)


        self.tex = None
        self.surfTex = None
        self.texture = None

        self._tex_cache = set()

        self.renderDistance = Vector2(10, 10)

        self.uPos = None
        self.uSize = None
        self.uColor = None 
        self.uObjTex = None
        self.uCheckObjTex = None

    def createRectUniforms(self):
        self.uPos = glGetUniformLocation(self.app.shaderProgram_Objects, "uPos")
        self.uSize = glGetUniformLocation(self.app.shaderProgram_Objects, "uSize")
        self.uColor = glGetUniformLocation(self.app.shaderProgram_Objects, "uColor")
        self.uObjTex = glGetUniformLocation(self.app.shaderProgram_Objects, "uObjTex")
        self.uCheckObjTex = glGetUniformLocation(self.app.shaderProgram_Objects, "uCheckObjTex")

    def checkRenderDistance(self, obj):
        camera = self.app.Camera
        camPos = camera.Position

        camScale = camera.getWorldTileScale()

        pos = camera.worldToScreen(obj.Position)
        camPos = camera.worldToScreen(camPos)

        objSize = obj.Size * camScale

        obj_rect = pg.Rect(
            pos.x,
            pos.y,
            objSize.x,
            objSize.y 
        )

        rd_rect = pg.Rect(
            camPos.x,
            camPos.y,
            self.renderDistance.x,
            self.renderDistance.y
        )

        return rd_rect.colliderect(obj_rect)

    def get_texture(self, path):

        if path in self._tex_cache:
            tex = pg.image.load(path).convert_alpha()
            self._tex_cache[path] = tex
        return tex

    def add_texture(self, path):
        self._tex_cache.add(path)

    def createScreenTex(self):
        self.texture = glGenTextures(1)
        self.surfTex = glGenTextures(1)

    def clear(self, color: Color4 | UColor4):
        if isinstance(color, Color4):
            c = ColorToTuple(color.UnitColor)  
        elif isinstance(color, UColor4):
            c = ColorToTuple(color)
        else:
            raise TypeError("Color type must be a Color4 or UColor4")

        r, g, b, a = c
    
        if max(r, g, b, a) > 1.0:
            r, g, b, a = r / 255.0, g / 255.0, b / 255.0, a / 255.0

        glClearColor(float(r), float(g), float(b), float(a))
        glClear(GL_COLOR_BUFFER_BIT)

    def surface_to_Tex(self, surf: pg.Surface):
        surf = pg.transform.flip(surf, False, True)
        surf = surf.convert_alpha()
        w, h = surf.get_size()
        pixels = pg.image.tobytes(surf, "BGRA")

        texture = self.texture
        if not texture:
            texture = glGenTextures(1)
            self.texture = texture

        glBindTexture(GL_TEXTURE_2D, texture)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)  # optional for BGRA; required for RGB

        glTexImage2D(
            GL_TEXTURE_2D, 0,
            GL_RGBA8,          # how GPU stores it
            w, h, 0,
            GL_BGRA,           # how your bytes are laid out
            GL_UNSIGNED_BYTE,
            pixels
        )

        glBindTexture(GL_TEXTURE_2D, 0)
        return texture

    def createShaderProgram(self, vert, frag):        
        VERT = glCreateShader(GL_VERTEX_SHADER)
        FRAG = glCreateShader(GL_FRAGMENT_SHADER)

        vert = getShader(vert)
        frag = getShader(frag)

        glShaderSource(VERT,vert)
        glCompileShader(VERT)
        if not glGetShaderiv(VERT, GL_COMPILE_STATUS):
            raise RuntimeError(glGetShaderInfoLog(VERT).decode())
        
        glShaderSource(FRAG,frag)
        glCompileShader(FRAG)

        if not glGetShaderiv(FRAG, GL_COMPILE_STATUS):
            raise RuntimeError(glGetShaderInfoLog(FRAG).decode())

        shaderProgram = glCreateProgram()

        glAttachShader(shaderProgram, VERT)
        glAttachShader(shaderProgram, FRAG)

        glLinkProgram(shaderProgram)

        if not glGetProgramiv(shaderProgram, GL_LINK_STATUS):
            raise RuntimeError(glGetProgramInfoLog(shaderProgram).decode())

        glDeleteShader(VERT)
        glDeleteShader(FRAG)

        return shaderProgram
        
    def drawScreen(self):
        texture = self.surface_to_Tex(self.display)

        glUseProgram(self.app.shaderProgram)
        glBindVertexArray(self.app.rect_mesh)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texture)
        glUniform1i(self.tex, 0)
        
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
                
    def createRectMesh(self):
        
        vertecies_info = [
            # x, y,   u, v
            -1.0,  1.0,  0.0, 1.0, 
            -1.0, -1.0,  0.0, 0.0,  
            1.0,  1.0,  1.0, 1.0,  
            1.0, -1.0,  1.0, 0.0, 
        ]

        indices_info = [
            0, 1, 2,  
            1, 3, 2,  
        ]
        
        vertices = np.array(vertecies_info, dtype='f4')
        indices  = np.array(indices_info, dtype='u4')

        vao = glGenVertexArrays(1)
        glBindVertexArray(vao)

        vbo = glGenBuffers(1)
        ebo = glGenBuffers(1)
        
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 4 * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 4 * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(2 * ctypes.sizeof(ctypes.c_float)))
        glEnableVertexAttribArray(1)

        glBindVertexArray(0)

        return vao

    def drawRect(self, obj):

        camera = self.app.Camera

        size = obj.Size
        pos = camera.worldToScreen_GL(obj.Position)
        color = obj.Color.UnitColor()
        trans = obj.Transparency

        glUseProgram(self.app.shaderProgram_Objects)
        glBindVertexArray(self.app.rect_mesh)

        width, height = self.app.getWindowSize().list

        aspect = width / height

        glScaleFactor = (self.app.worldScaleFactor / 10)

        size_Width = size.x / aspect / glScaleFactor
        size_Height = size.y / glScaleFactor

        pos_X = pos.x / aspect / glScaleFactor * -1
        pos_Y = pos.y / glScaleFactor * -1

        glUniform2f(self.uSize, size_Width, size_Height)
        glUniform2f(self.uPos, pos_X, pos_Y)
        glUniform4f(self.uColor, color.r, color.g, color.b, trans)

        glUniform1i(self.uCheckObjTex, obj.texture)

        if  obj.texture:
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, obj.TEXTUREID)
            glUniform1i(self.uObjTex, 0)
                
        
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

        glUseProgram(0)
        glBindVertexArray(0)