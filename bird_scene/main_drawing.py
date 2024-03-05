from math import degrees
import sys
import numpy as np
import pygame

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from pygame.locals import *
from PIL import Image as Image

from dog_model import *
from bird import *
from cube_map import *
from load_obj import load_leafs, load_pear
from materials import *


def main_drawing(cur_quadric, time1=None, time2=None):
    glPushMatrix()
    
    glPushMatrix() ########### fruits
    glScalef(3,3,3)
    glTranslatef(-60, 20, -60)
    load_leafs()
    glPopMatrix()

    glPushMatrix() ########### pear
    glTranslatef(0, -10, 0)
    glRotatef(60, -0.8, 1, 2)
    glScalef(10, 10, 10)
    load_pear()
    glPopMatrix()

    glPushMatrix() ########### bird
    glScalef(0.5, 0.5, 0.5)
    glTranslatef(-5, 6, 15)
    glRotatef(25, 1, 0, 0)
    glRotatef(-115, 0, 1, 0)
    bird()
    glPopMatrix()


    textname = load_cubemap_texture()
    enable_reflection_cube()
    glBindTexture(GL_TEXTURE_CUBE_MAP, textname)
    pearl()
    glColor3d(1,1,1);
    glPushMatrix()  ############### bottom
    glTranslatef(0, -40, -20)
    glScalef(1, 0.3, 1)
    gluSphere(cur_quadric, 50, 64, 32)
    glPopMatrix()


    R = 30
    plane = 30
    silver()
    glPushMatrix()  #### big ball
    glTranslatef(20, R-plane, -40)
    gluSphere(cur_quadric, R, 32, 16)
    glPopMatrix()
    disable_reflection_cube()

    emerald()
    glColor3d(0.2, 0.9, 0.8);
    R = 22
    glPushMatrix()
    glTranslatef(-30, R-plane, -30)
    gluSphere(cur_quadric, R, 32, 16)
    glPopMatrix()

    yellow_rubber()
    glColor3d(1., 0.7, 0.1);
    R = 6
    glPushMatrix()
    glTranslatef(-10, R-plane-1, 20)
    gluSphere(cur_quadric, R, 32, 16)
    glPopMatrix()
    
    black_plastic()
    glColor3d(0., 0, 0);
    R = 7
    glPushMatrix()
    glTranslatef(25, R-plane-4, 20)
    gluSphere(cur_quadric, R, 32, 16)
    glPopMatrix()

    glColor3d(1,1,1);
    glPopMatrix()
    return

def draw_ref_plane(length=20, depth=5):
    glColor3d(0.6, 0.5, 0.9);
    glBegin(GL_QUADS);
    glVertex3f(length, -depth, length);
    glVertex3f(length, -depth, -length);
    glVertex3f(-length, -depth, -length);
    glVertex3f(-length, -depth, length);
    glEnd();

    glPointSize(10);
    glColor3d(1, 0, 0);
    glBegin(GL_POINTS);
    glVertex3f(0,0,0);
    glEnd()
    glColor3d(0, 0, 1);
    glPointSize(10);
    glBegin(GL_POINTS);
    glVertex3f(10,15,0);
    glVertex3f(0,25,0);
    glVertex3f(0,15,10);
    glEnd()

def bird():
    glPushMatrix()
    line_mode, cps, t_elements, cp_num = read_datafile()
    points = draw_splines(cps, line_mode, t_elements)
    draw_surface(points, cp_num)
    glPopMatrix()

def enable_reflection_cube():
    glEnable(GL_TEXTURE_GEN_S)
    glEnable(GL_TEXTURE_GEN_T)
    glEnable(GL_TEXTURE_GEN_R)
    glEnable(GL_TEXTURE_CUBE_MAP)

def disable_reflection_cube():
    glDisable(GL_TEXTURE_GEN_S)
    glDisable(GL_TEXTURE_GEN_T)
    glDisable(GL_TEXTURE_GEN_R)
    glDisable(GL_TEXTURE_CUBE_MAP)
