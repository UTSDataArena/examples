#version 120
varying vec3 vertex_light_position;
varying vec4 eye_position;

void main (void)
{
    float x = gl_PointCoord.x;
    float y = gl_PointCoord.y;
    const float center_x = 0.5;
    const float center_y = 0.5;
    float zz = 0.25 - (x-center_x)*(x-center_x) - (y-center_y)*(y-center_y);

    if (zz <= 0.0 )
    	discard;

    float z = sqrt(zz);

    vec3 normal = vec3(x, y, z);

    // Lighting
    float diffuse_value = max(dot(normal, vertex_light_position), 0.0);

    vec4 pos = eye_position;
    pos.z += z * 0.5;
    pos = gl_ProjectionMatrix * pos;
		
    gl_FragDepth = (pos.z / pos.w + 1.0) / 2.0;
    gl_FragColor.rgb = gl_Color.rgb * diffuse_value ;
    // gl_FragColor.a = color.a;
}
