import pygame as pg
from pygame.locals import *

import imgui
from imgui.integrations.pygame import PygameRenderer
from imgui.integrations.opengl import ProgrammablePipelineRenderer

from Box2D import b2World, b2_dynamicBody, b2_staticBody, b2PolygonShape
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

import traceback

import os

import ctypes
import json
import random
import uuid
import copy
import time 
import importlib.util
from enum import Enum
from pathlib import Path
import glm

class ImGuiGL(ProgrammablePipelineRenderer):
    def __init__(self):
        super().__init__()
        self._gui_time = None
        

    def process_event(self, event):
        io = self.io
        if event.type == pg.MOUSEMOTION:
            io.mouse_pos = event.pos
        elif event.type == pg.MOUSEBUTTONDOWN and event.button <= 3:
            io.mouse_down[event.button - 1] = 1
        elif event.type == pg.MOUSEBUTTONUP and event.button <= 3:
            io.mouse_down[event.button - 1] = 0
        
            
        elif event.type == pg.VIDEORESIZE:
            io.display_size = event.size
        elif event.type == pg.KEYDOWN:
            if event.unicode:
                code = ord(event.unicode)
                if 0 < code < 0x10000:
                    io.add_input_character(code)
            if event.key == pg.K_BACKSPACE:
                io.keys_down[pg.K_BACKSPACE] = True

        elif event.type == pg.KEYUP:
            if event.key == pg.K_BACKSPACE:
                io.keys_down[pg.K_BACKSPACE] = False
                

    def process_inputs(self):
        io = imgui.get_io()
        now = pg.time.get_ticks() / 1000.0
        io.delta_time = (now - self._gui_time) if self._gui_time else 1 / 60
        if io.delta_time <= 0:
            io.delta_time = 1 / 1000
        self._gui_time = now

class ImGuiGL(ProgrammablePipelineRenderer):
    def __init__(self):
        super().__init__()
        self._gui_time = None
        self._ids = {}

        km = self.io.key_map
        km[imgui.KEY_BACKSPACE] = self._id(pg.K_BACKSPACE)
        km[imgui.KEY_DELETE]    = self._id(pg.K_DELETE)
        km[imgui.KEY_ENTER]     = self._id(pg.K_RETURN)
        km[imgui.KEY_LEFT_ARROW]  = self._id(pg.K_LEFT)
        km[imgui.KEY_RIGHT_ARROW] = self._id(pg.K_RIGHT)
        km[imgui.KEY_HOME] = self._id(pg.K_HOME)
        km[imgui.KEY_END]  = self._id(pg.K_END)

        pg.key.set_repeat(400, 40)   # hold-to-repeat

    def _id(self, key):
        if key not in self._ids:
            self._ids[key] = len(self._ids)   # 0..512 only
        return self._ids[key]

    def process_event(self, event):
        io = self.io

        if event.type == pg.MOUSEMOTION:
            io.mouse_pos = event.pos

        elif event.type == pg.MOUSEBUTTONDOWN and event.button <= 3:
            io.mouse_down[event.button - 1] = 1

        elif event.type == pg.MOUSEBUTTONUP and event.button <= 3:
            io.mouse_down[event.button - 1] = 0
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 4:
                io.mouse_wheel = 0.5
            elif event.button == 5:
                io.mouse_wheel = -0.5
        elif event.type == pg.KEYDOWN:
            # letters/numbers only — skip \b, \r, etc.
            if event.unicode and ord(event.unicode) >= 32:
                io.add_input_character(ord(event.unicode))
            io.keys_down[self._id(event.key)] = True

        elif event.type == pg.KEYUP:
            io.keys_down[self._id(event.key)] = False

        elif event.type == pg.VIDEORESIZE:
            io.display_size = event.size

    def process_inputs(self):
        io = imgui.get_io()
        now = pg.time.get_ticks() / 1000.0
        io.delta_time = (now - self._gui_time) if self._gui_time else 1 / 60
        if io.delta_time <= 0:
            io.delta_time = 1 / 1000
        self._gui_time = now

def ortho(left, right, bottom, top, near, far):
    return np.array([
        [2/(right-left), 0, 0, -(right+left)/(right-left)],
        [0, 2/(top-bottom), 0, -(top+bottom)/(top-bottom)],
        [0, 0, -2/(far-near), -(far+near)/(far-near)],
        [0, 0, 0, 1],
    ], dtype=np.float32).T


class Color3:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
        self.list = [r,g,b]
        if not type(r) == int: raise TypeError(f"R must be an intager")
        if not type(g) == int: raise TypeError(f"G must be an intager")
        if not type(b) == int: raise TypeError(f"B must be an intager")

    
    def UnitColor(self):
        return Color3(
            int(self.r/255),
            int(self.g/255),
            int(self.b/255)
        )

    def __repr__(self):
        return f"Color3({self.r}, {self.g}, {self.b})"
    
class Color4:
    def __init__(self, r, g, b, a):
        self.r = r
        self.g = g
        self.b = b
        self.a = a
        self.list = [r,g,b,a]

        self.UnitColor = UColor4(
            self.r/255,
            self.g/255,
            self.b/255,
            self.a/255
        )
        if not type(r) == int: raise TypeError(f"R must be an intager")
        if not type(g) == int: raise TypeError(f"G must be an intager")
        if not type(b) == int: raise TypeError(f"B must be an intager")
        if not type(a) == int: raise TypeError(f"A must be an intager")

    def __repr__(self):
        return f"Color4({self.r}, {self.g}, {self.b}, {self.a})"

class UColor4:
    def __init__(self, r, g, b, a):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

        self.list = [r,g,b,a]
        if not type(r) == int and not type(r) == float: raise TypeError(f"R must be an intager or float")
        if not type(g) == int and not type(g) == float: raise TypeError(f"G must be an intager or float")
        if not type(b) == int and not type(b) == float: raise TypeError(f"B must be an intager or float")
        if not type(a) == int and not type(a) == float: raise TypeError(f"A must be an intager or float")

    def __repr__(self):
        return f"UColor4({self.r}, {self.g}, {self.b}, {self.a})"

def ColorToTuple(color) -> Color3 | Color4 | UColor4:
    if type(color) == Color3:
        return (color.r, color.g, color.b)
    elif type(color) == Color4 or UColor4:
        return (color.r, color.g, color.b, color.a)
    
    
class Key(Enum):
        # Letters
        A = pg.K_a
        B = pg.K_b
        C = pg.K_c
        D = pg.K_d
        E = pg.K_e
        F = pg.K_f
        G = pg.K_g
        H = pg.K_h
        I = pg.K_i
        J = pg.K_j
        K = pg.K_k
        L = pg.K_l
        M = pg.K_m
        N = pg.K_n
        O = pg.K_o
        P = pg.K_p
        Q = pg.K_q
        R = pg.K_r
        S = pg.K_s
        T = pg.K_t
        U = pg.K_u
        V = pg.K_v
        W = pg.K_w
        X = pg.K_x
        Y = pg.K_y
        Z = pg.K_z

        # Numbers
        ZERO = pg.K_0
        ONE = pg.K_1
        TWO = pg.K_2
        THREE = pg.K_3
        FOUR = pg.K_4
        FIVE = pg.K_5
        SIX = pg.K_6
        SEVEN = pg.K_7
        EIGHT = pg.K_8
        NINE = pg.K_9

        # Movement
        UP = pg.K_UP
        DOWN = pg.K_DOWN
        LEFT = pg.K_LEFT
        RIGHT = pg.K_RIGHT

        # Common keys
        SPACE = pg.K_SPACE
        ENTER = pg.K_RETURN
        ESCAPE = pg.K_ESCAPE
        TAB = pg.K_TAB
        BACKSPACE = pg.K_BACKSPACE
        DELETE = pg.K_DELETE

        # Modifiers
        SHIFT = pg.K_LSHIFT
        CTRL = pg.K_LCTRL
        ALT = pg.K_LALT

        # Function keys
        F1 = pg.K_F1
        F2 = pg.K_F2
        F3 = pg.K_F3
        F4 = pg.K_F4
        F5 = pg.K_F5
        F6 = pg.K_F6
        F7 = pg.K_F7
        F8 = pg.K_F8
        F9 = pg.K_F9
        F10 = pg.K_F10
        F11 = pg.K_F11
        F12 = pg.K_F12

class Input:
    def __init__(self):
        self.keys = None
        self.old_key = None
   
    def update(self):
        self.keys = pg.key.get_pressed()

    def is_key_pressed(self,key) -> int:
        if self.keys is None:
            return False
        
        return self.keys[key.value]

    def key_button_down(self, key) -> int:
        if self.keys[pg.K_0] and not self.old_key[pg.K_0]:
            return

        self.old_key = self.keys

        if self.keys is None:
            return False
                
        return self.keys[key.value]

    def clearInput(self):
        self.keys = 0

class PhysicsType(Enum):
    DEFAULT = 0
    BOX2D = 1
    MUNK = 2

class TweenType(Enum):
    LINEAR = 0
    EXPONETIAL = 1
    QUADRATIC = 2

def getFile(path, name) -> str | None:
    projectFile = os.path.join(path, name)        
    
    if os.path.exists(projectFile):
        return projectFile
    else:
        print(f"File not found: {projectFile}")
        return None

class Tween:
    def __init__(self):
        pass


class TextureFilter(Enum):
    LINEAR = GL_LINEAR
    NEAREST = GL_NEAREST

class TextureWarping(Enum):
    REPEAT = GL_REPEAT
    MIRRORED_REPEAT = GL_MIRRORED_REPEAT
    CLAMP_TO_EDGE = GL_CLAMP_TO_EDGE
    CLAMP_TO_BOARDER = GL_CLAMP_TO_BORDER


PPM = 50.0  # 50 pixels = 1 meter

def to_m(v):
    return v / PPM

def to_px(v):
    return v * PPM