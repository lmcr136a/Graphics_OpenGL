import sys
import numpy as np
import pygame

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from pygame.locals import *
from PIL import Image as Image


DOG_BROWN_COLOR = (0.4, 0.3, 0.28, 1)
DOG_BAIGE_COLOR = (0.6, 0.5, 0.45, 1)

def time_to_angle_pendulum(time, T, max_=20):
    time = time/T*max_
    if (time // max_) %2 == 0:
        angle = time % (max_)
    else:
        angle = max_ - time % (max_)
    return angle


def draw_body(cur_quadric, time1=None, T=50):
    glPushMatrix()
    glTranslatef(1, 0, -0.7)
    body(cur_quadric)

    front_legs_angle = time_to_angle_pendulum(time1, T, 15)

    glPushMatrix()
    glRotate(front_legs_angle, 0, 1, 0)
    draw_frontlegs(cur_quadric, time1, T)
    glPopMatrix()

    glPushMatrix()
    glRotate(-front_legs_angle, 0, 1, 0)
    draw_rarelegs(cur_quadric, time1, T)
    glPopMatrix()
    
    glTranslatef(1, 0, 0.53)
    tail_angle = time_to_angle_pendulum(time1, T, 50)
    glPushMatrix()
    glRotate(tail_angle, 0, 1, 0)
    tail(cur_quadric)
    glTranslatef(0.03, 0, 0.03)
    tail(cur_quadric)
    glPopMatrix()
    glPopMatrix()




def draw_frontlegs(cur_quadric, time1=None, T=50):
    glPushMatrix()
    glTranslatef(-0.5, 0.5, -0.5)

    # 오른다리
    leg(cur_quadric)

    foot_angle = time_to_angle_pendulum(time1, T, 30)
    glPushMatrix()
    glRotate(-15+foot_angle, 0, 1, 0)
    foot(cur_quadric)
    glPopMatrix()
    
    glTranslatef(0., -1, 0.)
    # 왼다리
    leg(cur_quadric)

    glPushMatrix()
    glRotate(-15+foot_angle, 0, 1, 0)
    foot(cur_quadric)
    glPopMatrix()

    glPopMatrix()


def draw_rarelegs(cur_quadric, time1=None, T=50):
    glPushMatrix()
    glTranslatef(0.5, 0.5, -0.4)

    # 오른다리
    leg(cur_quadric)
    
    foot_angle = time_to_angle_pendulum(time1, T, 20)
    glPushMatrix()
    glRotate(10-foot_angle, 0, 1, 0)
    foot(cur_quadric)
    glPopMatrix()

    glTranslatef(0., -1, 0.)
    # 왼다리
    leg(cur_quadric)

    foot_angle = time_to_angle_pendulum(time1, T, 20)
    glPushMatrix()
    glRotate(10-foot_angle, 0, 1, 0)
    foot(cur_quadric)
    glPopMatrix()


    glPopMatrix()


def foot(cur_quadric):
    glPushMatrix()
    glTranslatef(-0.1, 0, -0.5)

    glScalef(1, 1, 0.8)

    glColor4f(*DOG_BAIGE_COLOR)
    gluSphere(cur_quadric, 0.1, 32,16)

    glPushMatrix()
    glTranslatef(-0.1, 0.04, 0.01)
    glColor4f(*DOG_BAIGE_COLOR)
    gluSphere(cur_quadric, 0.05, 32,16)
    glTranslatef(0., -0.04, 0)
    glColor4f(*DOG_BAIGE_COLOR)
    gluSphere(cur_quadric, 0.05, 32,16)
    glTranslatef(0., -0.04, 0)
    glColor4f(*DOG_BAIGE_COLOR)
    gluSphere(cur_quadric, 0.05, 32,16)
    glPopMatrix()


    glPopMatrix()



def tail(cur_quadric):
    glPushMatrix()
    glColor4f(*DOG_BAIGE_COLOR)
    gluSphere(cur_quadric, 0.15, 32,16)
    glPopMatrix()


def draw_face(cur_quadric, time1=None, T=50):
    glPushMatrix()
    glScalef(0.9, 0.95, 1)
    glColor4f(*DOG_BROWN_COLOR)
    gluSphere(cur_quadric, 1.0, 32, 16) 
    
    # 턱과 입
    glPushMatrix()
    glTranslatef(-0.7, 0, -0.4)
    glRotatef(-30, 0., 1., 0.)
    glScalef(0.6, 1, 0.8)
    glColor4f(*DOG_BAIGE_COLOR)
    gluSphere(cur_quadric, 0.7, 32, 16) 
    glTranslatef(-0.01, 0, 0.73)
    glRotatef(30, 0., 1., 0.)
    glColor4f(0.2,0.2,0.2,1)
    gluSphere(cur_quadric, 0.12, 32, 16) 

    glPushMatrix()
    glTranslatef(-0.28, 0., -0.34)
    glRotatef(20, 0., 1., 0.)
    glLineWidth(10)
    glBegin(GL_LINE_STRIP)
    glColor4f(0.7,0.4,0.4,1)
    for i in range(180):
        glVertex3f(0, 0.2*(0.01*i-0.9), -np.sin(3.1415/180*i)*0.1)
    glEnd()
    glPopMatrix()
    glPopMatrix()
    glPushMatrix()
    glTranslatef(-0.02, 0, 0)
    glColor4f(*DOG_BAIGE_COLOR)
    glScalef(1.01, 0.8, 0.6)
    gluSphere(cur_quadric, 1.0, 32,16)
    glPopMatrix()

    # 눈
    glPushMatrix()
    glTranslatef(-0.93, 0.3, 0.3)    
    glRotate(10, 0., 1., 0.)
    glScalef(0.3, 1., 1.)
    glColor4f(0.,0.,0.,1.)
    gluSphere(cur_quadric, 0.2, 16, 8)     
    glTranslatef(-0.2, 0., 0.)
    glColor4f(1.,1.,1.,1.)
    gluSphere(cur_quadric, 0.1, 16, 8)     
    glTranslatef(0.07, -0.6, 0.)
    glColor4f(0.,0.,0.,1.)
    gluSphere(cur_quadric, 0.2, 16, 8)   
    glTranslatef(-0.2, 0., 0.)
    glColor4f(1.,1.,1.,1.)
    gluSphere(cur_quadric, 0.1, 16, 8)  
    glPopMatrix()
    
    glTranslatef(-0.75, -0.25, 0.6)

    glPushMatrix()
    glRotate(50, 1.,  0., 0.)
    glRotate(40, 0.,  1., 0.)
    glScalef(0.3, 0.7, 1.)
    glColor4f(*DOG_BAIGE_COLOR)
    gluSphere(cur_quadric, 0.1, 16, 8)  
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0., 0.5, 0.)
    glRotate(-50, 1.,  0., 0.)
    glRotate(40, 0.,  1., 0.)
    glScalef(0.3, 0.7, 1.)
    glColor4f(*DOG_BAIGE_COLOR)
    gluSphere(cur_quadric, 0.1, 16, 8)  
    glPopMatrix()
    glPopMatrix()

    # 귀
    ear_angle = time_to_angle_pendulum(time1, T, 30)
    glPushMatrix()
    glTranslatef(0., 0.9, 0.5)
    glRotate(30, 1, 0,0)
    glRotate(ear_angle, 1, 0,0)
    ear(cur_quadric)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0., -0.9, 0.5)
    glRotate(-30, 1, 0,0)
    glRotate(-ear_angle, 1, 0,0)
    ear(cur_quadric)
    glPopMatrix()


def ear(cur_quadric):
    glPushMatrix()
    glScalef(0.6, 0.1, 1.)
    glColor4f(*DOG_BAIGE_COLOR)
    gluSphere(cur_quadric, 0.6, 16, 8)  
    glPopMatrix()


def leg(cur_quadric):
    glPushMatrix()
    glRotatef(-20., 0., 1., 0.)
    glScalef(0.4, 0.4, 1)
    glColor4f(*DOG_BROWN_COLOR)
    gluSphere(cur_quadric, 0.3, 32,16)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0., 0., -0.3)
    glRotatef(30., 0., 1., 0.)
    glScalef(0.3, 0.3, 0.7)
    glColor4f(*DOG_BROWN_COLOR)
    gluSphere(cur_quadric, 0.3, 32,16)
    glPopMatrix()


def body(cur_quadric):
    glPushMatrix()
    glColor4f(*DOG_BROWN_COLOR)
    glScalef(1, 0.7, 0.6)
    gluSphere(cur_quadric, 1.2, 32,16)
    glTranslatef(0.1, 0, 0)
    glScalef(0.8, 1, 1)
    gluSphere(cur_quadric, 1.2, 32,16)
    glTranslatef(0.1, 0, 0)
    gluSphere(cur_quadric, 1.2, 32,16)
    glTranslatef(0.16, 0, 0.1)
    gluSphere(cur_quadric, 1., 32,16)
    glTranslatef(0.08, 0, 0.13)
    gluSphere(cur_quadric, 1., 32,16)
    glPopMatrix()