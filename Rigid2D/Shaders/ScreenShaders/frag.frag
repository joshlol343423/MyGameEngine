#version 330 core

uniform sampler2D uTex;
uniform bool uUseTex;
in vec2 aUV;
out vec4 FragColor;



void main() {
    FragColor = texture(uTex, aUV);
}