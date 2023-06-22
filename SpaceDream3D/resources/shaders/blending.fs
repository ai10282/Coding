#version 330 core
out vec4 FragColor;

in vec2 TexCoords;

uniform sampler2D blending_texture;

void main()
{
    FragColor = texture(blending_texture, TexCoords);
}