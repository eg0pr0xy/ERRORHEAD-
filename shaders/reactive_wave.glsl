#version 330

in vec2 v_text;
out vec4 fragColor;

uniform sampler2D Texture;
uniform float amplitude;

void main() {
    vec2 uv = v_text;
    uv.x += sin(uv.y * 40.0) * 0.01 * amplitude;
    fragColor = texture(Texture, uv);
}