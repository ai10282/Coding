#version 330 core
layout (location = 0) out vec4 FragColor;
layout (location = 1) out vec4 BrightColor;

in vec3 FragPos;
in vec3 Normal;
in vec2 TexCoords;

struct DirLight {
    vec3 direction;

    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
};

struct PointLight {
    vec3 position;

    vec3 ambient;
    vec3 diffuse;
    vec3 specular;

    float constant;
    float linear;
    float quadratic;
};

struct SpotLight {
    vec3 position;
    vec3 direction;

    float cutOff;
    float outerCutOff;

    vec3 ambient;
    vec3 diffuse;
    vec3 specular;

    float constant;
    float linear;
    float quadratic;
};

#define NR_SPOT_LIGHTS 4

uniform sampler2D texture_diffuse1;
uniform sampler2D texture_specular1;

uniform vec3 lightColor;
uniform vec3 viewPos;
uniform DirLight dirLight;
uniform PointLight pointLight;
uniform SpotLight spotLight[NR_SPOT_LIGHTS];

vec3 CalcDirLight(DirLight light, vec3 normal, vec3 viewDir);
vec3 CalcPointLight(PointLight light, vec3 normal, vec3 fragPos, vec3 viewDir);
vec3 CalcSpotLight(SpotLight light, vec3 normal, vec3 fragPos, vec3 viewDir);

void main()
{
    vec3 normal = normalize(Normal);
    vec3 viewDir = normalize(viewPos - FragPos);
    vec3 result = CalcDirLight(dirLight, normal, viewDir);
    result += CalcPointLight(pointLight, normal, FragPos, viewDir);
    for (int i = 0; i < NR_SPOT_LIGHTS; i++){
        result += CalcSpotLight(spotLight[i], normal, FragPos, viewDir);
    }
    float brightness = dot(result, vec3(0.2126, 0.7152, 0.0722));
        if(brightness > 1.0)
            BrightColor = vec4(result, 1.0);
        else
            BrightColor = vec4(0.0, 0.0, 0.0, 1.0);
        FragColor = vec4(result, 1.0);
}

vec3 CalcDirLight(DirLight light, vec3 normal, vec3 viewDir) {
    vec3 lightDir = normalize(-light.direction);
    float diff = max(dot(normal, lightDir), 0.0);

    vec3 halfwayDir = normalize(lightDir + viewDir);
    float spec = pow(max(dot(normal, halfwayDir), 0.0), 32.0);

    vec3 ambient = light.ambient * vec3(texture(texture_diffuse1, TexCoords));
    vec3 diffuse = light.diffuse * diff * vec3(texture(texture_diffuse1, TexCoords));
    vec3 specular = light.specular * spec * vec3(texture(texture_specular1, TexCoords).xxx);

    return (ambient + diffuse + specular);
}

vec3 CalcPointLight(PointLight light, vec3 normal, vec3 fragPos, vec3 viewDir) {
    vec3 lightDir = normalize(light.position - fragPos);
    float diff = max(dot(normal, lightDir), 0.0);

    vec3 halfwayDir = normalize(lightDir + viewDir);
    float spec = pow(max(dot(normal, halfwayDir), 0.0), 32.0);

    float distance = length(light.position - fragPos);
    float attenuation = 1.0 / (distance * distance);

    vec3 ambient = light.ambient * attenuation * vec3(texture(texture_diffuse1, TexCoords));
    vec3 diffuse = light.diffuse * diff * attenuation * vec3(texture(texture_diffuse1, TexCoords));
    vec3 specular = light.specular * spec * attenuation * vec3(texture(texture_specular1, TexCoords).xxx);

    return(ambient + diffuse + specular);
}

vec3 CalcSpotLight(SpotLight light, vec3 normal, vec3 fragPos, vec3 viewDir){
    vec3 lightDir = normalize(light.position - fragPos);
    float diff = max(dot(normal, lightDir), 0.0);

    vec3 halfwayDir = normalize(lightDir + viewDir);
    float spec = pow(max(dot(normal, halfwayDir), 0.0), 32.0);

    float distance = length(light.position - fragPos);
    float attenuation = 1.0 / (distance * distance);

    float theta = dot(lightDir, normalize(-light.direction));
    float epsilon = (light.cutOff - light.outerCutOff);
    float intesity = clamp((theta - light.outerCutOff)/ epsilon, 0.0, 1.0);

    vec3 ambient = lightColor * light.ambient * attenuation * intesity * vec3(texture(texture_diffuse1, TexCoords));
    vec3 diffuse = lightColor * light.diffuse * diff * attenuation * intesity * vec3(texture(texture_diffuse1, TexCoords));
    vec3 specular = lightColor * light.specular * spec * attenuation * intesity * vec3(texture(texture_specular1, TexCoords).xxx);

    return (ambient + diffuse + specular);
}