import ctypes
import math
import pygame
from pygame.locals import *
from OpenGL.GL import *

VERT = """
#version 330 core
layout (location = 0) in vec2 aPos;

uniform vec2 uPos;
uniform vec2 uScale;
uniform float uRot;
uniform vec2 uScreen;
uniform vec3 uColor;

out vec3 vColor;

void main() {
    float c = cos(uRot);
    float s = sin(uRot);
    vec2 p = aPos * uScale;
    vec2 r = vec2(p.x * c - p.y * s, p.x * s + p.y * c);
    vec2 world = r + uPos;
    vec2 ndc = (world / uScreen) * 2.0 - 1.0;
    ndc.y = -ndc.y;
    gl_Position = vec4(ndc, 0.0, 1.0);
    vColor = uColor;
}
"""

FRAG = """
#version 330 core
in vec3 vColor;
out vec4 FragColor;
void main() {
    FragColor = vec4(vColor, 1.0);
}
"""


def compile_program(vs_src, fs_src):
    def compile_shader(src, kind):
        s = glCreateShader(kind)
        glShaderSource(s, src)
        glCompileShader(s)
        if not glGetShaderiv(s, GL_COMPILE_STATUS):
            raise RuntimeError(glGetShaderInfoLog(s).decode())
        return s

    vs = compile_shader(vs_src, GL_VERTEX_SHADER)
    fs = compile_shader(fs_src, GL_FRAGMENT_SHADER)
    prog = glCreateProgram()
    glAttachShader(prog, vs)
    glAttachShader(prog, fs)
    glLinkProgram(prog)
    if not glGetProgramiv(prog, GL_LINK_STATUS):
        raise RuntimeError(glGetProgramInfoLog(prog).decode())
    glDeleteShader(vs)
    glDeleteShader(fs)
    return prog


def make_quad():
    verts = (GLfloat * 8)(
        -0.5, -0.5,
         0.5, -0.5,
         0.5,  0.5,
        -0.5,  0.5,
    )
    inds = (GLuint * 6)(0, 1, 2, 2, 3, 0)

    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)
    ebo = glGenBuffers(1)

    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, ctypes.sizeof(verts), verts, GL_STATIC_DRAW)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, ctypes.sizeof(inds), inds, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 8, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    glBindVertexArray(0)
    return vao


class Item:
    def __init__(self, x, y, w, h, color, spin):
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.color = color
        self.spin = spin
        self.rot = 0.0


def main():
    pygame.init()
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
    pygame.display.gl_set_attribute(
        pygame.GL_CONTEXT_PROFILE_MASK,
        pygame.GL_CONTEXT_PROFILE_CORE
    )

    size = (900, 600)
    pygame.display.set_mode(size, DOUBLEBUF | OPENGL | RESIZABLE)
    pygame.display.set_caption("Simple OpenGL Window")
    glViewport(0, 0, *size)

    program = compile_program(VERT, FRAG)
    vao = make_quad()

    u_pos = glGetUniformLocation(program, "uPos")
    u_scale = glGetUniformLocation(program, "uScale")
    u_rot = glGetUniformLocation(program, "uRot")
    u_screen = glGetUniformLocation(program, "uScreen")
    u_color = glGetUniformLocation(program, "uColor")

    items = [
        Item(200, 180, 80, 80, (1.0, 0.3, 0.3), 1.5),
        Item(450, 300, 140, 70, (0.3, 0.9, 0.4), -0.8),
        Item(700, 160, 60, 120, (0.3, 0.5, 1.0), 0.6),
        Item(320, 460, 100, 100, (1.0, 0.85, 0.2), 2.2),
        Item(640, 430, 90, 50, (0.9, 0.4, 1.0), -1.3),
    ]

    clock = pygame.time.Clock()
    running = True

    while running:
        dt = clock.tick(60) / 1000.0
        width, height = pygame.display.get_surface().get_size()

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == VIDEORESIZE:
                glViewport(0, 0, event.w, event.h)

        for item in items:
            item.rot += item.spin * dt

        glClearColor(0.08, 0.09, 0.12, 1)
        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(program)
        glUniform2f(u_screen, float(width), float(height))
        glBindVertexArray(vao)

        for item in items:
            glUniform2f(u_pos, item.x, item.y)
            glUniform2f(u_scale, item.w, item.h)
            glUniform1f(u_rot, item.rot)
            glUniform3f(u_color, *item.color)
            glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()