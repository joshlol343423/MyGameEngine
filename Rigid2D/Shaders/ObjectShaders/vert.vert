#version 330 core
layout (location = 0) in vec2 aPos;
layout (location = 1) in vec2 uv;

uniform vec2 uSize;
uniform vec2 uPos;

uniform vec4 uColor;

out vec4 color;
out vec2 aUV;

void main() {
    aUV = uv;
    color = uColor; 
    vec2 p = aPos * uSize + uPos;
    gl_Position = vec4(p, 0.0, 1.0);
}