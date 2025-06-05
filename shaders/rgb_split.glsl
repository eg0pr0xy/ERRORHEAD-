#version 330

in vec2 v_text;
out vec4 fragColor;

uniform sampler2D Texture;
uniform float offset_amount; // Added uniform for offset

void main() {
    float offset = offset_amount; // Use uniform for offset
    vec2 uv = v_text;
    float r = texture(Texture, uv + vec2(offset, 0.0)).r;
    float g = texture(Texture, uv).g;
    float b = texture(Texture, uv - vec2(offset, 0.0)).b;
    fragColor = vec4(r, g, b, 1.0);
}