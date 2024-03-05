
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from pygame.locals import *


def yellow_rubber():
    amb = [0.05, 0.05, 0., 1.]
    dif = [0.5, 0.5, 0.4]
    spe = [0.7, 0.7, 0.04]
    shine = 0.078125
    glMaterialfv(GL_FRONT, GL_AMBIENT, amb);
    glMaterialfv(GL_FRONT, GL_DIFFUSE, dif);
    glMaterialfv(GL_FRONT, GL_SPECULAR, spe);
    glMaterialf(GL_FRONT, GL_SHININESS, shine * 128.0);

def emerald():
    amb = [0.0215, 0.1745, 0.0215, 1.]
    dif = [0.07568, 0.61424, 0.07568]
    spe = [0.633, 0.727811, 0.633]
    shine = 0.6
    glMaterialfv(GL_FRONT, GL_AMBIENT, amb);
    glMaterialfv(GL_FRONT, GL_DIFFUSE, dif);
    glMaterialfv(GL_FRONT, GL_SPECULAR, spe);
    glMaterialf(GL_FRONT, GL_SHININESS, shine * 128.0);

def black_plastic():
    amb = [0., 0., 0., 1.]
    dif = [0.01, 0.01, 0.01]
    spe = [0.50, 0.50, 0.50]
    shine = 0.25
    glMaterialfv(GL_FRONT, GL_AMBIENT, amb);
    glMaterialfv(GL_FRONT, GL_DIFFUSE, dif);
    glMaterialfv(GL_FRONT, GL_SPECULAR, spe);
    glMaterialf(GL_FRONT, GL_SHININESS, shine * 128.0);

def pearl():
    amb = [0.25, 0.20725, 0.20725]
    dif = [1, 0.829, 0.829]
    spe = [0.296648, 0.296648, 0.296648]
    shine = 0.088
    glMaterialfv(GL_FRONT, GL_AMBIENT, amb);
    glMaterialfv(GL_FRONT, GL_DIFFUSE, dif);
    glMaterialfv(GL_FRONT, GL_SPECULAR, spe);
    glMaterialf(GL_FRONT, GL_SHININESS, shine * 128.0);

def ruby():
    amb = [0.1745, 0.01175, 0.01175]
    dif = [0.61424, 0.04136, 0.04136]
    spe = [0.727811, 0.626959, 0.626959]
    shine = 0.6
    glMaterialfv(GL_FRONT, GL_AMBIENT, amb);
    glMaterialfv(GL_FRONT, GL_DIFFUSE, dif);
    glMaterialfv(GL_FRONT, GL_SPECULAR, spe);
    glMaterialf(GL_FRONT, GL_SHININESS, shine * 128.0);

def silver():
    amb = [0.19225, 0.19225, 0.19225]
    dif = [0.50754, 0.50754, 0.50754]
    spe = [0.508273, 0.508273, 0.508273]
    shine = 0.4
    glMaterialfv(GL_FRONT, GL_AMBIENT, amb);
    glMaterialfv(GL_FRONT, GL_DIFFUSE, dif);
    glMaterialfv(GL_FRONT, GL_SPECULAR, spe);
    glMaterialf(GL_FRONT, GL_SHININESS, shine * 128.0);


def jade():
    amb = [0.135,	0.2225,	0.1575]
    dif = [0.54,	0.89,	0.63]
    spe = [0.316228,	0.316228,	0.316228]
    shine = 0.1
    glMaterialfv(GL_FRONT, GL_AMBIENT, amb);
    glMaterialfv(GL_FRONT, GL_DIFFUSE, dif);
    glMaterialfv(GL_FRONT, GL_SPECULAR, spe);
    glMaterialf(GL_FRONT, GL_SHININESS, shine * 128.0);