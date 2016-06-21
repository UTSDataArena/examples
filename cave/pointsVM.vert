#version 120

uniform sampler2D defaultTex;
varying vec3 vertex_light_position;
varying vec4 eye_position;



void main()
{
    eye_position = gl_ModelViewMatrix * gl_Vertex;
    vertex_light_position = normalize(gl_LightSource[0].position.xyz - eye_position.xyz);

    gl_Position = gl_ProjectionMatrix  * eye_position;
    gl_FrontColor = gl_Color;
}