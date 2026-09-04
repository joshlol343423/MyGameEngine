#version 330 core

in vec2 aUV;
in vec4 color;

uniform sampler2D uObjTex;
uniform bool uCheckObjTex;
out vec4 FragColor;



vec4 tex_color = texture(uObjTex, aUV);
void main() {
    if (uCheckObjTex)
    {
        if (tex_color.a < 0.1) discard;
        FragColor = tex_color;
    }
    else
    {
        FragColor = color;
    }
}