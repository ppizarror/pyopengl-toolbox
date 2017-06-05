// Definicion de constantes
#define MAX_LIGHTS 8
#define NUM_LIGHTS {1}

// Definicion de variables
varying vec3 N, v, lightDir[MAX_LIGHTS];
vec4 texColor, ambientdiff, specular, finalColor;
uniform sampler2D texture[{0}];
uniform int toggletexture;

void main(void){

    // Se obtiene el color de la textura
    if (toggletexture == 1){
       texColor = texture2D(texture[0], gl_TexCoord[0].st);
    }else{
       texColor = vec4(0.0,0.0,0.0,0.0);
    }

    // Colores finales, ambiental-difuso y especular
    finalColor = vec4(0.0,0.0,0.0,0.0);
    ambientdiff = vec4(0.0,0.0,0.0,0.0);
    specular = vec4(0.0,0.0,0.0,0.0);

    // Se calcula el aporte de cada luz
    for (int i=0; i<NUM_LIGHTS; ++i){

        // Se calculan los vectores L, E y R
        vec3 L = normalize(lightDir[i]);
        vec3 E = normalize(-v);
        vec3 R = normalize(reflect(-L,N));
        float lambertTerm = dot(N,L);

        // Si N*L es valido
        if (lambertTerm>0.0){

            // Se calculan los colores ambiental, difuso y especular
            vec4 Iamb = gl_FrontLightProduct[i].ambient;
            vec4 Idiff = gl_FrontLightProduct[i].diffuse * lambertTerm;
            vec4 Ispec = gl_FrontLightProduct[i].specular * pow(max(dot(R,E),0.0),gl_FrontMaterial.shininess);
            ambientdiff += Iamb+Idiff;
            specular+=Ispec;
        }
    }

    // Se aplica el color al pixel
    if (toggletexture == 1){
        gl_FragColor=texColor*(gl_FrontLightModelProduct.sceneColor+ambientdiff)+specular;
    }else{
        gl_FragColor=ambientdiff+specular;
    }

}