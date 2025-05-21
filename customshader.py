from scripts import geometry
from pyglet.graphics.shader import Shader, ShaderProgram

class customShader:
    def __init__(self, batch = None):
        self.batch = batch
        self.set_program_code()
    
    def set_program_code(self):
        # Vertex shader
        self.vertex_shader_code = """
        #version 330 core
        layout (location = 0) in vec3 position;
        layout (location = 1) in vec3 normal;
        layout (location = 2) in vec4 color;
        layout (location = 3) in float specular;

        out vec4 objColor;
        out float specularStrength;
        out vec3 fragPos;
        out vec3 fragNormal;

        uniform mat4 model;
        uniform mat4 view;
        uniform mat4 projection;

        void main() {
            objColor = color;
            specularStrength = specular;
            fragPos = vec3(model * vec4(position, 1.0));
            fragNormal = mat3(transpose(inverse(model))) * normal;
            gl_Position = projection * view * vec4(fragPos, 1.0);
        }
        """

        # Fragment shader
        self.fragment_shader_code = """
        #version 330 core
        in vec3 fragPos;
        in vec3 fragNormal;
        in vec4 objColor;
        in float specularStrength;

        out vec4 outputColor;

        uniform vec3 lightPos;
        uniform vec3 viewPos;
        uniform vec3 lightColor;


        void main() {
            // Ambient
            float ambientStrength = 0.0;
            vec3 ambient = ambientStrength * lightColor;

            // Diffuse
            vec3 norm = normalize(fragNormal);
            vec3 lightDir = normalize(lightPos - fragPos);
            float diff = max(dot(norm, lightDir), 0.0);
            vec3 diffuse = diff * lightColor;

            // Specular
            vec3 viewDir = normalize(viewPos - fragPos);
            vec3 reflectDir = reflect(-lightDir, norm);
            float spec = pow(max(dot(viewDir, reflectDir), 0.0), 128);
            vec3 specular = specularStrength * spec * lightColor;

            vec3 result = (ambient + diffuse + specular) * objColor.rgb;
            outputColor = vec4(result, 1.0);
        }
        """

        self.apply_shader()

    def apply_shader(self):
        vert_shader = Shader(self.vertex_shader_code, 'vertex')
        frag_shader = Shader(self.fragment_shader_code, 'fragment')
        self.program = ShaderProgram(vert_shader, frag_shader)