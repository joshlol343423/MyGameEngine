Python version is 3.11.6

Therese are the libraries in the engine:

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

from math import *
import numba as nb
from numba import njit
