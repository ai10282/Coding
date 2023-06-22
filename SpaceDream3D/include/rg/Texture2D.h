//
// Created by matf-rg on 30.10.20..
//

#ifndef PROJECT_BASE_TEXTURE2D_H
#define PROJECT_BASE_TEXTURE2D_H
#include <glad/glad.h>
#include <stb_image.h>
#include <rg/Error.h>

class Texture2D {
    unsigned int m_Id;
public:
    Texture2D(std::string pathToImg, bool gammaCorrection) {
        unsigned int tex;
        glGenTextures(1, &tex);

        int width, height, nChannel;
        stbi_set_flip_vertically_on_load(true);
        unsigned char* data = stbi_load(pathToImg.c_str(), &width, &height, &nChannel, 0);

        if(data) {
            GLenum internalFormat = 0;
            GLenum dataFormat = 0;
            if(nChannel == 1)
                internalFormat = dataFormat = GL_RED;
            else if (nChannel == 3)
            {
                internalFormat = gammaCorrection ? GL_SRGB : GL_RGB;
                dataFormat = GL_RGB;
            }
            else if (nChannel == 4)
            {
                internalFormat = gammaCorrection ? GL_SRGB_ALPHA : GL_RGBA;
                dataFormat = GL_RGBA;
            }



            glBindTexture(GL_TEXTURE_2D, tex);


            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);

            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR);
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);


            glTexImage2D(GL_TEXTURE_2D, 0, internalFormat, width, height, 0, dataFormat, GL_UNSIGNED_BYTE, data);
            glGenerateMipmap(GL_TEXTURE_2D);

        }
        else {
            ASSERT( false, "Failed to load texture!\n");
        }

        stbi_image_free(data);
        m_Id = tex;
    }
    void active(GLenum e) {
        glActiveTexture(e);
        glBindTexture(GL_TEXTURE_2D, m_Id);
    }

};

#endif //PROJECT_BASE_TEXTURE2D_H
