//
// Created by adminstrator on 13/04/2022.
//

#ifndef PROJECT_BASE_CUBEMAP2D_H
#define PROJECT_BASE_CUBEMAP2D_H
#include <glad/glad.h>
#include <stb_image.h>
#include <rg/Error.h>
#include <vector>

using namespace std;

class Cubemap2D {
    unsigned int w_Id;
public:
    Cubemap2D(vector<std::string> faces) {
        unsigned int tex;
        glGenTextures(1, &tex);
        glBindTexture(GL_TEXTURE_CUBE_MAP, tex);

        int width, height, nChannel;
        stbi_set_flip_vertically_on_load(true);
        for (unsigned int i = 0; i < faces.size(); i++) {
            unsigned char *data = stbi_load(faces[i].c_str(), &width, &height, &nChannel, 0);
            if (data) {
                glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X + i, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, data);
                stbi_image_free(data);
            }
            else {
                ASSERT(false, "Failed to load texture!\n");
                stbi_image_free(data);
            }
        }

        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE);


        w_Id = tex;
    }
    void active(GLenum e) {
        glActiveTexture(e);
        glBindTexture(GL_TEXTURE_CUBE_MAP, w_Id);
    }

};

#endif //PROJECT_BASE_CUBEMAP2D_H
