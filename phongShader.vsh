// Definicion de constantes
#define MAX_LIGHTS 8
#define NUM_LIGHTS {0}

// Definicion de variables
varying vec3 N, v, lightDir[MAX_LIGHTS];

void main(void){

    // Se calculan los vectores de vertice y normal
    v = vec3(gl_ModelViewMatrix * gl_Vertex);
    N = normalize(gl_NormalMatrix * gl_Normal);

    // Se calcula la posicion y la textura
    gl_Position = ftransform();
    gl_TexCoord[0]  = gl_TextureMatrix[0] * gl_MultiTexCoord0;

    // Se calculan las direcciones de cada luz
    for(int i=0; i<NUM_LIGHTS; ++i){
        lightDir[i]=vec3(gl_LightSource[i].position.xyz - v);
    }
    
}