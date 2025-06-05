# core/shader_manager.py

import moderngl
import numpy as np
from PIL import Image

class ShaderManager:
    def __init__(self, width, height):
        self.ctx = moderngl.create_standalone_context()
        self.width = width
        self.height = height
        self.fbo = self.ctx.framebuffer(
            color_attachments=[self.ctx.texture((width, height), 4)]
        )

    def apply_shader(self, image_np, shader_path, uniforms=None):
        img = image_np.astype('f4') / 255.0
        texture = self.ctx.texture((self.width, self.height), 3, data=img.tobytes())
        texture.use()

        with open(shader_path, 'r') as f:
            shader_source = f.read()

        prog = self.ctx.program(vertex_shader=self.vertex_shader(), fragment_shader=shader_source)
        if uniforms:
            for name, value in uniforms.items():
                if name in prog:
                    prog[name].value = value

        quad = self.ctx.buffer(np.array([
            -1.0, -1.0, 0.0, 0.0,
             1.0, -1.0, 1.0, 0.0,
            -1.0,  1.0, 0.0, 1.0,
             1.0,  1.0, 1.0, 1.0,
        ], dtype='f4').tobytes())

        vao = self.ctx.simple_vertex_array(prog, quad, 'in_vert', 'in_text')
        self.fbo.use()
        vao.render(moderngl.TRIANGLE_STRIP)
        data = self.fbo.read(components=3)
        img_out = np.frombuffer(data, dtype=np.uint8).reshape((self.height, self.width, 3))
        return img_out

    def vertex_shader(self):
        return """
        #version 330
        in vec2 in_vert;
        in vec2 in_text;
        out vec2 v_text;
        void main() {
            gl_Position = vec4(in_vert, 0.0, 1.0);
            v_text = in_text;
        }
        """