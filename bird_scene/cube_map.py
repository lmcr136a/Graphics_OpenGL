from math import degrees
import sys
import numpy as np
import pygame

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from pygame.locals import *
from PIL import Image as Image


def draw_skybox(texname, size=300):

    glEnable(GL_TEXTURE_2D)
    load_sq_texture(paths[0])
    glBegin(GL_QUADS)
    glNormal3f(-1.0, 0.0, 0.0)
    glTexCoord2f(0.0, 0.0); glVertex3f(size, -size, size)
    glTexCoord2f(1.0, 0.0); glVertex3f(size, -size, -size)
    glTexCoord2f(1.0, 1.0); glVertex3f(size, size, -size)
    glTexCoord2f(0.0, 1.0); glVertex3f(size, size, size)
    glEnd()
    glDisable(GL_TEXTURE_2D)

    glEnable(GL_TEXTURE_2D)
    load_sq_texture(paths[1])
    glBegin(GL_QUADS);
    glNormal3f(1.0, 0.0, 0.0)
    glTexCoord2f(0.0, 0.0); glVertex3f(-size, -size, -size)
    glTexCoord2f(1.0, 0.0); glVertex3f(-size, -size, size)
    glTexCoord2f(1.0, 1.0); glVertex3f(-size, size, size)
    glTexCoord2f(0.0, 1.0); glVertex3f(-size, size, -size)
    glEnd()
    glDisable(GL_TEXTURE_2D)

    glEnable(GL_TEXTURE_2D)
    load_sq_texture(paths[3])
    glBegin(GL_QUADS)
    glNormal3f( 0.0, 1.0, 0.0)
    glTexCoord2f(0.0, 0.0); glVertex3f(-size, -size, -size)
    glTexCoord2f(0.0, 1.0); glVertex3f(-size, -size, size)
    glTexCoord2f(1.0, 1.0); glVertex3f( size, -size, size)
    glTexCoord2f(1.0, 0.0); glVertex3f( size, -size, -size)
    glEnd()
    glDisable(GL_TEXTURE_2D)

    glEnable(GL_TEXTURE_2D)
    load_sq_texture(paths[2])
    glBegin(GL_QUADS);
    glNormal3f( 0.0, -1.0, 0.0)
    glTexCoord2f(0.0, 1.0); glVertex3f(-size, size, -size)
    glTexCoord2f(0.0, 0.0); glVertex3f(-size, size, size)
    glTexCoord2f(1.0, 0.0); glVertex3f( size, size, size)
    glTexCoord2f(1.0, 1.0); glVertex3f( size, size, -size)
    glEnd()
    glDisable(GL_TEXTURE_2D)
    
    glEnable(GL_TEXTURE_2D)
    load_sq_texture(paths[4])
    glBegin(GL_QUADS)
    glNormal3f( 0.0, 0.0, -1.0)
    glTexCoord2f(0.0, 0.0); glVertex3f(-size, -size, size)
    glTexCoord2f(1.0, 0.0); glVertex3f( size, -size, size)
    glTexCoord2f(1.0, 1.0); glVertex3f( size, size, size)
    glTexCoord2f(0.0, 1.0); glVertex3f(-size, size, size)
    glEnd()
    glDisable(GL_TEXTURE_2D)

    glEnable(GL_TEXTURE_2D)
    load_sq_texture(paths[5])
    glBegin(GL_QUADS)
    glNormal3f( 0.0, 0.0, 1.0)
    glTexCoord2f(0.0, 0.0); glVertex3f( size, -size, -size)
    glTexCoord2f(1.0, 0.0); glVertex3f(-size, -size, -size)
    glTexCoord2f(1.0, 1.0); glVertex3f(-size, size, -size)
    glTexCoord2f(0.0, 1.0); glVertex3f( size, size, -size)
    glEnd()
    glDisable(GL_TEXTURE_2D)


faces = [
    GL_TEXTURE_CUBE_MAP_POSITIVE_X,
    GL_TEXTURE_CUBE_MAP_NEGATIVE_X,
    GL_TEXTURE_CUBE_MAP_POSITIVE_Y,
    GL_TEXTURE_CUBE_MAP_NEGATIVE_Y,
    GL_TEXTURE_CUBE_MAP_POSITIVE_Z,
    GL_TEXTURE_CUBE_MAP_NEGATIVE_Z
]

paths = [
    "skybox/right.jpg",
    "skybox/left.jpg",
    "skybox/top.jpg",
    "skybox/bottom.jpg",
    "skybox/front.jpg",
    "skybox/back.jpg"
]

# paths = [
#     "sample/right.jpg",
#     "sample/left.jpg",
#     "sample/top.jpg",
#     "sample/bottom.jpg",
#     "sample/front.jpg",
#     "sample/back.jpg"
# ]



def load_cubemap_texture(PARAM=GL_REFLECTION_MAP):
    glClearColor(1,1,1,1.0)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_DEPTH_TEST)

    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    texname = glGenTextures(1)
    glBindTexture(GL_TEXTURE_CUBE_MAP, texname)

    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    for face, path in zip(faces, paths):
        image = Image.open(path).resize((300, 300))
        (width, height) = image.size[0:2]
        img_str = image.tobytes()
        glTexImage2D(face, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_str)

    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, PARAM)
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, PARAM)
    glTexGeni(GL_R, GL_TEXTURE_GEN_MODE, PARAM)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE);

    return texname


def load_sq_texture(img_path):
    textureSurface = pygame.image.load(f'{img_path}')
    textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
    width = textureSurface.get_width()
    height = textureSurface.get_height()

    texid = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texid)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
