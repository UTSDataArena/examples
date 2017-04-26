#ifdef GL_ES
precision mediump float;
precision mediump int;
#endif

#define PROCESSING_TEXTURE_SHADER

uniform sampler2D texture;
uniform vec2 texOffset;
varying vec4 vertTexCoord;

void main(void) {
  int i = 0;
  int j= 0;
  vec4 sum = vec4(0.0);

  for( i=-8;i<8;i++) {
    for( j=-8;j<8;j++) {
        sum += texture2D( texture, vertTexCoord.st + vec2(j,i)*texOffset.st)*0.1;
    }
  }

  gl_FragColor = sum*sum+ vec4(texture2D( texture, vertTexCoord.st).rgb, 1.0);
}
