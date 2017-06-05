// Definicion de constantes
#define MAX_LIGHTS 8
#define NUM_LIGHTS {0}

// Definicion de variables
varying vec3 normal,v,eye,lightDir[MAX_LIGHTS];
vec3 T,B;
uniform int togglebump;

void main(void){

    // Vector de vertice
    v = vec3(gl_ModelViewMatrix * gl_Vertex);

    // Vector normal
    normal = normalize(gl_NormalMatrix * gl_Normal);

    // Vector tangente
    T = normalize(gl_NormalMatrix * (gl_Color.rgb - 0.5));

    // Se calcula el vector binormal, donde B=NxT
    B = cross(normal,T);
    mat3 TBNMatrix = mat3(T, B, normal);

    //Si bump esta activo entonces se multiplica el vector de vision (eye) por tbn
    if (togglebump == 1){
        eye = -v * TBNMatrix;
    }else{
        eye = -v;
    }

    // Se obtiene la posicion y la textura
    gl_Position = ftransform();
    gl_TexCoord[0]  = gl_TextureMatrix[0] * gl_MultiTexCoord0;

    // Se calcula la direccion de cada luz
    for(int i=0; i<NUM_LIGHTS; ++i){
        if (togglebump == 1){
            lightDir[i]=vec3(gl_LightSource[i].position.xyz - v) * TBNMatrix;
        }else{
            lightDir[i]=vec3(gl_LightSource[i].position.xyz - v);
        }
    }
    
}