// Definicion de constantes
#define MAX_LIGHTS 8
#define NUM_LIGHTS {1}

// Definicion de variables
varying vec3 normal, v, eye, lightDir[MAX_LIGHTS];
vec4 texColor, ambient, diffuse, specular, finalColor;
uniform sampler2D texture[{0}];
uniform int toggletexture, togglebump;
vec3 N;

void main(void){

    // Si las texturas estan activadas se calculan las normales dado el normal texture
    if (toggletexture == 1){
        texColor = vec4(texture2D(texture[0], gl_TexCoord[0].st).rgb, 1.0);
        vec3 norm = normalize(texture2D(texture[1], gl_TexCoord[0].st).rgb - 0.5);
        N = norm;

    // Si no hay textura entonces se usa la normal pasada desde el vertex shader
    }else{
        texColor = vec4(0.0,0.0,0.0,0.0);
        N = normal;
    }

    // Colores final, ambiente, difuso y especular
    finalColor = vec4(0.0,0.0,0.0,0.0);
    ambient = vec4(0.0,0.0,0.0,0.0);
    diffuse = vec4(0.0,0.0,0.0,0.0);
    specular = vec4(0.0,0.0,0.0,0.0);

    // Por cada luz se calcula el color aportado
    for (int i=0; i<NUM_LIGHTS; ++i){

        // Se calculan los vectore L, E, R
        vec3 L = normalize(lightDir[i]);
        vec3 E = normalize(eye);
        vec3 R = vec3(0.0,0.0,0.0);
        if (togglebump == 1){
            R = reflect(-L,N);
        }else{
            R = normalize(reflect(-L,N));
        }
        float lambertTerm = dot(N,L);

        //Si N*L es valido se suma
        if (lambertTerm>0.0){

            // Se obtienen los colores de la luz y se suman adecuadamente
            vec4 Iamb = gl_FrontLightProduct[i].ambient;
            vec4 Idiff = gl_FrontLightProduct[i].diffuse * lambertTerm;
            vec4 Ispec = gl_FrontLightProduct[i].specular * pow(max(dot(R,E),0.0),gl_FrontMaterial.shininess);
            ambient += Iamb;
            diffuse += Idiff;
            specular+= Ispec;
        }
    }

    // Se aplica el color al pixel
    if (toggletexture == 1){
        gl_FragColor=texColor*(ambient+diffuse)+specular;
    }else{
        gl_FragColor=ambient+diffuse+specular;
    }

}