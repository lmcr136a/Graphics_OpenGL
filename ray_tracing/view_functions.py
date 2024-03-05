from math import degrees
import sys
import numpy as np
import pygame

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from pygame.locals import *
from PIL import Image as Image

window_size = (800, 800)
POINT_COLOR = (1,0.2,0.3,0.5)

def handle_pause_and_quit(displayCenter, paused, run):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                run = False
            if event.key == pygame.K_PAUSE or event.key == pygame.K_p:
                paused = not paused
                # pygame.mouse.set_pos(displayCenter) 
        if not paused: 
            # pygame.mouse.set_pos(displayCenter)   
            if event.type == pygame.MOUSEBUTTONDOWN:
                return paused, run
    return paused, run


# dolly in and out
def handle_movement(keypress, unit=2):
    if keypress[pygame.K_w]:
        glTranslatef(0,0,unit)
    if keypress[pygame.K_s]:
        glTranslatef(0,0,-unit)
    if keypress[pygame.K_d]:
        glTranslatef(-unit,0,0)
    if keypress[pygame.K_a]:
        glTranslatef(unit,0,0)
    if keypress[pygame.K_e]:
        glTranslatef(0,unit,0)
    if keypress[pygame.K_q]:
        glTranslatef(0,-unit,0)

def handle_zoom(keypress, fov, degree=1, far=1000):
    #if keypress[pygame.K_e]:
    #    glMatrixMode(GL_PROJECTION)
    #    glLoadIdentity()
    #   gluPerspective(80, window_size[0]/window_size[1], 0.1, far)
    #    glMatrixMode( GL_MODELVIEW )
    #    return fov

    if (keypress[pygame.K_LSHIFT] or keypress[pygame.K_RSHIFT]):
        if keypress[pygame.K_w]:
            fov -= degree
        elif keypress[pygame.K_s]:
            fov += degree
    fov = max(0, fov)
    fov = min(90., fov)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fov, window_size[0]/window_size[1], 0.1, far)
    glMatrixMode( GL_MODELVIEW )
    return fov


def get_mouse_position():
    po = np.array(pygame.mouse.get_pos()).astype(np.float64)
    po[1] = window_size[1] - po[1]
    po -= 0.5*np.array(window_size)
    return po


def rotate_view(startPoint, rotatings, keypress, users_axis=None):
    #if keypress[pygame.K_e]:
    #    glRotatef(-60, -0.2, -0.9, 1.)
    #    return None

    endpoint = get_mouse_position()
    v1 = np.array((window_size[0], startPoint[0], startPoint[1]))
    v2 = np.array((window_size[0], endpoint[0], endpoint[1]))
    if np.sum(v1 - v2) == 0:
        angle = 0
    else:
        angle = np.arccos(np.dot(v2, v1)/np.sqrt(np.sum(v1**2))/np.sqrt(np.sum(v2**2)))*150

    if users_axis is not None:
        model_axis = users_axis
    else:
        model_axis = np.cross(v1, v2)
        
    if  pygame.mouse.get_pressed()[0]:
        glPushMatrix()
        glRotatef(angle, model_axis[1], model_axis[2], 0 )
    
    for rotating in reversed(rotatings):
        glPushMatrix()
        glRotatef(rotating[1], rotating[0][1], rotating[0][2],  0)
    return (model_axis, angle)

    
def get_users_axis(keypress, cur_quadric, r=6, users_axis=None):
    if keypress[pygame.K_z]:
        glPushMatrix()
        if users_axis is None:
            ua = get_mouse_position()
            ua = np.array([0, ua[0]/window_size[0], ua[1]/window_size[1]])
            users_axis = r*ua
            users_axis[0] = np.sqrt(r**2 - users_axis[1]**2 - users_axis[2]**2)

        glTranslate(*users_axis)
        glColor4f(*POINT_COLOR)
        gluSphere(cur_quadric, 0.2, 32, 16)
        glPopMatrix()    

        glColor4f(0.9, 0.2, 0.3, 1)
        glPointSize(2);
        glBegin(GL_LINES)
        glVertex3f(*users_axis)
        glVertex3f(0, 0, 0)
        glEnd()
        if pygame.mouse.get_pressed()[0]:
            return users_axis