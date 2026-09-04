from math import *
import numba as nb
from numba import njit

class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.list = [x,y]
        if not type(x) == int and not type(x) == float: raise TypeError(f"X must be an intager or float")
        if not type(y) == int and not type(y) == float: raise TypeError(f"Y must be an intager or float")

    def __repr__(self):
        return f"Vector2({self.x} {self.y})"
   
    def __add__(self, other):
        if type(other) == float or type(other) == int:
            return Vector2(self.x + other, self.y + other)
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        if type(other) == float or type(other) == int:
            return Vector2(self.x - other, self.y - other)
        return Vector2(self.x - other.x, self.y - other.y)
    
    def __mul__(self, other):
        if type(other) == float or type(other) == int:
            return Vector2(self.x * other, self.y * other)
        return Vector2(self.x * other.x, self.y * other.y)
    
    def __truediv__(self, other):
        if type(other) == float or type(other) == int:
            return Vector2(self.x / other, self.y / other)
        return Vector2(self.x / other.x, self.y / other.y)
    
    def normalize(self):
        length = sqrt(self.x**2, self.y**2)

        if length == 0:
            return Vector2(0,0)
        
        return Vector2(self.x / length, self.y / length)

class Tween:
    def __init__(self, app):
        self.app = app

@njit
def backToNum(num, inter, new_num, dt):

    if num == new_num: return num

    if num > new_num:
        num -= inter * dt
        if num < new_num:
            num = new_num

        return num

    if num < new_num:
        num += inter * dt
        if num > new_num:
            num = new_num

        return num
        

def distance(v1 ,v2):
    distance = sqrt(
        (v2.x - v1.x)**2 +
        (v2.y - v1.y)**2 
    )  
    return distance 